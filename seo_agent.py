import os
import asyncio
import logging
from datetime import datetime, timezone
from typing import List, Dict, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("SEOMetadataAgent")

GENAI_CLIENT = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "agentic_blogging_system")

# --- INDUSTRY-GRADE SEO SCHEMAS ---

class OpenGraphMetadata(BaseModel):
    og_title: str
    og_description: str
    og_type: str = "article"
    twitter_card: str = "summary_large_image"

class JSONLDMarkup(BaseModel):
    context: str = "https://schema.org"
    type: str = "BlogPosting"
    headline: str
    description: str
    keywords: str # Gemini handles string lists better in flat descriptions

class SEOPackage(BaseModel):
    focus_keywords: List[str] = Field(description="Primary entities to rank for.")
    seo_title: str = Field(description="H1 title - Under 60 chars.")
    meta_description: str = Field(description="Under 155 chars, high CTR.")
    slug: str = Field(description="URL-friendly slug.")
    og_metadata: OpenGraphMetadata
    schema_markup: JSONLDMarkup

# --- THE AGENT ---
class SEOMetadataAgent:
    def __init__(self):
        self.db = AsyncIOMotorClient(MONGO_URI)[DB_NAME]
        self.model_id = "gemini-3-flash-preview"

    async def fetch_latest_post(self) -> Optional[Dict]:
        """Handshake: Pulls the latest post that hasn't been optimized."""
        return await self.db.strategic_blog_posts.find_one(
            {"seo_status": {"$exists": False}},
            sort=[("created_at", -1)]
        )

    async def generate_metadata(self, post: Dict) -> SEOPackage:
        """Technical SEO asset generation."""
        
        system_instruction = """
        ACT AS A TECHNICAL SEO ARCHITECT.
        Generate a professional Metadata Package and Schema.org JSON-LD markup.
        - Focus on 'Topical Authority' and 'Search Intent'.
        - Ensure Meta Descriptions are punchy and promise a solution.
        - Use JSON-LD to define the content as a high-authority BlogPosting.
        """

        prompt = f"""
        BLOG POST CONTENT:
        Title: {post.get('title')}
        Intro: {post.get('introduction')}
        Strategic Entities: {post.get('entity_keywords')}
        CTA: {post.get('strategic_cta')}

        Generate the SEO Package in JSON format.
        """

        response = await GENAI_CLIENT.aio.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=SEOPackage,
                temperature=0.2
            )
        )
        return SEOPackage.model_validate_json(response.text)

    async def run(self):
        logger.info("🔍 Scanning for posts requiring SEO optimization...")
        post = await self.fetch_latest_post()
        
        if not post:
            logger.info("No unoptimized posts found.")
            return

        logger.info(f"Generating SEO Assets for: {post.get('title')}")

        try:
            # 1. Generate SEO Assets
            seo_pkg = await self.generate_metadata(post)
            
            # 2. Persistence
            metadata_doc = seo_pkg.model_dump()
            metadata_doc["post_id"] = post["_id"]
            metadata_doc["created_at"] = datetime.now(timezone.utc)
            
            await self.db.seo_metadata.insert_one(metadata_doc)

            # 3. Final Handshake - Marking the entire pipeline as COMPLETE
            await self.db.strategic_blog_posts.update_one(
                {"_id": post["_id"]},
                {"$set": {
                    "seo_status": "optimized",
                    "fully_completed_at": datetime.now(timezone.utc)
                }}
            )

            print("\n" + "🚀" * 20)
            print(f"SEO COMPLETE: {seo_pkg.seo_title}")
            print(f"SLUG: {seo_pkg.slug}")
            print(f"SCHEMA TYPE: {seo_pkg.schema_markup.type}")
            print("🚀" * 20 + "\n")

        except Exception as e:
            logger.error(f"SEO Agent Failed: {e}")

if __name__ == "__main__":
    agent = SEOMetadataAgent()
    asyncio.run(agent.run())