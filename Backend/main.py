import os
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.api.v1.api import api_router
from app.core.config import settings
from app.core.security import create_access_token
from app.core.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for application lifespan events.
    """
    # 1. Initialize database tables
    await init_db()
    
    yield
    # Cleanup logic (if any) goes here

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Set Hugging Face environment variables for Docling
if settings.hf_token:
    os.environ["HF_TOKEN"] = settings.hf_token
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = settings.hf_hub_disable_symlinks_warning

# Mock login for demonstration
@app.post(f"{settings.API_V1_STR}/login/access-token")
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Mock login to get access token.
    Default: admin/admin
    """
    if form_data.username == "admin" and form_data.password == "admin":
        access_token = create_access_token(subject=form_data.username)
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

# Main router inclusion
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    # This allows running the app as a debugger application
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
