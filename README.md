# Sleeper Bus Booking System

A web-based sleeper bus ticket booking system for the **Ahmedabad to Mumbai** route with integrated meal booking service and ML-powered booking confirmation prediction.

---

## Project Overview

This system allows users to book sleeper bus tickets from Ahmedabad to Mumbai with intermediate stops at Vadodara, Surat, and Vapi. The unique feature includes meal booking as part of the checkout process and a booking confirmation prediction powered by a trained Logistic Regression model.

### Route Map

```
Ahmedabad → Vadodara → Surat → Vapi → Mumbai
```

---

## Live Demo

- **Frontend:** https://bus-booking-system-siddharth.vercel.app
- **Backend API:** https://bus-booking-system-yqmk.onrender.com
- **API Docs (Swagger):** https://bus-booking-system-yqmk.onrender.com/docs

> Note: The backend is hosted on an on-demand service. The first request after inactivity may take up to 30 seconds due to cold start.

---

## AI / ML Feature - Booking Confirmation Prediction

The system predicts the probability that a booking will be successfully confirmed vs cancelled.

### Problem Framing

This is modeled as a **binary classification problem**:

- `1` → Booking confirmed
- `0` → Booking cancelled

### Approach

- Started with a **rule-based scoring system**
- Improved to a **Logistic Regression model**
- Trained on **synthetic data** due to lack of real historical data
- Focused on **interpretability and practicality**

### Key Input Features

| Feature           | Description            |
| ----------------- | ---------------------- |
| Seat type         | Upper or lower deck    |
| Meal selected     | Whether meal was added |
| Booking lead days | Days before travel     |
| Day of week       | Weekend vs weekday     |
| Number of seats   | 1-4 seats              |

### Data & Model Notes

- Real historical booking data was not available, so a synthetic dataset was generated to simulate realistic booking behavior.
- Synthetic data was used to validate feature influence and ML pipeline behavior in the absence of production data.
- The model predicts the probability of a booking being confirmed (not seat availability).
- Logistic Regression was selected for its interpretability and low data requirements.
- Feature coefficients are used to explain which factors increase or decrease confirmation likelihood.
- The goal is to demonstrate the end-to-end ML pipeline and decision reasoning rather than optimize for production accuracy.

Full details: [docs/PREDICTION_APPROACH.md](docs/PREDICTION_APPROACH.md)

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

---

## Test Cases

Comprehensive test cases covering functional, edge, and UI/UX scenarios.

| Category        | Count        |
| --------------- | ------------ |
| Functional      | 10           |
| Edge Cases      | 6            |
| UI/UX           | 4            |
| **Total** | **20** |

[View Detailed Test Cases](docs/TEST_CASES.md)

---

## UI/UX Prototype

[View Figma Prototype](https://www.figma.com/design/b1BQhDbkjAtLGCNiZY7fBc/Sleeper-Bus-Booking-%E2%80%93-Ahmedabad-to-Mumbai?node-id=0-1&t=aQJ8rKXC1KhAoh2R-1)

---

## Tech Stack

- **Backend:** Python (FastAPI)
- **Database:** SQLite with SQLAlchemy ORM
- **Frontend:** HTML, CSS, JavaScript
- **ML:** scikit-learn (Logistic Regression)
- **API Docs:** Swagger UI (auto-generated)

---

## Project Structure

```
bus-booking-system/
├── README.md
├── requirements.txt
├── data/
│   └── booking_data.csv          # Synthetic training data
├── models/
│   └── prediction_model.pkl      # Trained model
├── docs/
│   ├── TEST_CASES.md
│   └── PREDICTION_APPROACH.md
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── generate_dataset.py       # Data generation script
│   ├── train_model.py            # Model training script
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

| Method | Endpoint           | Description                 |
| ------ | ------------------ | --------------------------- |
| GET    | /api/stations      | List all stations           |
| GET    | /api/seats         | Get seats with availability |
| GET    | /api/meals         | List meal options           |
| POST   | /api/bookings      | Create booking              |
| GET    | /api/bookings/{id} | Get booking details         |
| DELETE | /api/bookings/{id} | Cancel booking              |
| POST   | /api/predict       | Get confirmation prediction |

---

## Documentation

- [Test Cases](docs/TEST_CASES.md)
- [Prediction Approach](docs/PREDICTION_APPROACH.md)

---

## Author

Siddharth Narigra
