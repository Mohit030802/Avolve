import os
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.parser_service import parser_service
from app.services.llm_service import llm_service
from app.core.logger import logger
from app.core.security import get_current_user
from app.core.database import get_session
from app.models.resume import Resume
from app.models.user import User
from app.schemas.resume_schema import ResumeSchema


router = APIRouter()

@router.post("/upload", response_model=ResumeSchema)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """
    Upload a PDF resume, parse it, and save the structured data to the database.
    Required authentication to ensure the resume is linked to a user.
    """
    logger.log("API.upload_resume", "RECEIVED", {
        "filename": file.filename, 
        "user_id": str(current_user.id)
    })
    
    ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt", ".md", ".html"}
    ext = Path(file.filename).suffix.lower()
    
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}")

    # Create a temporary file to store the upload
    try:
        with NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = Path(tmp.name)
            
        logger.log("API.upload_resume", "SAVED_TEMP", {"path": str(tmp_path)})
        
        # 1. Parse with MCP Server
        markdown_text = await parser_service.parse_document(tmp_path)
        
        # 2. Extract with LLM (Gemini)
        structured_data = llm_service.extract_structured_data(markdown_text)
        
        # 3. Persist to Database
        db_resume = Resume(
            filename=file.filename,
            raw_markdown=markdown_text,
            structured_data=structured_data.model_dump(),
            user_id=str(current_user.id)
        )
        
        db.add(db_resume)
        await db.commit()
        await db.refresh(db_resume)
        
        logger.log("API.upload_resume", "SUCCESS", {
            "name": structured_data.name,
            "db_id": str(db_resume.id)
        })
        
        return structured_data

    except Exception as e:
        logger.log("API.upload_resume", "ERROR", {"error": str(e)})
        # Rollback in case of DB error
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Cleanup
        if 'tmp_path' in locals() and tmp_path.exists():
            os.remove(tmp_path)
            logger.log("API.upload_resume", "CLEANED_TEMP", {"path": str(tmp_path)})
