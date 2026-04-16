import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import JSONB

class Resume(SQLModel, table=True):
    """
    Database model for storing processed resumes.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    filename: str
    raw_markdown: str
    
    # Store the structured JSON as a PostgreSQL JSONB column
    structured_data: Dict[str, Any] = Field(
        default_factory=dict, 
        sa_column=Column(JSONB)
    )
    
    # Associate with the user who uploaded it
    user_id: str = Field(index=True)
    
    # Metadata
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Config:
        arbitrary_types_allowed = True
