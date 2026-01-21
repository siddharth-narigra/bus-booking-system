"""
Main FastAPI application entry point.

This file:
1. Creates the FastAPI app
2. Initializes the database tables
3. Seeds initial data (stations, seats, meals)
4. Registers all route handlers
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import engine, Base, SessionLocal
from backend import models


def seed_initial_data():
    """
    Populate the database with initial data.
    
    This runs once when the server starts.
    Only adds data if tables are empty (won't duplicate on restart).
    """
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(models.Station).count() > 0:
            return  # Already seeded
        
        # Seed Stations
        # order_index represents the sequence on the route
        stations = [
            models.Station(name="Ahmedabad", order_index=0),
            models.Station(name="Vadodara", order_index=1),
            models.Station(name="Surat", order_index=2),
            models.Station(name="Vapi", order_index=3),
            models.Station(name="Mumbai", order_index=4),
        ]
        db.add_all(stations)
        
        # Seed Seats
        # Typical sleeper bus: 2 columns (left/right), 2 decks (lower/upper)
        # Creating 20 seats total (10 lower, 10 upper)
        seats = []
        seat_num = 1
        for deck in ["lower", "upper"]:
            for position in ["left", "right"]:
                for i in range(5):  # 5 seats per position
                    prefix = "L" if deck == "lower" else "U"
                    seat_number = f"{prefix}{seat_num}"
                    # Upper deck slightly cheaper (common in real buses)
                    price = 800.0 if deck == "lower" else 700.0
                    seats.append(models.Seat(
                        seat_number=seat_number,
                        deck=deck,
                        position=position,
                        price=price
                    ))
                    seat_num += 1
        db.add_all(seats)
        
        # Seed Meals
        meals = [
            # Breakfast options
            models.Meal(name="Poha with Chai", meal_type="breakfast", price=80.0),
            models.Meal(name="Sandwich with Juice", meal_type="breakfast", price=100.0),
            # Lunch options
            models.Meal(name="Veg Thali", meal_type="lunch", price=150.0),
            models.Meal(name="Paneer Rice Bowl", meal_type="lunch", price=120.0),
            # Dinner options
            models.Meal(name="Roti Sabzi", meal_type="dinner", price=130.0),
            models.Meal(name="Dal Rice", meal_type="dinner", price=110.0),
        ]
        db.add_all(meals)
        
        db.commit()
        print("Database seeded successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()


def create_app() -> FastAPI:
    """
    Factory function to create and configure the FastAPI app.
    
    Why a factory function?
    - Allows for different configurations (testing vs production)
    - Clean separation of app creation and running
    """
    
    # Create the FastAPI app with metadata
    app = FastAPI(
        title="Bus Booking System API",
        description="API for sleeper bus ticket booking (Ahmedabad to Mumbai)",
        version="1.0.0"
    )
    
    # Add CORS middleware
    # This allows the frontend (running on a different port) to call our API
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify exact frontend URL
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Create database tables
    # This checks if tables exist and creates them if they don't
    Base.metadata.create_all(bind=engine)
    
    # Seed initial data
    seed_initial_data()
    
    # Import and register routes
    from backend.routes import stations, seats, meals, bookings, predict
    
    app.include_router(stations.router, prefix="/api", tags=["Stations"])
    app.include_router(seats.router, prefix="/api", tags=["Seats"])
    app.include_router(meals.router, prefix="/api", tags=["Meals"])
    app.include_router(bookings.router, prefix="/api", tags=["Bookings"])
    app.include_router(predict.router, prefix="/api", tags=["Prediction"])
    
    @app.get("/")
    def root():
        """Health check endpoint."""
        return {"status": "running", "message": "Bus Booking System API"}
    
    return app


# Create the app instance
app = create_app()
