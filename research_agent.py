import os
import asyncio
import logging
import json
from datetime import datetime, timezone
from typing import List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from tavily import TavilyClient
from dotenv import load_dotenv

# 1. Setup
load_dotenv()
genai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "agentic_blogging_system")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("UnifiedResearchAgent")

# 2. Updated Data Schemas
class UnifiedTopic(BaseModel):
    title: str = Field(description="The core unified theme found across personas.")
    rationale: str = Field(description="Why this is a high-impact commonality.")
    voc_keywords: List[str] = Field(description="Exact language (Bonglish/Specific phrases) to search for.")
    jtbd_summary: str = Field(description="The deeper emotional job being satisfied.")

# FIX: Wrapper class for the List
class UnifiedTopicList(BaseModel):
    topics: List[UnifiedTopic]

class ResearchSource(BaseModel):
    title: str
    url: str
    content_snippet: str

class ResearchCorpus(BaseModel):
    topic_title: str
    massive_data_content: str = Field(description="The synthesized deep-research text (10000+ words).")
    technical_concepts: List[str]
    expert_quotes_or_theories: List[str]
    sources: List[ResearchSource]
    unified_psychology_summary: str = Field(description="The 5-technique analysis result.")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# 3. System Instructions
STRATEGIST_SYSTEM_PROMPT = """
ACT AS A BEHAVIORAL ARCHITECT & MASTER RESEARCHER.
Analyze the provided Kolkata personas (18-29) using Identity Resolution, VoC Mining, JTBD, and clustering.
Output a list of Unified Topics that solve problems for ALL three personas simultaneously.
"""

RESEARCHER_SYSTEM_PROMPT = """
ACT AS A SENIOR DATA SYNTHESIZER.
Using the provided Web Search Results and Unified Psychology, create a 'Massive Data Corpus'.
Target high word count, high density, and authoritative regional tone.
"""

class UnifiedResearchAgent:
    def __init__(self):
        self.db = AsyncIOMotorClient(MONGO_URI)[DB_NAME]
        self.model_id = "gemini-3-flash-preview" 

    async def get_all_personas(self) -> List[Dict]:
        return await self.db.biopersonas.find({}).to_list(length=10)

    async def generate_unified_topics(self, personas: List[Dict]) -> List[UnifiedTopic]:
        """Step 1: Merge personas and find common ground."""
        logger.info("Synthesizing all persona data into Unified Topics...")
        # Clean persona data for the prompt
        context = []
        for p in personas:
            context.append({
                "name": p.get("name"),
                "category": p.get("category"),
                "layers": p.get("layers")
            })
        
        response = await genai_client.aio.models.generate_content(
            model=self.model_id,
            contents=f"PERSONA DATASET:\n{json.dumps(context)}",
            config=types.GenerateContentConfig(
                system_instruction=STRATEGIST_SYSTEM_PROMPT,
                response_mime_type="application/json",
                response_schema=UnifiedTopicList, # Use the wrapper here
                temperature=0.2
            )
        )
        
        # Parse the wrapped object
        parsed = UnifiedTopicList.model_validate_json(response.text)
        return parsed.topics

    def perform_search(self, topic: UnifiedTopic) -> List[Dict]:
        """Step 2: Web Research."""
        query = f"{topic.title} {', '.join(topic.voc_keywords)} Kolkata career trends"
        logger.info(f"Searching for: {topic.title}")
        try:
            results = tavily_client.search(query=query, search_depth="advanced", max_results=8)
            return results.get('results', [])
        except Exception as e:
            logger.error(f"Tavily search failed: {e}")
            return []

    async def synthesize_final_corpus(self, topic: UnifiedTopic, search_data: List[Dict]) -> ResearchCorpus:
        """Step 3: Combine Psychology + Web Data."""
        logger.info(f"Synthesizing final corpus for: {topic.title}")
        
        raw_web_context = "\n".join([f"Source: {r.get('title')}\nContent: {r.get('content')}" for r in search_data])
        
        prompt = f"""
        UNIFIED PSYCHOLOGY: {topic.rationale} | {topic.jtbd_summary}
        CORE THEME: {topic.title}
        WEB DATA: {raw_web_context}
        """

        response = await genai_client.aio.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=RESEARCHER_SYSTEM_PROMPT,
                response_mime_type="application/json",
                response_schema=ResearchCorpus, # Single objects usually work fine
                temperature=0.3
            )
        )
        
        corpus = ResearchCorpus.model_validate_json(response.text)
        corpus.topic_title = topic.title
        corpus.unified_psychology_summary = f"{topic.rationale} | Job: {topic.jtbd_summary}"
        return corpus

    async def run(self):
        # 1. Fetch
        personas = await self.get_all_personas()
        if not personas:
            logger.error("No personas found. Run seed_data.py first!")
            return

        # 2. Unified Topics
        topics = await self.generate_unified_topics(personas)
        logger.info(f"Identified {len(topics)} Unified Research Themes.")

        # 3. Process Each Topic
        for topic in topics:
            print(f"\n🚀 RESEARCHING: {topic.title}")
            
            # Search
            search_results = self.perform_search(topic)
            if not search_results:
                continue
            
            # Synthesize
            try:
                corpus = await self.synthesize_final_corpus(topic, search_results)
                # Save
                await self.db.research_corpus.insert_one(corpus.model_dump())
                print(f"📊 Saved Corpus: {len(corpus.massive_data_content)} chars | {len(corpus.sources)} sources")
            except Exception as e:
                logger.error(f"Synthesis failed for {topic.title}: {e}")

        print("\n✨ ALL UNIFIED RESEARCH COMPLETE.")

if __name__ == "__main__":
    agent = UnifiedResearchAgent()
    asyncio.run(agent.run())