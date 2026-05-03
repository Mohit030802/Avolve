from fastapi import APIRouter
from app.api.v1.endpoints import example, resume, career, auth

api_router = APIRouter()
api_router.include_router(auth.router, tags=["authentication"])
api_router.include_router(example.router, prefix="/example", tags=["example"])
api_router.include_router(resume.router, prefix="/resume", tags=["resume"])
api_router.include_router(career.router, prefix="/career", tags=["career analysis"])
