import operator
from typing import Annotated, TypedDict, Optional, List, Dict, Any
from app.schemas.career_schema import GapAnalysis, RoadmapStep

class AgentState(TypedDict):
    # Inputs
    resume_text: str
    parsed_resume_data: Dict[str, Any]  # The structured data from phase 1
    target_role: Optional[str]
    duration_weeks: int
    
    # Outputs (can be updated by different nodes)
    inferred_role: Optional[str]
    gap_analysis: Optional[GapAnalysis]
    roadmap: Optional[List[RoadmapStep]]
    
    # State tracking
    messages: Annotated[list, operator.add]
    errors: Annotated[list, operator.add]
