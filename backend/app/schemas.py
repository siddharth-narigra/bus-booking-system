"""
Pydantic schemas for request/response validation.

Why separate from models?
- Models = Database structure (what we store)
- Schemas = API structure (what we send/receive)

Pydantic automatically validates incoming data and converts outgoing data.
If someone sends invalid data, FastAPI returns a clear error message.
"""

from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


# ------------------------------
# Station Schemas
# ------------------------------

class StationResponse(BaseModel):
    """Response schema for a station."""
    id: int
    name: str
    order_index: int

    class Config:
        from_attributes = True  # Allows Pydantic to read data from SQLAlchemy models


# ------------------------------
# Seat Schemas
# ------------------------------

class SeatResponse(BaseModel):
    """Response schema for a seat."""
    id: int
    seat_number: str
    deck: str
    position: str
    price: float
    is_available: bool = True  # We'll compute this based on bookings

    class Config:
        from_attributes = True


# ------------------------------
# Meal Schemas
# ------------------------------

class MealResponse(BaseModel):
    """Response schema for a meal option."""
    id: int
    name: str
    meal_type: str
    price: float

    class Config:
        from_attributes = True


# ------------------------------
# Booking Schemas
# ------------------------------

class MealSelection(BaseModel):
    """Schema for selecting a meal for a specific seat."""
    seat_id: int
    meal_id: int


class BookingCreate(BaseModel):
    """
    Schema for creating a new booking.
    
    Note: We don't include booking_id here because the server generates it.
    """
    passenger_name: str
    passenger_phone: str
    passenger_email: Optional[str] = None
    travel_date: str  # Format: "2026-01-25"
    boarding_station_id: int
    dropping_station_id: int
    seat_ids: List[int]  # List of seat IDs being booked
    meals: Optional[List[MealSelection]] = []  # Optional meal selections


class BookingSeatDetail(BaseModel):
    """Seat details within a booking."""
    seat_number: str
    deck: str
    price: float


class BookingMealDetail(BaseModel):
    """Meal details within a booking."""
    seat_number: str
    meal_name: str
    price: float


class BookingResponse(BaseModel):
    """
    Full booking details returned after creation or retrieval.
    
    Includes the generated booking_id that user can use for cancellation.
    """
    id: int
    booking_id: str  # User-facing ID like "BK12345"
    passenger_name: str
    passenger_phone: str
    passenger_email: Optional[str]
    travel_date: str
    boarding_station: str
    dropping_station: str
    seats: List[BookingSeatDetail]
    meals: List[BookingMealDetail]
    total_amount: float
    status: str
    prediction_percentage: Optional[float] = None  # Booking confirmation prediction
    created_at: datetime

    class Config:
        from_attributes = True


class BookingCancelResponse(BaseModel):
    """Response after cancelling a booking."""
    message: str
    booking_id: str
    refund_amount: float


# ------------------------------
# Prediction Schemas
# ------------------------------

class PredictionRequest(BaseModel):
    """Request schema for getting booking confirmation prediction."""
    travel_date: str
    seat_count: int


class PredictionResponse(BaseModel):
    """Response schema for booking confirmation prediction."""
    prediction_percentage: float
    factors: dict  # Breakdown of factors affecting the prediction
