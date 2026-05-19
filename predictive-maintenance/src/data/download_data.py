import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")


def create_sensor_data(n_samples=50000):
    """Generate synthetic predictive maintenance sensor data"""
    np.random.seed(42)

    print("📊 Generating sensor data...")

    # Time series data
    data = {
        "timestamp": pd.date_range("2024-01-01", periods=n_samples, freq="H"),
        "engine_id": np.random.randint(1, 101, n_samples),  # 100 engines
        "cycle": np.tile(range(1, int(n_samples / 100) + 1), 100),
        "temperature": np.random.normal(50, 10, n_samples),
        "pressure": np.random.normal(100, 15, n_samples),
        "vibration": np.random.normal(5, 2, n_samples),
        "rpm": np.random.normal(3000, 200, n_samples),
        "torque": np.random.normal(50, 10, n_samples),
        "fuel_flow": np.random.normal(200, 30, n_samples),
    }

    df = pd.DataFrame(data)

    # Create failure labels (10% failure rate, correlated with sensors)
    failure_prob = (
        0.03
        + 0.01 * (df["temperature"] - 50) / 10
        + 0.02 * (df["vibration"] - 5) / 2
        + 0.005 * (df["pressure"] - 100) / 15
    )
    df["failure"] = (np.random.random(n_samples) < failure_prob).astype(int)

    return df


if __name__ == "__main__":
    # Create directory
    Path("data/raw").mkdir(parents=True, exist_ok=True)

    # Generate data
    df = create_sensor_data(n_samples=50000)

    # Save to CSV
    output_path = "data/raw/sensor_data.csv"
    df.to_csv(output_path, index=False)

    print(f"""
✅ Dataset Created:
   Location: {output_path}
   Samples:  {len(df):,}
   Features: {len(df.columns) - 1}
   Failures: {df['failure'].sum():,} ({df['failure'].mean()*100:.1f}%)
   Columns: {list(df.columns)}
   First 5 rows:
{df.head()}
    """)
