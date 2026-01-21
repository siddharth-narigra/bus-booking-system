"""
Database models (tables) for the Bus Booking System.

Each class here becomes a table in the SQLite database.
SQLAlchemy will automatically create these tables when we run the app.
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.database import Base


class Station(Base):
    """
    Represents a stop on the bus route.
    
    We store all 5 stations: Ahmedabad, Vadodara, Surat, Vapi, Mumbai
    order_index helps us know the sequence (0 = first, 4 = last)
    """
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    order_index = Column(Integer, nullable=False)  # 0=Ahmedabad, 4=Mumbai


class Seat(Base):
    """
    Represents a sleeper berth in the bus.
    
    seat_number: Like "L1" (Lower 1), "U5" (Upper 5)
    deck: "lower" or "upper"
    position: "left" or "right" side of the bus
    price: Base price for this seat
    """
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, index=True)
    seat_number = Column(String(10), nullable=False, unique=True)
    deck = Column(String(10), nullable=False)  # "lower" or "upper"
    position = Column(String(10), nullable=False)  # "left" or "right"
    price = Column(Float, nullable=False, default=800.0)


class Meal(Base):
    """
    Available meal options.
    
    meal_type: "breakfast", "lunch", or "dinner"
    """
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    meal_type = Column(String(20), nullable=False)  # breakfast, lunch, dinner
    price = Column(Float, nullable=False)


class Booking(Base):
    """
    A booking made by a user.
    
    One booking can have multiple seats and meals.
    We generate a unique booking_id for the user to reference.
    """
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(String(20), nullable=False, unique=True, index=True)  # User-facing ID like "BK12345"
    passenger_name = Column(String(200), nullable=False)
    passenger_phone = Column(String(15), nullable=False)
    passenger_email = Column(String(200), nullable=True)
    travel_date = Column(String(10), nullable=False)  # Format: "2026-01-25"
    boarding_station_id = Column(Integer, ForeignKey("stations.id"), nullable=False)
    dropping_station_id = Column(Integer, ForeignKey("stations.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String(20), nullable=False, default="confirmed")  # confirmed, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships - allows us to access related data easily
    boarding_station = relationship("Station", foreign_keys=[boarding_station_id])
    dropping_station = relationship("Station", foreign_keys=[dropping_station_id])
    seats = relationship("BookingSeat", back_populates="booking")
    meals = relationship("BookingMeal", back_populates="booking")


class BookingSeat(Base):
    """
    Links a booking to its seats.
    
    Why a separate table?
    - One booking can have multiple seats (e.g., family booking 3 seats)
    - We need to track which specific seats are booked for which date
    """
    __tablename__ = "booking_seats"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    seat_id = Column(Integer, ForeignKey("seats.id"), nullable=False)

    booking = relationship("Booking", back_populates="seats")
    seat = relationship("Seat")


class BookingMeal(Base):
    """
    Links a booking to selected meals.
    
    Why a separate table?
    - One booking can have multiple meals (breakfast + dinner for a passenger)
    - Each passenger (seat) might have different meal choices
    """
    __tablename__ = "booking_meals"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    meal_id = Column(Integer, ForeignKey("meals.id"), nullable=False)
    seat_id = Column(Integer, ForeignKey("seats.id"), nullable=False)  # Which passenger's meal

    booking = relationship("Booking", back_populates="meals")
    meal = relationship("Meal")
    seat = relationship("Seat")
