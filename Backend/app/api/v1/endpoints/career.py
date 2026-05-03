import uuid
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.database import get_session
from app.core.security import get_current_user
from app.core.logger import logger
from app.models.resume import Resume
from app.models.career import CareerAnalysis
from app.schemas.career_schema import CareerAnalysisRequest, CareerAnalysisResponse
from app.agents.graph import career_agent_graph

router = APIRouter()

@router.post("/analyze/{resume_id}", response_model=CareerAnalysisResponse)
async def analyze_career_gap(
    resume_id: uuid.UUID,
    request: CareerAnalysisRequest = None,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """
    Run the LangGraph agentic workflow to analyze gaps and generate a roadmap.
    """
    if request is None:
        request = CareerAnalysisRequest()
        
    logger.log("API.analyze_career_gap", "START", {"resume_id": str(resume_id), "target_role": request.target_role})
    
    # 1. Fetch the resume from the DB
    statement = select(Resume).where(Resume.id == resume_id)
    result = await db.execute(statement)
    resume = result.scalar_one_or_none()
    
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
        
    # Ensure the user owns this resume
    if resume.user_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to access this resume")
        
    # 2. Prepare the initial state for LangGraph
    initial_state = {
        "resume_text": resume.raw_markdown,
        "parsed_resume_data": resume.structured_data,
        "target_role": request.target_role,
        "duration_weeks": request.duration_weeks,
        "inferred_role": None,
        "gap_analysis": None,
        "roadmap": None,
        "messages": [],
        "errors": []
    }
    
    # 3. Execute the Graph
    try:
        final_state = career_agent_graph.invoke(initial_state)
        
        if final_state.get("errors"):
            logger.log("API.analyze_career_gap", "GRAPH_ERRORS", {"errors": final_state["errors"]})
            raise HTTPException(status_code=500, detail=f"Analysis encountered errors: {final_state['errors']}")
            
        role_targeted = final_state.get("inferred_role") or final_state.get("target_role")
        
        # 4. Save to Database
        db_career_analysis = CareerAnalysis(
            resume_id=resume.id,
            user_id=current_user["id"],
            target_role=role_targeted,
            duration_weeks=final_state["duration_weeks"],
            analysis_data={
                "gap_analysis": final_state["gap_analysis"].model_dump(),
                "roadmap": [step.model_dump() for step in final_state["roadmap"]]
            }
        )
        
        db.add(db_career_analysis)
        await db.commit()
        await db.refresh(db_career_analysis)
        
        # 5. Return Response
        return CareerAnalysisResponse(
            target_role=role_targeted,
            duration_weeks=final_state["duration_weeks"],
            gap_analysis=final_state["gap_analysis"],
            roadmap=final_state["roadmap"]
        )
        
    except Exception as e:
        logger.log("API.analyze_career_gap", "ERROR", {"error": str(e)})
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
