from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from datetime import datetime

from backend.database import Base


class RoadIncident(Base):
    """Road incident model for tracking accidents and safety events"""
    
    __tablename__ = "road_incidents"
    
    id = Column(Integer, primary_key=True, index=True)
    incident_type = Column(String(100), nullable=False, index=True)
    severity = Column(String(50), nullable=False, index=True)
    location = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
    date_time = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    casualties = Column(Integer, default=0)
    vehicles_involved = Column(Integer, default=0)
    weather_conditions = Column(String(100), nullable=True)
    road_conditions = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<RoadIncident(id={self.id}, type={self.incident_type}, severity={self.severity})>"
