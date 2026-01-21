# Test Cases - Sleeper Bus Booking System

This document contains all test cases for the Ahmedabad to Mumbai sleeper bus booking system.

---

## Feature 1: Route & Date Selection

| ID | Type | Test Case | Expected Result |
|----|------|-----------|-----------------|
| TC-01 | Functional | User selects a valid future travel date | System displays the Ahmedabad–Mumbai route with intermediate stops (Vadodara, Surat, Vapi) |
| TC-02 | Edge | User attempts to select a past date or past time | System prevents selection and shows appropriate error message |
| TC-03 | UI/UX | No date is selected | "Continue" button remains disabled |

---

## Feature 2: Seat Availability View

| ID | Type | Test Case | Expected Result |
|----|------|-----------|-----------------|
| TC-04 | Functional | User opens the seat layout page | Available and booked seats are clearly visible |
| TC-05 | UI/UX | Viewing seat layout | Booked seats are visually distinct (greyed out/disabled) from available seats |

---

## Feature 3: Seat Selection

| ID | Type | Test Case | Expected Result |
|----|------|-----------|-----------------|
| TC-06 | Functional | User clicks on an available seat | Seat is marked as selected with visual feedback |
| TC-07 | Edge | User attempts to select an already booked seat | System prevents selection |
| TC-08 | UI/UX | No seat is selected | User cannot proceed to checkout |

---

## Feature 4: Meal Booking

| ID | Type | Test Case | Expected Result |
|----|------|-----------|-----------------|
| TC-09 | Functional | User selects a meal option | Meal is added to booking summary with charges |
| TC-10 | Edge | User skips meal selection | Booking proceeds successfully without meal |

---

## Feature 5: Booking Summary & Confirmation

| ID | Type | Test Case | Expected Result |
|----|------|-----------|-----------------|
| TC-11 | Functional | User reaches summary page | All details (seats, meals, fare, journey info) are displayed correctly |
| TC-12 | UI/UX | User clicks "Back" from summary | Previously selected seats and meals remain selected |

---

## Feature 6: Booking Confirmation & Ticket

| ID | Type | Test Case | Expected Result |
|----|------|-----------|-----------------|
| TC-13 | Functional | Booking is successful | System generates booking ID and displays confirmation details |
| TC-14 | Edge | Booking fails (seat became unavailable) | System shows clear error message |

---

## Feature 7: Booking Cancellation

| ID | Type | Test Case | Expected Result |
|----|------|-----------|-----------------|
| TC-15 | Functional | User enters valid booking ID and cancels | Booking is cancelled successfully |
| TC-16 | Edge | User enters invalid booking ID | System shows error message |
| TC-17 | Functional | Booking is cancelled | Seat becomes available for new bookings |

---

## Feature 8: Booking Confirmation Prediction

| ID | Type | Test Case | Expected Result |
|----|------|-----------|-----------------|
| TC-18 | Functional | User reaches booking summary | System displays booking confirmation probability (%) |
| TC-19 | Edge | Historical data is unavailable | System shows default prediction value |
| TC-20 | UI/UX | Viewing prediction | Percentage is clearly visible and easy to understand |

---

## Test Case Summary

| Category | Count |
|----------|-------|
| Functional | 10 |
| Edge Cases | 6 |
| UI/UX | 4 |
| **Total** | **20** |
