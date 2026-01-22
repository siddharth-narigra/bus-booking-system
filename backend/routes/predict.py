"""
Prediction API route.

This implements the "Booking Confirmation Prediction" feature using
a trained Logistic Regression model.

Evolution:
- V1: Rule-based scoring (hardcoded weights)
- V2: Logistic Regression trained on synthetic data (current)
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, date
import pickle
import numpy as np
import os

from backend.database import get_db
from backend import models, schemas


router = APIRouter()

# Load the trained model at startup
_model_bundle = None

def get_model():
    """Load model once and cache it."""
    global _model_bundle
    if _model_bundle is None:
        # Try multiple possible paths
        possible_paths = [
            os.path.join(os.path.dirname(__file__), '..', '..', 'models', 'prediction_model.pkl'),
            os.path.join('models', 'prediction_model.pkl'),
            'models/prediction_model.pkl'
        ]
        
        for path in possible_paths:
            try:
                with open(path, 'rb') as f:
                    _model_bundle = pickle.load(f)
                    break
            except FileNotFoundError:
                continue
    return _model_bundle


def calculate_prediction_ml(
    travel_date: str,
    seat_count: int,
    meal_selected: bool = False,
    seat_type: str = 'lower'
) -> tuple[float, dict]:
    """
    Calculate booking confirmation prediction using Logistic Regression.
    
    Features used:
    - seat_type: 0 = upper, 1 = lower
    - meal_selected: 0 = no, 1 = yes
    - booking_lead_days: days until travel
    - day_of_week: 0-6 (Mon-Sun)
    - num_seats: number of seats booked
    
    Returns:
    - prediction_percentage: 0-100 float
    - factors: explanation of input features
    """
    
    # Parse travel date
    try:
        parsed_date = datetime.strptime(travel_date, "%Y-%m-%d").date()
    except ValueError:
        return 70.0, {"error": "Invalid date format"}
    
    # Calculate features
    booking_lead_days = max(0, (parsed_date - date.today()).days)
    day_of_week = parsed_date.weekday()
    seat_type_encoded = 1 if seat_type == "lower" else 0
    meal_encoded = 1 if meal_selected else 0
    
    factors = {
        "seat_type": {"value": seat_type, "encoded": seat_type_encoded},
        "meal_selected": {"value": meal_selected, "encoded": meal_encoded},
        "booking_lead_days": {"value": booking_lead_days},
        "day_of_week": {"value": parsed_date.strftime("%A"), "encoded": day_of_week},
        "num_seats": {"value": seat_count}
    }
    
    # Get model
    bundle = get_model()
    
    if bundle is None:
        # Fallback to simple rule-based if model not available
        base = 75.0
        prediction = base + (booking_lead_days * 0.5) + (meal_encoded * 5) - ((seat_count - 1) * 2)
        if day_of_week in [4, 5, 6]:  # Weekend
            prediction += 5
        prediction = max(0, min(100, prediction))
        factors["model"] = "rule-based (fallback)"
        return round(prediction, 1), factors
    
    # Make prediction with ML model
    model = bundle['model']
    scaler = bundle['scaler']
    
    features = np.array([[seat_type_encoded, meal_encoded, booking_lead_days, day_of_week, seat_count]])
    features_scaled = scaler.transform(features)
    
    # Get probability of confirmation (class 1)
    probability = model.predict_proba(features_scaled)[0][1]
    prediction = round(probability * 100, 1)
    
    factors["model"] = "logistic_regression"
    
    return prediction, factors


@router.post("/predict", response_model=schemas.PredictionResponse)
def get_prediction(
    request: schemas.PredictionRequest,
    db: Session = Depends(get_db)
):
    """
    Get booking confirmation prediction using trained ML model.
    
    This endpoint uses a Logistic Regression model trained on
    synthetic booking data to predict confirmation likelihood.
    """
    
    prediction, factors = calculate_prediction_ml(
        travel_date=request.travel_date,
        seat_count=request.seat_count,
        meal_selected=getattr(request, 'meal_selected', False),
        seat_type=getattr(request, 'seat_type', 'lower')
    )
    
    return schemas.PredictionResponse(
        prediction_percentage=prediction,
        factors=factors
    )
