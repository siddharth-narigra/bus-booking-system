"""
Synthetic Dataset Generator for Bus Booking Prediction

Generates realistic booking data for training a logistic regression model
to predict booking confirmation vs cancellation.

Features:
- seat_type: 0 = upper, 1 = lower
- meal_selected: 0 = no, 1 = yes
- booking_lead_days: 0-30 days before travel
- day_of_week: 0-6 (Mon-Sun)
- num_seats: 1-4 seats

Target:
- confirmed: 1 = confirmed, 0 = cancelled
"""

import numpy as np
import pandas as pd
import os

# Set random seed for reproducibility
np.random.seed(42)

# Number of samples
N_SAMPLES = 1000


def generate_features(n: int) -> pd.DataFrame:
    """Generate feature values for n samples."""
    data = {
        'seat_type': np.random.choice([0, 1], size=n, p=[0.5, 0.5]),  # 50% upper, 50% lower
        'meal_selected': np.random.choice([0, 1], size=n, p=[0.4, 0.6]),  # 60% select meal
        'booking_lead_days': np.random.randint(0, 31, size=n),  # 0-30 days
        'day_of_week': np.random.randint(0, 7, size=n),  # Mon-Sun
        'num_seats': np.random.choice([1, 2, 3, 4], size=n, p=[0.5, 0.3, 0.15, 0.05])  # Most book 1-2
    }
    return pd.DataFrame(data)


def calculate_confirmation_probability(row: pd.Series) -> float:
    """
    Calculate probability of confirmation based on realistic patterns.
    
    Logic:
    - Lower deck seats: slightly higher confirmation (premium, more committed)
    - Meal selected: higher confirmation (more invested in trip)
    - More lead days: higher confirmation (planned trip)
    - Weekend travel (Fri=4, Sat=5, Sun=6): higher confirmation (leisure)
    - More seats: slightly lower confirmation (group coordination issues)
    """
    base_prob = 0.70  # Base 70% confirmation rate
    
    # Seat type effect: lower deck +5%
    seat_effect = 0.05 if row['seat_type'] == 1 else 0
    
    # Meal selected: +10% (commitment indicator)
    meal_effect = 0.10 if row['meal_selected'] == 1 else 0
    
    # Lead days: +0.5% per day, max +15%
    lead_effect = min(row['booking_lead_days'] * 0.005, 0.15)
    
    # Weekend travel: +8%
    is_weekend = row['day_of_week'] in [4, 5, 6]  # Fri, Sat, Sun
    weekend_effect = 0.08 if is_weekend else 0
    
    # Number of seats: -3% per additional seat
    seat_count_effect = -(row['num_seats'] - 1) * 0.03
    
    # Calculate total probability
    prob = base_prob + seat_effect + meal_effect + lead_effect + weekend_effect + seat_count_effect
    
    # Clamp between 0.1 and 0.95 (never 0% or 100%)
    return np.clip(prob, 0.1, 0.95)


def add_noise_and_classify(probabilities: np.ndarray, noise_level: float = 0.15) -> np.ndarray:
    """
    Convert probabilities to binary outcomes with some noise.
    
    Args:
        probabilities: Array of confirmation probabilities
        noise_level: Fraction of samples to randomly flip (0.15 = 15%)
    
    Returns:
        Binary array of confirmed (1) or cancelled (0)
    """
    # Generate outcomes based on probability
    outcomes = np.random.random(len(probabilities)) < probabilities
    
    # Add noise: randomly flip some outcomes
    noise_mask = np.random.random(len(outcomes)) < noise_level
    outcomes[noise_mask] = ~outcomes[noise_mask]
    
    return outcomes.astype(int)


def generate_dataset(n: int = N_SAMPLES) -> pd.DataFrame:
    """Generate complete dataset with features and target."""
    # Generate features
    df = generate_features(n)
    
    # Calculate confirmation probabilities
    probabilities = df.apply(calculate_confirmation_probability, axis=1).values
    
    # Generate binary outcomes with noise
    df['confirmed'] = add_noise_and_classify(probabilities, noise_level=0.12)
    
    return df


def main():
    """Generate and save the dataset."""
    print("Generating synthetic booking dataset...")
    
    # Generate dataset
    df = generate_dataset(N_SAMPLES)
    
    # Create data directory if needed
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Save to CSV
    output_path = os.path.join(data_dir, 'booking_data.csv')
    df.to_csv(output_path, index=False)
    
    print(f"Dataset saved to: {output_path}")
    print(f"Total samples: {len(df)}")
    print(f"\nConfirmation rate: {df['confirmed'].mean():.1%}")
    print(f"\nFeature distributions:")
    print(df.describe())
    
    print(f"\nTarget distribution:")
    print(df['confirmed'].value_counts(normalize=True))
    
    return df


if __name__ == "__main__":
    main()
