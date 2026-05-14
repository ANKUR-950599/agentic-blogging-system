import os
import asyncio
import logging
from datetime import datetime, timezone
from typing import List, Dict, Optional
from bson import ObjectId

from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from dotenv import load_dotenv

# 1. Setup & Logging
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("StrategicAuthorAgent")

# 2. Configuration
GENAI_CLIENT = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "agentic_blogging_system")

# --- SCHEMA FIX ---
class BlogSection(BaseModel):
    header: str = Field(description="The H2 or H3 heading for this section.")
    content: str = Field(description="The main text/paragraphs for this section.")

class BlogPost(BaseModel):
    title: str = Field(description="SEO-optimized H1 title.")
    meta_description: str = Field(description="150-160 character snippet for Google.")
    slug: str = Field(description="URL-friendly version of the title.")
    narrative_framework: str = Field(description="The framework used (PAS, AIDA, etc.)")
    introduction: str = Field(description="The hook and psychological bridge.")
    # Gemini API prefers explicit models over List[Dict]
    body_sections: List[BlogSection] = Field(description="A list of content sections.")
    strategic_cta: str = Field(description="A high-intent call to action.")
    entity_keywords: List[str] = Field(description="Keywords used for Topical Authority.")

# 4. The Agent
class StrategicBlogAuthorAgent:
    def __init__(self):
        self.db = AsyncIOMotorClient(MONGO_URI)[DB_NAME]
        self.model_id = "gemini-3-flash-preview" 

    async def fetch_latest_strategy(self) -> Optional[Dict]:
        return await self.db.competitor_gap_strategies.find_one(
            {"post_status": {"$exists": False}}, 
            sort=[("created_at", -1)]
        )

    async def fetch_research_corpus(self, source_ids: List[str]) -> str:
        combined_text = ""
        for s_id in source_ids:
            doc = await self.db.research_corpus.find_one({"_id": ObjectId(s_id)})
            if doc:
                combined_text += f"\nSOURCE DATA ({doc.get('topic_title')}):\n{doc.get('massive_data_content', '')[:5000]}\n"
        return combined_text

    async def generate_blog_post(self, target_topic: Dict, research_text: str, gap_insight: str) -> BlogPost:
        system_instruction = """
        ACT AS A WORLD-CLASS STRATEGIC CONTENT DIRECTOR. 
        Write a high-authority blog post using the PAS (Problem-Agitate-Solution) framework.
        Focus on professional, punchy prose. Avoid AI clichés like 'delve' or 'tapestry'.
        Reference technical concepts from the research text to prove authority.
        """

        user_prompt = f"""
        TARGET TOPIC: {target_topic.get('title')}
        HOOK: {target_topic.get('hook')}
        ENTITIES: {target_topic.get('semantic_entities')}
        GAP INSIGHT: {gap_insight}

        RESEARCH DATA:
        {research_text}

        Generate the full blog post in JSON format.
        """

        response = await GENAI_CLIENT.aio.models.generate_content(
            model=self.model_id,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=BlogPost,
                temperature=0.7 
            )
        )
        return BlogPost.model_validate_json(response.text)

    async def run(self):
        logger.info("Starting Strategic Author Agent...")
        strategy = await self.fetch_latest_strategy()
        
        if not strategy:
            logger.info("No new gap strategies found.")
            return

        queue = strategy.get("high_impact_topic_queue", [])
        if not queue:
            logger.error("No topics found in the strategy queue.")
            return

        target_topic = queue[0] 
        source_ids = strategy.get("source_ids", [])
        gap_insight = strategy.get("share_of_voice_summary", "")

        logger.info(f"Writing blog post for: {target_topic.get('title')}")
        
        try:
            research_text = await self.fetch_research_corpus(source_ids)
            post = await self.generate_blog_post(target_topic, research_text, gap_insight)
            
            post_data = post.model_dump()
            post_data["strategy_ref"] = strategy["_id"]
            post_data["created_at"] = datetime.now(timezone.utc)
            
            result = await self.db.strategic_blog_posts.insert_one(post_data)

            await self.db.competitor_gap_strategies.update_one(
                {"_id": strategy["_id"]},
                {"$set": {"post_status": "authored", "post_id": result.inserted_id}}
            )

            print("\n" + "✨" * 20)
            print(f"BLOG POST READY: {post.title}")
            print(f"SECTIONS WRITTEN: {len(post.body_sections)}")
            print("✨" * 20 + "\n")

        except Exception as e:
            logger.error(f"Authoring failed: {e}")

if __name__ == "__main__":
    agent = StrategicBlogAuthorAgent()
    asyncio.run(agent.run())