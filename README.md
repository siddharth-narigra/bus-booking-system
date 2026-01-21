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

Optionally add meals (breakfast/lunch/dinner) during the checkout process.

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

[View Detailed Test Cases](docs/TEST_CASES.md)

---

## UI/UX Prototype

<!-- TODO: Add Figma prototype link -->

**Prototype Link:** [Coming Soon]()

---

## Tech Stack

- **Backend:** Python
- **Database:** (To be decided)
- **Design:** Figma

---

## Project Structure

```
bus-booking-system/
├── README.md
├── docs/
│   ├── TEST_CASES.md
│   └── PREDICTION_APPROACH.md
├── backend/
│   └── (API source code)
└── .gitignore
```

---

## Setup & Installation

*(Instructions will be added after backend development)*

---

## Documentation

- [Test Cases](docs/TEST_CASES.md)
- [Prediction Approach](docs/PREDICTION_APPROACH.md) *(Coming Soon)*

---

## Author
