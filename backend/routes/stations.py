"""
Stations API routes.

Simple endpoint that returns all stations on the route.
This is static data - the route doesn't change.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend import models, schemas


router = APIRouter()


@router.get("/stations", response_model=List[schemas.StationResponse])
def get_stations(db: Session = Depends(get_db)):
    """
    Get all stations on the Ahmedabad-Mumbai route.
    
    Returns stations in order (Ahmedabad first, Mumbai last).
    
    Why this endpoint?
    - Frontend needs to show the route to user
    - Frontend needs station IDs for booking
    """
    stations = db.query(models.Station).order_by(models.Station.order_index).all()
    return stations
