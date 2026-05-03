from typing import Dict, Any, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from pydantic import BaseModel, Field

from app.core.config import settings
from app.core.logger import logger
from app.agents.state import AgentState
from app.schemas.career_schema import GapAnalysis, RoadmapStep

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    google_api_key=settings.google_api_key,
    temperature=0.2,
    max_retries=3
)

class RoadmapResponse(BaseModel):
    steps: List[RoadmapStep]

def determine_role_node(state: AgentState) -> Dict[str, Any]:
    """Infers the next logical career step if target_role is not provided."""
    logger.log("LangGraph", "determine_role_node", {"target_role_provided": bool(state.get("target_role"))})
    
    if state.get("target_role"):
        return {"inferred_role": state["target_role"]}
        
    prompt = ChatPromptTemplate.from_template(
        "Analyze the following resume data and suggest the single most logical next career role (job title) for this person.\n"
        "Consider their current skills and experience. Output ONLY the job title.\n\n"
        "Resume Data:\n{resume_data}"
    )
    
    chain = prompt | llm | StrOutputParser()
    
    try:
        inferred_role = chain.invoke({"resume_data": str(state["parsed_resume_data"])})
        inferred_role = inferred_role.strip()
        logger.log("LangGraph", "role_inferred", {"role": inferred_role})
        return {"inferred_role": inferred_role}
    except Exception as e:
        logger.log("LangGraph", "role_inference_error", {"error": str(e)})
        return {"errors": [f"Role inference failed: {str(e)}"]}

def gap_analyst_node(state: AgentState) -> Dict[str, Any]:
    """Analyzes gaps between current resume and target role."""
    role_to_target = state.get("inferred_role") or state.get("target_role")
    logger.log("LangGraph", "gap_analyst_node", {"role": role_to_target})
    
    parser = PydanticOutputParser(pydantic_object=GapAnalysis)
    
    prompt = ChatPromptTemplate.from_template(
        "You are an expert career counselor and technical recruiter.\n"
        "Analyze the gap between the candidate's current resume and their target role: '{target_role}'.\n"
        "{format_instructions}\n\n"
        "Candidate Resume Data:\n{resume_data}"
    )
    
    chain = prompt | llm | parser
    
    try:
        analysis = chain.invoke({
            "target_role": role_to_target,
            "resume_data": str(state["parsed_resume_data"]),
            "format_instructions": parser.get_format_instructions()
        })
        return {"gap_analysis": analysis}
    except Exception as e:
        logger.log("LangGraph", "gap_analysis_error", {"error": str(e)})
        return {"errors": [f"Gap analysis failed: {str(e)}"]}

def pathmaker_node(state: AgentState) -> Dict[str, Any]:
    """Generates a learning roadmap based on gaps and duration."""
    role_to_target = state.get("inferred_role") or state.get("target_role")
    duration = state.get("duration_weeks", 4)
    logger.log("LangGraph", "pathmaker_node", {"duration": duration})
    
    parser = PydanticOutputParser(pydantic_object=RoadmapResponse)
    
    prompt = ChatPromptTemplate.from_template(
        "You are an expert technical mentor. Create a {duration_weeks}-week learning roadmap "
        "to help the candidate transition into the role of '{target_role}'.\n"
        "Focus on addressing these specific gaps:\n"
        "- Missing Hard Skills: {hard_skills}\n"
        "- Missing Soft Skills: {soft_skills}\n"
        "- Missing Keywords: {keywords}\n\n"
        "The roadmap MUST have exactly {duration_weeks} steps (one for each week).\n"
        "{format_instructions}"
    )
    
    chain = prompt | llm | parser
    
    try:
        gaps = state.get("gap_analysis")
        if not gaps:
            raise ValueError("Gap analysis data is missing.")
            
        roadmap_res = chain.invoke({
            "duration_weeks": duration,
            "target_role": role_to_target,
            "hard_skills": ", ".join(gaps.hard_skills_missing),
            "soft_skills": ", ".join(gaps.soft_skills_missing),
            "keywords": ", ".join(gaps.keywords_missing),
            "format_instructions": parser.get_format_instructions()
        })
        return {"roadmap": roadmap_res.steps}
    except Exception as e:
        logger.log("LangGraph", "pathmaker_error", {"error": str(e)})
        return {"errors": [f"Roadmap generation failed: {str(e)}"]}
