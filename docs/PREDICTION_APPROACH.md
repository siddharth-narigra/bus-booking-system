## Prediction Approach

### Method: Rule-Based Scoring Model

We use a weighted scoring system based on factors that historically correlate with booking confirmation rates.

**Why Rule-Based instead of Machine Learning?**

| Approach   | Pros                                                | Cons                           |
| ---------- | --------------------------------------------------- | ------------------------------ |
| Rule-Based | Explainable, no training data needed, deterministic | Less adaptive                  |
| ML Model   | Learns from data, potentially more accurate         | Needs large dataset, black box |

For this demo, rule-based is appropriate because:

1. We don't have real historical booking data
2. The logic is transparent and explainable
3. It demonstrates the concept effectively

---

## Factors Considered

### Factor 1: Days Until Travel

| Days      | Impact | Reasoning                        |
| --------- | ------ | -------------------------------- |
| Past date | -50%   | Invalid booking                  |
| Same day  | -10%   | Last-minute, less committed      |
| 1-2 days  | -5%    | Very short notice                |
| 3-7 days  | +5%    | Planned trip                     |
| 8-14 days | +10%   | Well-planned                     |
| >14 days  | +15%   | Advance booking, high commitment |

### Factor 2: Current Seat Occupancy

| Occupancy | Impact | Reasoning                        |
| --------- | ------ | -------------------------------- |
| <25%      | 0%     | Low demand, neutral              |
| 25-50%    | +5%    | Moderate demand                  |
| 50-80%    | +8%    | Good demand                      |
| >80%      | +12%   | High demand, committed travelers |

### Factor 3: Day of Week

| Day                      | Impact | Reasoning                  |
| ------------------------ | ------ | -------------------------- |
| Friday, Saturday, Sunday | +5%    | Weekend travel, firm plans |
| Monday                   | +3%    | Start of week travel       |
| Tuesday-Thursday         | 0%     | Neutral                    |

### Factor 4: Number of Seats Booked

| Seats     | Impact | Reasoning                      |
| --------- | ------ | ------------------------------ |
| 1 seat    | +3%    | Solo traveler, high commitment |
| 2 seats   | +2%    | Couples, good commitment       |
| 3-4 seats | 0%     | Small group, neutral           |
| 5+ seats  | -3%    | Large groups sometimes cancel  |

---

## Calculation Formula

```
Base Score = 75%

Final Score = Base Score 
            + Days Factor 
            + Occupancy Factor 
            + Day of Week Factor 
            + Seat Count Factor

Final Score = clamp(Final Score, 0, 100)
```

---

## Mock Training Dataset

Below is a simulated historical dataset that represents the patterns our model is based on:

