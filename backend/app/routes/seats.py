"""
Seats API routes.

Returns seat layout with availability status.
This is more complex because availability depends on existing bookings for a specific date.
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, date

from ..database import get_db
from .. import models, schemas


router = APIRouter()


@router.get("/seats", response_model=List[schemas.SeatResponse])
def get_seats(
    travel_date: str = Query(..., description="Travel date in YYYY-MM-DD format"),
    db: Session = Depends(get_db)
):
    """
    Get all seats with availability status for a specific date.
    
    Why pass travel_date?
    - A seat might be booked on one date but available on another
    - We need to check existing bookings for the requested date
    
    Returns:
    - All seats with their details
    - is_available: True if seat can be booked for this date
    """
    
    # Validate date format and check it's not in the past
    try:
        parsed_date = datetime.strptime(travel_date, "%Y-%m-%d").date()
        if parsed_date < date.today():
            raise HTTPException(
                status_code=400, 
                detail="Cannot check seats for past dates"
            )
    except ValueError:
        raise HTTPException(
            status_code=400, 
            detail="Invalid date format. Use YYYY-MM-DD"
        )
    
    # Get all seats
    all_seats = db.query(models.Seat).order_by(models.Seat.seat_number).all()
    
    # Find which seats are booked for this date
    # A seat is booked if it's in a confirmed booking for this date
    booked_seat_ids = db.query(models.BookingSeat.seat_id).join(
        models.Booking
    ).filter(
        models.Booking.travel_date == travel_date,
        models.Booking.status == "confirmed"
    ).all()
    
    # Convert to set for O(1) lookup
    booked_seat_ids = {seat_id[0] for seat_id in booked_seat_ids}
    
    # Build response with availability
    result = []
    for seat in all_seats:
        seat_response = schemas.SeatResponse(
            id=seat.id,
            seat_number=seat.seat_number,
            deck=seat.deck,
            position=seat.position,
            price=seat.price,
            is_available=seat.id not in booked_seat_ids
        )
        result.append(seat_response)
    
    return result
