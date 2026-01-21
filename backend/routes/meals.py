"""
Meals API routes.

Returns available meal options for booking.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend import models, schemas


router = APIRouter()


@router.get("/meals", response_model=List[schemas.MealResponse])
def get_meals(db: Session = Depends(get_db)):
    """
    Get all available meal options.
    
    Returns meals grouped by type (breakfast, lunch, dinner).
    
    Why this endpoint?
    - Frontend needs to show meal options during booking
    - Prices and IDs are needed for the booking request
    """
    meals = db.query(models.Meal).order_by(models.Meal.meal_type, models.Meal.price).all()
    return meals
