from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from backend.database import get_db
from backend.models import RoadIncident
from backend.schemas import IncidentCreate, IncidentUpdate, IncidentResponse

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/incidents", response_model=IncidentResponse, status_code=status.HTTP_201_CREATED)
def create_incident(incident: IncidentCreate, db: Session = Depends(get_db)):
    """Create a new road incident"""
    try:
        db_incident = RoadIncident(**incident.model_dump())
        db.add(db_incident)
        db.commit()
        db.refresh(db_incident)
        logger.info(f"Created incident with ID: {db_incident.id}")
        return db_incident
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating incident: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create incident"
        )


@router.get("/incidents", response_model=List[IncidentResponse])
def get_incidents(
    skip: int = 0,
    limit: int = 100,
    severity: str = None,
    incident_type: str = None,
    db: Session = Depends(get_db)
):
    """Get all road incidents with optional filtering"""
    try:
        query = db.query(RoadIncident)
        
        if severity:
            query = query.filter(RoadIncident.severity == severity)
        if incident_type:
            query = query.filter(RoadIncident.incident_type == incident_type)
        
        incidents = query.offset(skip).limit(limit).all()
        return incidents
    except Exception as e:
        logger.error(f"Error fetching incidents: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch incidents"
        )


@router.get("/incidents/{incident_id}", response_model=IncidentResponse)
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    """Get a specific road incident by ID"""
    incident = db.query(RoadIncident).filter(RoadIncident.id == incident_id).first()
    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incident with ID {incident_id} not found"
        )
    return incident


@router.put("/incidents/{incident_id}", response_model=IncidentResponse)
def update_incident(
    incident_id: int,
    incident_update: IncidentUpdate,
    db: Session = Depends(get_db)
):
    """Update a road incident"""
    db_incident = db.query(RoadIncident).filter(RoadIncident.id == incident_id).first()
    if not db_incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incident with ID {incident_id} not found"
        )
    
    try:
        update_data = incident_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_incident, field, value)
        
        db.commit()
        db.refresh(db_incident)
        logger.info(f"Updated incident with ID: {incident_id}")
        return db_incident
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating incident: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update incident"
        )


@router.delete("/incidents/{incident_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_incident(incident_id: int, db: Session = Depends(get_db)):
    """Delete a road incident"""
    db_incident = db.query(RoadIncident).filter(RoadIncident.id == incident_id).first()
    if not db_incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incident with ID {incident_id} not found"
        )
    
    try:
        db.delete(db_incident)
        db.commit()
        logger.info(f"Deleted incident with ID: {incident_id}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting incident: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete incident"
        )