| Booking ID | Days Advance | Day of Week | Seats | Occupancy | Confirmed |
| ---------- | ------------ | ----------- | ----- | --------- | --------- |
| BK001      | 15           | Saturday    | 2     | 75%       | Yes       |
| BK002      | 3            | Tuesday     | 1     | 40%       | Yes       |
| BK003      | 1            | Monday      | 4     | 20%       | No        |
| BK004      | 7            | Friday      | 2     | 60%       | Yes       |
| BK005      | 0            | Sunday      | 1     | 85%       | No        |
| BK006      | 21           | Saturday    | 2     | 90%       | Yes       |
| BK007      | 5            | Wednesday   | 3     | 50%       | Yes       |
| BK008      | 2            | Thursday    | 6     | 30%       | No        |
| BK009      | 10           | Friday      | 1     | 70%       | Yes       |
| BK010      | 14           | Sunday      | 2     | 80%       | Yes       |
| BK011      | 1            | Tuesday     | 5     | 25%       | No        |
| BK012      | 8            | Monday      | 1     | 55%       | Yes       |
| BK013      | 0            | Wednesday   | 2     | 45%       | No        |
| BK014      | 12           | Saturday    | 3     | 85%       | Yes       |
| BK015      | 4            | Friday      | 2     | 65%       | Yes       |
| BK016      | 18           | Sunday      | 1     | 72%       | Yes       |
| BK017      | 2            | Monday      | 3     | 35%       | No        |
| BK018      | 9            | Thursday    | 2     | 68%       | Yes       |
| BK019      | 0            | Friday      | 1     | 90%       | No        |
| BK020      | 25           | Saturday    | 2     | 82%       | Yes       |
| BK021      | 6            | Wednesday   | 4     | 48%       | Yes       |
| BK022      | 1            | Sunday      | 2     | 55%       | No        |
| BK023      | 11           | Friday      | 1     | 77%       | Yes       |
| BK024      | 3            | Tuesday     | 6     | 42%       | No        |
| BK025      | 16           | Monday      | 2     | 63%       | Yes       |
| BK026      | 5            | Saturday    | 3     | 88%       | Yes       |
| BK027      | 0            | Thursday    | 1     | 30%       | No        |
| BK028      | 8            | Sunday      | 2     | 71%       | Yes       |
| BK029      | 2            | Wednesday   | 5     | 38%       | No        |
| BK030      | 13           | Friday      | 1     | 79%       | Yes       |
| BK031      | 7            | Monday      | 2     | 52%       | Yes       |
| BK032      | 1            | Saturday    | 4     | 91%       | No        |
| BK033      | 19           | Tuesday     | 1     | 66%       | Yes       |
| BK034      | 4            | Thursday    | 3     | 44%       | Yes       |
| BK035      | 0            | Sunday      | 2     | 58%       | No        |
| BK036      | 10           | Wednesday   | 1     | 83%       | Yes       |
| BK037      | 3            | Friday      | 6     | 47%       | No        |
| BK038      | 22           | Saturday    | 2     | 76%       | Yes       |
| BK039      | 6            | Monday      | 1     | 61%       | Yes       |
| BK040      | 1            | Tuesday     | 3     | 29%       | No        |
| BK041      | 14           | Sunday      | 2     | 87%       | Yes       |
| BK042      | 5            | Thursday    | 1     | 53%       | Yes       |
| BK043      | 0            | Wednesday   | 4     | 41%       | No        |
| BK044      | 9            | Friday      | 2     | 74%       | Yes       |
| BK045      | 2            | Saturday    | 5     | 36%       | No        |
| BK046      | 17           | Monday      | 1     | 69%       | Yes       |
| BK047      | 4            | Sunday      | 3     | 81%       | Yes       |
| BK048      | 1            | Thursday    | 2     | 33%       | No        |
| BK049      | 12           | Tuesday     | 1     | 78%       | Yes       |
| BK050      | 8            | Friday      | 2     | 84%       | Yes       |

**Observations from mock data:**

- Advance bookings (>7 days) have ~90% confirmation rate
- Same-day bookings have only ~20% confirmation rate
- Weekend bookings show higher confirmation rates
- Large groups (5+ seats) have lower confirmation rates
- High occupancy dates correlate with committed travelers

---

## Example Predictions

### Example 1: Weekend trip, 10 days advance, 2 seats

```
Base: 75%
Days (10 days): +10%
Day (Saturday): +5%
Seats (2): +2%
Occupancy (60%): +8%
---
Total: 100% → Clamped to 100%

Result: 100% Likely to Confirm
```

### Example 2: Last-minute solo trip

```
Base: 75%
Days (1 day): -5%
Day (Wednesday): 0%
Seats (1): +3%
Occupancy (30%): +5%
---
Total: 78%

Result: 78% Likely to Confirm
```

### Example 3: Large group, same day

```
Base: 75%
Days (0 days): -10%
Day (Tuesday): 0%
Seats (6): -3%
Occupancy (25%): 0%
---
Total: 62%

Result: 62% Likely to Confirm
```

---

## API Implementation

**Endpoint:** `POST /api/predict`

**Request:**

```json
{
  "travel_date": "2026-01-25",
  "seat_count": 2
}
```

**Response:**

```json
{
  "prediction_percentage": 87.0,
  "factors": {
    "days_until_travel": {
      "days": 4,
      "impact": 5.0,
      "reasoning": "Advance bookings have higher confirmation rates"
    },
    "seat_occupancy": {
      "current_occupancy_percent": 45.0,
      "impact": 5.0,
      "reasoning": "Higher demand correlates with committed travelers"
    },
    "day_of_week": {
      "day": "Saturday",
      "impact": 5.0,
      "reasoning": "Weekend/Monday travel shows confirmed intent"
    },
    "seat_count": {
      "seats": 2,
      "impact": 2.0,
      "reasoning": "Smaller bookings have higher confirmation rates"
    }
  }
}
```

---

## Future Improvements

If real historical data becomes available, we could:

1. **Train an ML model** (Logistic Regression or Random Forest)
2. **Add more features:** Time of booking, payment method, user history
3. **A/B test** predictions against actual outcomes
4. **Dynamic weights** that update based on real confirmation rates
