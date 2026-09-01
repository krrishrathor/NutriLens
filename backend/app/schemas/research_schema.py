from pydantic import BaseModel, Field
from typing import List

class SafetyAssessment(BaseModel):
    classification: str = Field(
        description="Safety classification based only on retrieved evidence."
    )
    basis: str = Field(
        description="Evidence supporting the classification."
    )
    caveat: str = Field(
        description="Important limitations or conditions of use."
    )

class ResearchResult(BaseModel):
    name: str
    aliases: List[str]
    category: str
    used_for: str
    safety: SafetyAssessment
    risk_level: str
    description: str
    sources: List[str]