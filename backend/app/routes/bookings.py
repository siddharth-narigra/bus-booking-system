"""
Bookings API routes.

This is the most complex route file:
- Create booking (POST)
- Get booking details (GET)
- Cancel booking (DELETE)
"""

import random
import string
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, date

from ..database import get_db
from .. import models, schemas


router = APIRouter()


def generate_booking_id() -> str:
    """
    Generate a unique, user-friendly booking ID.
    
    Format: BK + 6 random alphanumeric characters
    Example: BK7X3M9K
    
    Why this format?
    - Easy to communicate verbally
    - Easy to type for cancellation
    - Looks professional
    """
    chars = string.ascii_uppercase + string.digits
    random_part = ''.join(random.choices(chars, k=6))
    return f"BK{random_part}"


@router.post("/bookings", response_model=schemas.BookingResponse)
def create_booking(
    booking_data: schemas.BookingCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new booking.
    
    This endpoint:
    1. Validates the input data
    2. Checks if seats are available
    3. Creates the booking and related records
    4. Returns the complete booking details
    
    Common errors:
    - Seat already booked for this date
    - Invalid station IDs
    - Boarding station after dropping station on the route
    """
    
    # Validate travel date
    try:
        parsed_date = datetime.strptime(booking_data.travel_date, "%Y-%m-%d").date()
        if parsed_date < date.today():
            raise HTTPException(status_code=400, detail="Cannot book for past dates")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    # Validate stations exist and boarding is before dropping
    boarding_station = db.query(models.Station).filter(
        models.Station.id == booking_data.boarding_station_id
    ).first()
    dropping_station = db.query(models.Station).filter(
        models.Station.id == booking_data.dropping_station_id
    ).first()
    
    if not boarding_station or not dropping_station:
        raise HTTPException(status_code=400, detail="Invalid station ID")
    
    if boarding_station.order_index >= dropping_station.order_index:
        raise HTTPException(
            status_code=400, 
            detail="Boarding station must be before dropping station on the route"
        )
    
    # Validate seats exist and are available
    if not booking_data.seat_ids:
        raise HTTPException(status_code=400, detail="At least one seat must be selected")
    
    # Check if any requested seats are already booked
    booked_seat_ids = db.query(models.BookingSeat.seat_id).join(
        models.Booking
    ).filter(
        models.Booking.travel_date == booking_data.travel_date,
        models.Booking.status == "confirmed",
        models.BookingSeat.seat_id.in_(booking_data.seat_ids)
    ).all()
    
    if booked_seat_ids:
        raise HTTPException(
            status_code=400, 
            detail="One or more selected seats are already booked for this date"
        )
    
    # Get seat details for price calculation
    seats = db.query(models.Seat).filter(models.Seat.id.in_(booking_data.seat_ids)).all()
    if len(seats) != len(booking_data.seat_ids):
        raise HTTPException(status_code=400, detail="Invalid seat ID")
    
    # Calculate total amount
    seat_total = sum(seat.price for seat in seats)
    meal_total = 0.0
    
    # Validate meals if provided
    if booking_data.meals:
        meal_ids = [m.meal_id for m in booking_data.meals]
        meals = db.query(models.Meal).filter(models.Meal.id.in_(meal_ids)).all()
        meal_map = {meal.id: meal for meal in meals}
        
        for meal_selection in booking_data.meals:
            if meal_selection.meal_id not in meal_map:
                raise HTTPException(status_code=400, detail="Invalid meal ID")
            if meal_selection.seat_id not in booking_data.seat_ids:
                raise HTTPException(
                    status_code=400, 
                    detail="Meal can only be added for booked seats"
                )
            meal_total += meal_map[meal_selection.meal_id].price
    
    total_amount = seat_total + meal_total
    
    # Generate unique booking ID
    booking_id = generate_booking_id()
    # Ensure uniqueness (very unlikely to collide, but safe)
    while db.query(models.Booking).filter(models.Booking.booking_id == booking_id).first():
        booking_id = generate_booking_id()
    
    # Create the booking
    booking = models.Booking(
        booking_id=booking_id,
        passenger_name=booking_data.passenger_name,
        passenger_phone=booking_data.passenger_phone,
        passenger_email=booking_data.passenger_email,
        travel_date=booking_data.travel_date,
        boarding_station_id=booking_data.boarding_station_id,
        dropping_station_id=booking_data.dropping_station_id,
        total_amount=total_amount,
        status="confirmed"
    )
    db.add(booking)
    db.flush()  # Get the booking ID without committing
    
    # Add seats to booking
    for seat_id in booking_data.seat_ids:
        booking_seat = models.BookingSeat(
            booking_id=booking.id,
            seat_id=seat_id
        )
        db.add(booking_seat)
    
    # Add meals to booking
    if booking_data.meals:
        for meal_selection in booking_data.meals:
            booking_meal = models.BookingMeal(
                booking_id=booking.id,
                meal_id=meal_selection.meal_id,
                seat_id=meal_selection.seat_id
            )
            db.add(booking_meal)
    
    db.commit()
    db.refresh(booking)
    
    # Build response
    seat_details = [
        schemas.BookingSeatDetail(
            seat_number=seat.seat_number,
            deck=seat.deck,
            price=seat.price
        )
        for seat in seats
    ]
    
    meal_details = []
    if booking_data.meals:
        seat_map = {seat.id: seat for seat in seats}
        for meal_selection in booking_data.meals:
            meal = meal_map[meal_selection.meal_id]
            seat = seat_map[meal_selection.seat_id]
            meal_details.append(schemas.BookingMealDetail(
                seat_number=seat.seat_number,
                meal_name=meal.name,
                price=meal.price
            ))
    
    return schemas.BookingResponse(
        id=booking.id,
        booking_id=booking.booking_id,
        passenger_name=booking.passenger_name,
        passenger_phone=booking.passenger_phone,
        passenger_email=booking.passenger_email,
        travel_date=booking.travel_date,
        boarding_station=boarding_station.name,
        dropping_station=dropping_station.name,
        seats=seat_details,
        meals=meal_details,
        total_amount=booking.total_amount,
        status=booking.status,
        created_at=booking.created_at
    )


@router.get("/bookings/{booking_id}", response_model=schemas.BookingResponse)
def get_booking(booking_id: str, db: Session = Depends(get_db)):
    """
    Get booking details by booking ID.
    
    The booking_id is the user-facing ID (like BK7X3M9K),
    not the internal database ID.
    """
    
    booking = db.query(models.Booking).filter(
        models.Booking.booking_id == booking_id.upper()
    ).first()
    
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Get related data
    boarding_station = db.query(models.Station).filter(
        models.Station.id == booking.boarding_station_id
    ).first()
    dropping_station = db.query(models.Station).filter(
        models.Station.id == booking.dropping_station_id
    ).first()
    
    # Get seats
    booking_seats = db.query(models.BookingSeat).filter(
        models.BookingSeat.booking_id == booking.id
    ).all()
    seat_ids = [bs.seat_id for bs in booking_seats]
    seats = db.query(models.Seat).filter(models.Seat.id.in_(seat_ids)).all()
    
    seat_details = [
        schemas.BookingSeatDetail(
            seat_number=seat.seat_number,
            deck=seat.deck,
            price=seat.price
        )
        for seat in seats
    ]
    
    # Get meals
    booking_meals = db.query(models.BookingMeal).filter(
        models.BookingMeal.booking_id == booking.id
    ).all()
    
    meal_details = []
    seat_map = {seat.id: seat for seat in seats}
    for bm in booking_meals:
        meal = db.query(models.Meal).filter(models.Meal.id == bm.meal_id).first()
        seat = seat_map.get(bm.seat_id)
        if meal and seat:
            meal_details.append(schemas.BookingMealDetail(
                seat_number=seat.seat_number,
                meal_name=meal.name,
                price=meal.price
            ))
    
    return schemas.BookingResponse(
        id=booking.id,
        booking_id=booking.booking_id,
        passenger_name=booking.passenger_name,
        passenger_phone=booking.passenger_phone,
        passenger_email=booking.passenger_email,
        travel_date=booking.travel_date,
        boarding_station=boarding_station.name,
        dropping_station=dropping_station.name,
        seats=seat_details,
        meals=meal_details,
        total_amount=booking.total_amount,
        status=booking.status,
        created_at=booking.created_at
    )


@router.delete("/bookings/{booking_id}", response_model=schemas.BookingCancelResponse)
def cancel_booking(booking_id: str, db: Session = Depends(get_db)):
    """
    Cancel a booking.
    
    We don't actually delete the booking - we mark it as cancelled.
    
    Why soft delete?
    - Keeps booking history for analytics
    - Allows for potential undo functionality
    - Required for refund tracking
    
    When cancelled:
    - Status changes to "cancelled"
    - Seats become available again for new bookings
    """
    
    booking = db.query(models.Booking).filter(
        models.Booking.booking_id == booking_id.upper()
    ).first()
    
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    if booking.status == "cancelled":
        raise HTTPException(status_code=400, detail="Booking is already cancelled")
    
    # Update status
    booking.status = "cancelled"
    db.commit()
    
    return schemas.BookingCancelResponse(
        message="Booking cancelled successfully",
        booking_id=booking.booking_id,
        refund_amount=booking.total_amount  # Full refund (simplified)
    )
