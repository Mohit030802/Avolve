from typing import List, Optional
from pydantic import BaseModel, Field

class GapAnalysis(BaseModel):
    hard_skills_missing: List[str] = Field(description="Hard skills the user lacks for the target role.")
    soft_skills_missing: List[str] = Field(description="Soft skills the user lacks for the target role.")
    keywords_missing: List[str] = Field(description="Important industry keywords missing from the resume.")
    overall_readiness_score: int = Field(description="Readiness score from 0 to 100.")
    feedback_summary: str = Field(description="A brief summary of the gap analysis.")

class RoadmapStep(BaseModel):
    week_number: int = Field(description="The week number (e.g., 1, 2, 3...)")
    focus_area: str = Field(description="The main topic or focus for this week.")
    tasks: List[str] = Field(description="Specific, actionable tasks or topics to learn.")
    recommended_resources: List[str] = Field(description="Types of resources to use (e.g., 'React Official Docs', 'Build a Todo App').")

class CareerAnalysisRequest(BaseModel):
    target_role: Optional[str] = Field(None, description="The desired job title. If omitted, the system will infer the next logical step.")
    duration_weeks: int = Field(4, description="The duration of the learning roadmap in weeks (e.g., 4, 12, 24, 52).")

class CareerAnalysisResponse(BaseModel):
    target_role: str = Field(description="The role being targeted (either provided or inferred).")
    duration_weeks: int = Field(description="The total duration of the roadmap.")
    gap_analysis: GapAnalysis = Field(description="The detailed gap analysis.")
    roadmap: List[RoadmapStep] = Field(description="The week-by-week learning roadmap.")
