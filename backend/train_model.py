"""
Logistic Regression Model for Booking Confirmation Prediction

Trains a logistic regression model on synthetic booking data
to predict whether a booking will be confirmed or cancelled.
"""

import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler


def load_data(data_path: str) -> pd.DataFrame:
    """Load the booking dataset."""
    df = pd.read_csv(data_path)
    print(f"Loaded {len(df)} samples")
    return df


def prepare_features(df: pd.DataFrame) -> tuple:
    """
    Prepare features and target for training.
    
    Features:
    - seat_type: 0 = upper, 1 = lower
    - meal_selected: 0 = no, 1 = yes
    - booking_lead_days: 0-30 days
    - day_of_week: 0-6 (Mon-Sun)
    - num_seats: 1-4
    
    Target:
    - confirmed: 0 = cancelled, 1 = confirmed
    """
    feature_columns = ['seat_type', 'meal_selected', 'booking_lead_days', 'day_of_week', 'num_seats']
    target_column = 'confirmed'
    
    X = df[feature_columns]
    y = df[target_column]
    
    return X, y, feature_columns


def train_model(X_train, y_train) -> tuple:
    """
    Train logistic regression model with feature scaling.
    
    Returns:
        model: Trained LogisticRegression model
        scaler: Fitted StandardScaler
    """
    # Scale features for better convergence
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    # Train logistic regression
    model = LogisticRegression(
        random_state=42,
        max_iter=1000,
        solver='lbfgs'
    )
    model.fit(X_train_scaled, y_train)
    
    return model, scaler


def evaluate_model(model, scaler, X_test, y_test, feature_names: list):
    """Evaluate model performance and print metrics."""
    # Scale test features
    X_test_scaled = scaler.transform(X_test)
    
    # Predictions
    y_pred = model.predict(X_test_scaled)
    y_prob = model.predict_proba(X_test_scaled)[:, 1]
    
    # Metrics
    accuracy = accuracy_score(y_test, y_pred)
    
    print("\n" + "="*50)
    print("MODEL EVALUATION")
    print("="*50)
    
    print(f"\nAccuracy: {accuracy:.2%}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Cancelled', 'Confirmed']))
    
    print("Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(f"  Predicted:  Cancel  Confirm")
    print(f"  Actual Cancel:  {cm[0][0]:4d}    {cm[0][1]:4d}")
    print(f"  Actual Confirm: {cm[1][0]:4d}    {cm[1][1]:4d}")
    
    # Feature importance (coefficients)
    print("\nFeature Importance (Coefficients):")
    coefficients = pd.DataFrame({
        'feature': feature_names,
        'coefficient': model.coef_[0]
    }).sort_values('coefficient', ascending=False)
    
    for _, row in coefficients.iterrows():
        direction = "↑" if row['coefficient'] > 0 else "↓"
        print(f"  {row['feature']:20s}: {row['coefficient']:+.4f} {direction}")
    
    return accuracy


def save_model(model, scaler, model_dir: str):
    """Save trained model and scaler to a single file."""
    os.makedirs(model_dir, exist_ok=True)
    
    model_path = os.path.join(model_dir, 'prediction_model.pkl')
    
    # Combine model and scaler into one file
    model_bundle = {
        'model': model,
        'scaler': scaler
    }
    
    with open(model_path, 'wb') as f:
        pickle.dump(model_bundle, f)

    print(f"\nModel saved to: {model_path}")


def predict_single(model, scaler, seat_type: int, meal_selected: int, 
                   booking_lead_days: int, day_of_week: int, num_seats: int) -> dict:
    """
    Make prediction for a single booking.
    
    Returns:
        dict with 'confirmed' (bool) and 'probability' (float)
    """
    features = np.array([[seat_type, meal_selected, booking_lead_days, day_of_week, num_seats]])
    features_scaled = scaler.transform(features)
    
    probability = model.predict_proba(features_scaled)[0][1]
    confirmed = probability >= 0.5
    
    return {
        'confirmed': bool(confirmed),
        'probability': float(probability)
    }


def main():
    """Main training pipeline."""
    # Paths
    script_dir = os.path.dirname(__file__)
    data_path = os.path.join(script_dir, '..', 'data', 'booking_data.csv')
    model_dir = os.path.join(script_dir, '..', 'models')
    
    print("="*50)
    print("LOGISTIC REGRESSION TRAINING")
    print("="*50)
    
    # Load data
    df = load_data(data_path)
    
    # Prepare features
    X, y, feature_names = prepare_features(df)
    print(f"Features: {feature_names}")
    print(f"Target distribution: {y.value_counts(normalize=True).to_dict()}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"\nTrain set: {len(X_train)} samples")
    print(f"Test set: {len(X_test)} samples")
    
    # Train model
    print("\nTraining model...")
    model, scaler = train_model(X_train, y_train)
    
    # Evaluate
    accuracy = evaluate_model(model, scaler, X_test, y_test, feature_names)
    
    # Save model
    save_model(model, scaler, model_dir)
    
    # Demo prediction
    print("\n" + "="*50)
    print("DEMO PREDICTION")
    print("="*50)
    
    demo_booking = {
        'seat_type': 1,  # lower deck
        'meal_selected': 1,  # yes
        'booking_lead_days': 7,  # 1 week before
        'day_of_week': 5,  # Saturday
        'num_seats': 2  # 2 seats
    }
    
    result = predict_single(model, scaler, **demo_booking)
    print(f"\nBooking: {demo_booking}")
    print(f"Prediction: {'Confirmed' if result['confirmed'] else 'Cancelled'}")
    print(f"Probability: {result['probability']:.1%}")
    
    return model, scaler


if __name__ == "__main__":
    main()
