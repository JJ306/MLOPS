import warnings
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, f1_score, precision_score,
                             recall_score)
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")


def load_data():
    """Load sensor data"""
    df = pd.read_csv("data/raw/sensor_data.csv")

    # Drop non-features
    df = df.drop(["timestamp", "engine_id", "cycle"], axis=1)

    return df


def create_features(df, seq_length=24):
    """Create time series features"""
    features = ["temperature", "pressure", "vibration", "rpm", "torque", "fuel_flow"]
    X = df[features].values
    y = df["failure"].values

    # Create sequences
    X_seq, y_seq = [], []
    for i in range(len(X) - seq_length):
        X_seq.append(X[i : i + seq_length])
        y_seq.append(y[i + seq_length])

    return np.array(X_seq), np.array(y_seq), features


def train_model(X_train, y_train):
    """Train Random Forest model"""
    # Flatten 3D sequences: (samples, timesteps, features) -> (samples, timesteps*features)
    X_train_flat = X_train.reshape(X_train.shape[0], -1)

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1,
    )
    model.fit(X_train_flat, y_train)
    return model


def evaluate_model(model, X_test, y_test):
    """Evaluate model metrics"""
    # Flatten test data
    X_test_flat = X_test.reshape(X_test.shape[0], -1)
    y_pred = model.predict(X_test_flat)

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1_score": f1_score(y_test, y_pred),
    }

    return metrics, y_pred


if __name__ == "__main__":
    print("🎯 Starting Model Training...")

    # Load data
    print("📊 Loading data...")
    df = load_data()
    print(f"✅ Loaded {len(df):,} samples")

    # Create features
    print("🔧 Creating time series features...")
    X, y, features = create_features(df, seq_length=24)
    print(f"✅ Created {len(X):,} sequences with shape {X.shape}")

    # Scale features (flatten for scaling, then reshape back)
    scaler = StandardScaler()
    X_flat = X.reshape(-1, X.shape[-1])
    X_scaled = scaler.fit_transform(X_flat)
    X = X_scaled.reshape(X.shape)

    # Split data (time-based split, not random)
    split_idx = int(len(X) * 0.8)
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    print(f"✅ Split: {len(X_train):,} train, {len(X_test):,} test")

    # Train model
    print("🚀 Training model...")
    model = train_model(X_train, y_train)

    # Evaluate
    print("📈 Evaluating model...")
    metrics, y_pred = evaluate_model(model, X_test, y_test)

    print(f"""
✅ Model Performance:
   Accuracy:  {metrics['accuracy']:.4f}
   Precision: {metrics['precision']:.4f}
   Recall:    {metrics['recall']:.4f}
   F1 Score:  {metrics['f1_score']:.4f}
    """)

    # Log to MLflow
    print("📊 Logging to MLflow...")
    Path("models").mkdir(exist_ok=True)

    mlflow.set_experiment("Predictive Maintenance")
    with mlflow.start_run():
        # Log parameters
        mlflow.log_param("n_estimators", 100)
        mlflow.log_param("max_depth", 10)
        mlflow.log_param("seq_length", 24)
        mlflow.log_param("train_size", len(X_train))
        mlflow.log_param("test_size", len(X_test))
        mlflow.log_param("features", str(features))
        mlflow.log_param("flattened_features", X_train.shape[1] * X_train.shape[2])

        # Log metrics
        for metric_name, value in metrics.items():
            mlflow.log_metric(metric_name, value)

        # Save model
        model_path = "models/final_model.pkl"
        joblib.dump(model, model_path)
        joblib.dump(scaler, "models/scaler.pkl")

        mlflow.log_artifact(model_path)
        mlflow.log_artifact("models/scaler.pkl")

        print("✅ Model logged to MLflow")
        print(f"   Run ID: {mlflow.active_run().info.run_id}")
        print(f"   Model saved to: {model_path}")

    print("\n✅ Training complete!")
