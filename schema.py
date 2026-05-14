from pydantic import BaseModel, Field
from typing import List, Optional

class PersonaLayer(BaseModel):
    snapshot: str
    situation: str
    psychology: str
    the_gap: str
    pain_architecture: str
    voice_of_customer: str
    buying_behavior: str
    objection_stack: str
    trust_architecture: str
    digital_footprint: str
    transformation: str

class Biopersona(BaseModel):
    persona_id: str
    dataset_class: str  # e.g., "Tech Stack"
    name: str
    layers: PersonaLayer

class RankedActionablePoint(BaseModel):
    rank: int
    point_description: str
    impact_score: float # 1-10
    source_personas: List[str] # Which personas shared this pain?
    status: str = "pending_research" # pending_research, researched, exhausted