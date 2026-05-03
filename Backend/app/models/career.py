import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import JSONB

class CareerAnalysis(SQLModel, table=True):
    """
    Database model for storing career gap analysis and roadmaps.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    resume_id: uuid.UUID = Field(index=True, foreign_key="resume.id")
    user_id: str = Field(index=True)
    
    target_role: str
    duration_weeks: int
    
    # Store the complex structured data as a JSONB column
    analysis_data: Dict[str, Any] = Field(
        default_factory=dict, 
        sa_column=Column(JSONB)
    )
    
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=lambda: datetime.now(timezone.utc)
    )
