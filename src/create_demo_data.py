"""
Create Demo Data Matching Real Oura API Structure
Use this when you don't have an Oura Ring yet
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Directories
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data' / 'raw'
DATA_DIR.mkdir(parents=True, exist_ok=True)

def generate_demo_sleep_data(n_days=90):
    """Generate demo sleep data matching Oura API structure"""
    start_date = datetime.now() - timedelta(days=n_days)
    data = []
    
    for i in range(n_days):
        date = start_date + timedelta(days=i)
        day_of_week = date.weekday()
        
        # Weekend effects
        is_weekend = day_of_week >= 5
        
        # Generate realistic sleep scores
        base_score = np.random.normal(75, 10)
        if is_weekend:
            base_score += np.random.normal(5, 3)  # Better sleep on weekends
        
        score = max(40, min(100, int(base_score)))
        
        # Contributors (should sum to ~score)
        deep_sleep = max(0, min(100, int(np.random.normal(80, 15))))
        efficiency = max(0, min(100, int(np.random.normal(85, 10))))
        latency = max(0, min(100, int(np.random.normal(75, 20))))
        rem_sleep = max(0, min(100, int(np.random.normal(70, 15))))
        restfulness = max(0, min(100, int(np.random.normal(65, 20))))
        timing = max(0, min(100, int(np.random.normal(60, 25))))
        total_sleep = max(0, min(100, int(np.random.normal(75, 15))))
        
        data.append({
            "id": f"demo_sleep_{i}",
            "day": date.strftime("%Y-%m-%d"),
            "score": score,
            "timestamp": date.strftime("%Y-%m-%dT00:00:00+00:00"),
            "contributors": {
                "deep_sleep": deep_sleep,
                "efficiency": efficiency,
                "latency": latency,
                "rem_sleep": rem_sleep,
                "restfulness": restfulness,
                "timing": timing,
                "total_sleep": total_sleep
            }
        })
    
    return data

def generate_demo_activity_data(n_days=90):
    """Generate demo activity data matching Oura API structure"""
    start_date = datetime.now() - timedelta(days=n_days)
    data = []
    
    for i in range(n_days):
        date = start_date + timedelta(days=i)
        day_of_week = date.weekday()
        is_weekend = day_of_week >= 5
        
        # Generate realistic activity
        base_steps = np.random.normal(8000, 2000)
        if is_weekend:
            base_steps *= np.random.uniform(0.7, 1.2)
        
        steps = max(0, int(base_steps))
        active_calories = int(steps * 0.04 + np.random.normal(200, 50))
        total_calories = int(active_calories + 1500 + np.random.normal(0, 100))
        
        score = max(40, min(100, int(np.random.normal(75, 12))))
        
        data.append({
            "id": f"demo_activity_{i}",
            "day": date.strftime("%Y-%m-%d"),
            "score": score,
            "steps": steps,
            "active_calories": active_calories,
            "total_calories": total_calories,
            "timestamp": date.strftime("%Y-%m-%dT00:00:00+00:00"),
            "contributors": {
                "meet_daily_targets": max(0, min(100, int(np.random.normal(70, 20)))),
                "move_every_hour": max(0, min(100, int(np.random.normal(65, 25)))),
                "recovery_time": max(0, min(100, int(np.random.normal(80, 15)))),
                "stay_active": max(0, min(100, int(np.random.normal(75, 15)))),
                "training_frequency": max(0, min(100, int(np.random.normal(60, 25)))),
                "training_volume": max(0, min(100, int(np.random.normal(70, 20))))
            }
        })
    
    return data

def generate_demo_readiness_data(n_days=90):
    """Generate demo readiness data matching Oura API structure"""
    start_date = datetime.now() - timedelta(days=n_days)
    data = []
    
    for i in range(n_days):
        date = start_date + timedelta(days=i)
        
        score = max(40, min(100, int(np.random.normal(75, 12))))
        temp_dev = np.random.normal(0, 0.2)
        temp_trend = np.random.normal(0, 0.15)
        
        data.append({
            "id": f"demo_readiness_{i}",
            "day": date.strftime("%Y-%m-%d"),
            "score": score,
            "temperature_deviation": round(temp_dev, 2),
            "temperature_trend_deviation": round(temp_trend, 2),
            "timestamp": date.strftime("%Y-%m-%dT00:00:00+00:00"),
            "contributors": {
                "activity_balance": max(0, min(100, int(np.random.normal(70, 20)))),
                "body_temperature": max(0, min(100, int(np.random.normal(95, 10)))),
                "hrv_balance": max(0, min(100, int(np.random.normal(75, 15)))),
                "previous_day_activity": None,
                "previous_night": max(0, min(100, int(np.random.normal(70, 15)))),
                "recovery_index": max(0, min(100, int(np.random.normal(80, 15)))),
                "resting_heart_rate": max(0, min(100, int(np.random.normal(90, 10)))),
                "sleep_balance": max(0, min(100, int(np.random.normal(75, 15))))
            }
        })
    
    return data

def main():
    """Generate demo data matching Oura API structure"""
    print("=" * 60)
    print("GENERATING DEMO OURA DATA")
    print("=" * 60)
    print("\nThis creates example data matching the real Oura API structure.")
    print("Use this when you don't have an Oura Ring yet.\n")
    
    n_days = 90
    
    # Generate data
    print(f"Generating {n_days} days of demo data...")
    sleep_data = generate_demo_sleep_data(n_days)
    activity_data = generate_demo_activity_data(n_days)
    readiness_data = generate_demo_readiness_data(n_days)
    
    # Save as JSON
    print("\nSaving data...")
    with open(DATA_DIR / 'oura_sleep.json', 'w') as f:
        json.dump(sleep_data, f, indent=2)
    print(f"✅ Saved: oura_sleep.json ({len(sleep_data)} records)")
    
    with open(DATA_DIR / 'oura_activity.json', 'w') as f:
        json.dump(activity_data, f, indent=2)
    print(f"✅ Saved: oura_activity.json ({len(activity_data)} records)")
    
    with open(DATA_DIR / 'oura_readiness.json', 'w') as f:
        json.dump(readiness_data, f, indent=2)
    print(f"✅ Saved: oura_readiness.json ({len(readiness_data)} records)")
    
    # Save as CSV
    sleep_df = pd.json_normalize(sleep_data)
    sleep_df.to_csv(DATA_DIR / 'oura_sleep.csv', index=False)
    print(f"✅ Saved: oura_sleep.csv")
    
    activity_df = pd.json_normalize(activity_data)
    activity_df.to_csv(DATA_DIR / 'oura_activity.csv', index=False)
    print(f"✅ Saved: oura_activity.csv")
    
    readiness_df = pd.json_normalize(readiness_data)
    readiness_df.to_csv(DATA_DIR / 'oura_readiness.csv', index=False)
    print(f"✅ Saved: oura_readiness.csv")
    
    print("\n" + "=" * 60)
    print("✅ DEMO DATA GENERATED!")
    print("=" * 60)
    print("\nYou can now run:")
    print("  python src/data_processor.py")
    print("\nWhen you get your Oura Ring, just:")
    print("  1. Get token from: https://cloud.ouraring.com/personal-access-tokens")
    print("  2. Run: python src/data_fetcher.py")
    print("  3. All analytics will work with real data!")

if __name__ == '__main__':
    main()

