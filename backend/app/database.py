"""
Database connection setup for SQLite using SQLAlchemy.

Why SQLAlchemy?
- ORM: Work with Python objects instead of raw SQL queries
- Database agnostic: Can switch from SQLite to PostgreSQL without code changes
- Built-in connection pooling and session management
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database file will be created in the backend folder
# "check_same_thread=False" is needed for SQLite to work with FastAPI's async nature
SQLALCHEMY_DATABASE_URL = "sqlite:///./bus_booking.db"

# Engine: The starting point for any SQLAlchemy application
# It maintains a pool of connections to the database
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Only needed for SQLite
)

# SessionLocal: A factory for creating database sessions
# Each request will get its own session, then close it when done
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: All our database models will inherit from this
# It keeps track of all tables and their relationships
Base = declarative_base()


def get_db():
    """
    Dependency function for FastAPI.
    
    Creates a new database session for each request,
    and automatically closes it when the request is done.
    
    Usage in routes:
        @app.get("/example")
        def example(db: Session = Depends(get_db)):
            # use db here
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
