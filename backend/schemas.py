from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class IncidentBase(BaseModel):
    """Base schema for incident data"""
    incident_type: str = Field(..., description="Type of incident (e.g., collision, pedestrian accident)")
    severity: str = Field(..., description="Severity level (e.g., minor, major, fatal)")
    location: str = Field(..., description="Location description")
    latitude: Optional[float] = Field(None, description="Latitude coordinate")
    longitude: Optional[float] = Field(None, description="Longitude coordinate")
    description: Optional[str] = Field(None, description="Detailed description")
    date_time: datetime = Field(..., description="Date and time of incident")
    casualties: int = Field(default=0, ge=0, description="Number of casualties")
    vehicles_involved: int = Field(default=0, ge=0, description="Number of vehicles involved")
    weather_conditions: Optional[str] = Field(None, description="Weather conditions")
    road_conditions: Optional[str] = Field(None, description="Road conditions")


class IncidentCreate(IncidentBase):
    """Schema for creating a new incident"""
    pass


class IncidentUpdate(BaseModel):
    """Schema for updating an incident"""
    incident_type: Optional[str] = None
    severity: Optional[str] = None
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None
    date_time: Optional[datetime] = None
    casualties: Optional[int] = Field(None, ge=0)
    vehicles_involved: Optional[int] = Field(None, ge=0)
    weather_conditions: Optional[str] = None
    road_conditions: Optional[str] = None


class IncidentResponse(IncidentBase):
    """Schema for incident response"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
