"""
Prediction API route.

This implements the "Booking Confirmation Prediction" feature.
It's a mock/simulated prediction based on logical factors.

Why mock and not real ML?
- We don't have real historical data
- Assignment allows "mock or simulated model"
- This demonstrates the thinking process which is what matters
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta

from ..database import get_db
from .. import models, schemas


router = APIRouter()


def calculate_prediction(
    travel_date: str,
    seat_count: int,
    db: Session
) -> tuple[float, dict]:
    """
    Calculate booking confirmation prediction.
    
    Factors considered:
    1. Days until travel (more days = higher confirmation chance)
    2. Seat occupancy for that date (higher demand = higher confirmation)
    3. Day of week (weekends have higher demand)
    4. Number of seats being booked (more seats = slightly lower as group bookings sometimes cancel)
    
    Returns:
    - prediction_percentage: 0-100 float
    - factors: breakdown of how each factor contributed
    """
    
    base_score = 75.0  # Start with 75% base confirmation rate
    factors = {}
    
    # Parse travel date
    try:
        parsed_date = datetime.strptime(travel_date, "%Y-%m-%d").date()
    except ValueError:
        return 70.0, {"error": "Invalid date format"}
    
    # Factor 1: Days until travel
    # Bookings made further in advance are more likely to be confirmed
    days_until_travel = (parsed_date - date.today()).days
    
    if days_until_travel < 0:
        days_factor = -50.0  # Past date, very low
    elif days_until_travel == 0:
        days_factor = -10.0  # Same day, lower
    elif days_until_travel <= 2:
        days_factor = -5.0   # Very close, slightly lower
    elif days_until_travel <= 7:
        days_factor = 5.0    # Within a week, good
    elif days_until_travel <= 14:
        days_factor = 10.0   # Two weeks, better
    else:
        days_factor = 15.0   # More than 2 weeks, excellent
    
    factors["days_until_travel"] = {
        "days": days_until_travel,
        "impact": days_factor,
        "reasoning": "Advance bookings have higher confirmation rates"
    }
    
    # Factor 2: Current seat occupancy for that date
    # Higher occupancy = popular route = higher confirmation
    total_seats = db.query(models.Seat).count()
    booked_seats = db.query(models.BookingSeat).join(
        models.Booking
    ).filter(
        models.Booking.travel_date == travel_date,
        models.Booking.status == "confirmed"
    ).count()
    
    occupancy_rate = (booked_seats / total_seats * 100) if total_seats > 0 else 0
    
    if occupancy_rate >= 80:
        occupancy_factor = 12.0  # High demand
    elif occupancy_rate >= 50:
        occupancy_factor = 8.0   # Moderate demand
    elif occupancy_rate >= 25:
        occupancy_factor = 5.0   # Low-moderate demand
    else:
        occupancy_factor = 0.0   # Low demand, neutral
    
    factors["seat_occupancy"] = {
        "current_occupancy_percent": round(occupancy_rate, 1),
        "impact": occupancy_factor,
        "reasoning": "Higher demand correlates with committed travelers"
    }
    
    # Factor 3: Day of week
    # Weekend travel has higher confirmation (definite plans)
    day_of_week = parsed_date.weekday()
    day_name = parsed_date.strftime("%A")
    
    if day_of_week in [4, 5, 6]:  # Friday, Saturday, Sunday
        day_factor = 5.0
    elif day_of_week == 0:  # Monday
        day_factor = 3.0
    else:
        day_factor = 0.0
    
    factors["day_of_week"] = {
        "day": day_name,
        "impact": day_factor,
        "reasoning": "Weekend/Monday travel shows confirmed intent"
    }
    
    # Factor 4: Number of seats
    # Single travelers more likely to confirm than groups
    if seat_count == 1:
        seat_count_factor = 3.0
    elif seat_count == 2:
        seat_count_factor = 2.0
    elif seat_count <= 4:
        seat_count_factor = 0.0
    else:
        seat_count_factor = -3.0  # Large groups sometimes cancel
    
    factors["seat_count"] = {
        "seats": seat_count,
        "impact": seat_count_factor,
        "reasoning": "Smaller bookings have higher confirmation rates"
    }
    
    # Calculate final prediction
    total_adjustment = days_factor + occupancy_factor + day_factor + seat_count_factor
    prediction = base_score + total_adjustment
    
    # Clamp between 0 and 100
    prediction = max(0, min(100, prediction))
    
    return round(prediction, 1), factors


@router.post("/predict", response_model=schemas.PredictionResponse)
def get_prediction(
    request: schemas.PredictionRequest,
    db: Session = Depends(get_db)
):
    """
    Get booking confirmation prediction.
    
    This endpoint is called during the booking summary step
    to show users how likely their booking is to be confirmed.
    
    Note: This is a mock prediction for demonstration.
    In production, this would use a trained ML model with real historical data.
    """
    
    prediction, factors = calculate_prediction(
        travel_date=request.travel_date,
        seat_count=request.seat_count,
        db=db
    )
    
    return schemas.PredictionResponse(
        prediction_percentage=prediction,
        factors=factors
    )
