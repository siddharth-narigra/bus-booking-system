# Sleeper Bus Booking System

A web-based sleeper bus ticket booking system for the **Ahmedabad to Mumbai** route with integrated meal booking service.

---

## Project Overview

This system allows users to book sleeper bus tickets from Ahmedabad to Mumbai with intermediate stops at Vadodara, Surat, and Vapi. The unique feature includes meal booking as part of the checkout process and a booking confirmation prediction powered by historical data analysis.

### Route Map

```
Ahmedabad → Vadodara → Surat → Vapi → Mumbai
```

---

## Features

### 1. Route & Date Selection

Select travel date and view the complete bus route with all intermediate stops.

### 2. Seat Availability View

View the sleeper bus seat layout with clear distinction between available and booked seats.

### 3. Seat Selection

Select one or more available sleeper seats for booking.

### 4. Meal Booking

Optionally add meals (breakfast/lunch/dinner) during the checkout process. Meals are charged per passenger.

### 5. Booking Summary

Review complete booking details including seats, meals, fare, and journey information before confirmation.

### 6. Booking Confirmation

Receive booking confirmation with a unique booking ID and ticket details.

### 7. Booking Cancellation

Cancel existing bookings using the booking ID, which frees up seats for other users.

### 8. Booking Confirmation Prediction *(AI Feature)*

View a prediction percentage indicating the likelihood of booking confirmation based on historical patterns.

---

## Test Cases

Comprehensive test cases covering functional, edge, and UI/UX scenarios.

| Category        | Count        |
| --------------- | ------------ |
| Functional      | 10           |
| Edge Cases      | 6            |
| UI/UX           | 4            |
| **Total** | **20** |

📄 [View Detailed Test Cases](docs/TEST_CASES.md)

---

## Tech Stack

- **Backend:** Python (FastAPI)
- **Database:** SQLite with SQLAlchemy ORM
- **Frontend:** HTML, CSS, JavaScript
- **API Docs:** Swagger UI (auto-generated)

---

## Project Structure

```
bus-booking-system/
├── README.md
├── requirements.txt
├── docs/
│   ├── TEST_CASES.md
│   └── PREDICTION_APPROACH.md
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── routes/
│       ├── stations.py
│       ├── seats.py
│       ├── meals.py
│       ├── bookings.py
│       └── predict.py
└── frontend/
    └── index.html
```

---

## Setup & Installation

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/siddharth-narigra/bus-booking-system.git
cd bus-booking-system

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run backend server
python -m uvicorn backend.main:app --reload --port 8000

# In another terminal, serve frontend
cd frontend
python -m http.server 3000
```

### Access

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/stations | List all stations |
| GET | /api/seats | Get seats with availability |
| GET | /api/meals | List meal options |
| POST | /api/bookings | Create booking |
| GET | /api/bookings/{id} | Get booking details |
| DELETE | /api/bookings/{id} | Cancel booking |
| POST | /api/predict | Get confirmation prediction |

---

## Documentation

- 📄 [Test Cases](docs/TEST_CASES.md)
- 📄 [Prediction Approach](docs/PREDICTION_APPROACH.md)

---

## Author

Siddharth Narigra
