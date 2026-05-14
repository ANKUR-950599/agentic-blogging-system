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

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("CompetitorGapAgent")

GENAI_CLIENT = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
TAVILY_CLIENT = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "agentic_blogging_system"

# --- MODERN ANALYSIS SCHEMA ---

class CompetitiveInsight(BaseModel):
    technique: str = Field(description="The analysis framework used (e.g., Topical Mapping, Entity Clustering)")
    observation: str
    gap_opportunity: str = Field(description="The specific 'White Space' discovered.")

class TopicQueueItem(BaseModel):
    title: str
    semantic_entities: List[str] = Field(description="Core entities to cover for Topical Authority.")
    conversion_intent: str = Field(description="Informational, Navigational, or Transactional.")
    priority_score: int = Field(ge=1, le=10)
    hook: str = Field(description="The unique psychological angle to bypass competitors.")

class IndustryStrategyReport(BaseModel):
    share_of_voice_summary: str
    competitive_insights: List[CompetitiveInsight]
    high_impact_topic_queue: List[TopicQueueItem]
    silo_interlinking_plan: str = Field(description="How to connect these 5 themes for maximum SEO weight.")

# --- THE AGENT ---

class CompetitorGapAgent:
    def __init__(self):
        self.db = AsyncIOMotorClient(MONGO_URI)[DB_NAME]
        self.collection = self.db.research_corpus

    async def run_massive_analysis(self):
        # 1. Fetch all 5 research objects together
        cursor = self.collection.find({"gap_status": {"$exists": False}})
        research_docs = await cursor.to_list(length=10)

        if not research_docs:
            logger.info("No fresh research found. All sources have been analyzed.")
            return

        logger.info(f"⚡ Running Enterprise Analysis on {len(research_docs)} Research Themes...")

        # 2. Bundle Data for Deep Reasoning
        full_corpus = []
        for doc in research_docs:
            full_corpus.append({
                "topic": doc.get("topic_title"),
                "concepts": doc.get("technical_concepts", []),
                "psychology": doc.get("unified_psychology_summary"),
                "content_preview": doc.get("massive_data_content")[:3000]
            })

        # 3. Industry-Grade System Instruction
        system_instruction = """
        ACT AS A SENIOR GROWTH STRATEGIST & TECHNICAL SEO ARCHITECT.
        You are tasked with analyzing a corpus of 5 research modules using 10 modern techniques:
        1. Topical Authority Mapping
        2. Semantic Entity Clustering 
        3. Share of Voice (SoV) 
        4. White Space Detection
        5. Sentiment-Based Positioning
        6. Search Intent Alignment
        7. SERP Feature Prediction
        8. Knowledge Graph Gap Analysis
        9. Conversion Intent Scoring
        10. Silo Interlinking Strategy

        Identify where competitors are "Vibe-Coding" content and provide the "Deep Logic" alternative.
        """

        prompt = f"RESEARCH CORPUS:\n{json.dumps(full_corpus)}"

        try:
            response = await GENAI_CLIENT.aio.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=IndustryStrategyReport,
                    temperature=0.3
                )
            )

            report = IndustryStrategyReport.model_validate_json(response.text)
            
            # 4. Save Strategy
            strategy_entry = report.model_dump()
            strategy_entry["created_at"] = datetime.now(timezone.utc)
            strategy_entry["source_ids"] = [str(d["_id"]) for d in research_docs]
            
            await self.db.competitor_gap_strategies.insert_one(strategy_entry)

            # 5. Handshake: Update research objects
            for doc in research_docs:
                await self.collection.update_one(
                    {"_id": doc["_id"]},
                    {"$set": {
                        "gap_status": "analyzed",
                        "analyzed_at": datetime.now(timezone.utc),
                        "strategic_priority": next((t.priority_score for t in report.high_impact_topic_queue if t.title in doc['topic_title']), 5)
                    }}
                )

            print("\n" + "💎" * 20)
            print("ENTERPRISE ANALYSIS COMPLETE")
            print(f"Strategic White Space: {report.competitive_insights[0].gap_opportunity[:100]}...")
            print(f"Top Priority: {report.high_impact_topic_queue[0].title}")
            print("💎" * 20 + "\n")

        except Exception as e:
            logger.error(f"Analysis failed: {e}")

if __name__ == "__main__":
    agent = CompetitorGapAgent()
    asyncio.run(agent.run_massive_analysis())