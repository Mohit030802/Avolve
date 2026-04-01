from typing import List, Optional
from pydantic import BaseModel, Field

class Experience(BaseModel):
    company: str = Field(..., description="Name of the company")
    position: str = Field(..., description="Job title/position")
    duration: str = Field(..., description="Duration of employment (e.g., Jan 2020 - Dec 2022)")
    responsibilities: List[str] = Field(default_factory=list, description="Key responsibilities or achievements")

class Education(BaseModel):
    institution: str = Field(..., description="Name of the university/college")
    degree: str = Field(..., description="Degree obtained")
    year: str = Field(..., description="Year of graduation")

class ResumeSchema(BaseModel):
    name: str = Field(..., description="Full name of the candidate")
    email: str = Field(..., description="Email address")
    skills: List[str] = Field(default_factory=list, description="List of technical and soft skills")
    experience: List[Experience] = Field(default_factory=list, description="Work experience history")
    education: List[Education] = Field(default_factory=list, description="Educational background")
