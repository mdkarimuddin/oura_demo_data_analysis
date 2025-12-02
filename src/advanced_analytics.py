"""
Advanced Analytics on Oura Data
Time series forecasting, pattern recognition, anomaly detection
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Try to import ML libraries
try:
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_absolute_error, r2_score
    from sklearn.preprocessing import StandardScaler
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    print("⚠️  scikit-learn not available")

# Directories
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data' / 'processed'
OUTPUT_DIR = BASE_DIR / 'outputs'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_processed_data():
    """Load processed Oura data"""
    merged_file = DATA_DIR / 'oura_merged.csv'
    
    if not merged_file.exists():
        print(f"❌ Processed data not found: {merged_file}")
        print("   Run data_processor.py first!")
        return None
    
    df = pd.read_csv(merged_file)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)
    
    print(f"✅ Loaded {len(df)} records")
    print(f"   Date range: {df['date'].min()} to {df['date'].max()}")
    
    return df

def create_forecast_features(df):
    """Create features for readiness forecasting"""
    df_features = df.copy()
    
    # Lag features
    for lag in [1, 2, 3, 7]:
        if 'readiness_score' in df_features.columns:
            df_features[f'readiness_lag{lag}'] = df_features['readiness_score'].shift(lag)
        if 'sleep_score' in df_features.columns:
            df_features[f'sleep_lag{lag}'] = df_features['sleep_score'].shift(lag)
        if 'activity_score' in df_features.columns:
            df_features[f'activity_lag{lag}'] = df_features['activity_score'].shift(lag)
    
    # Rolling averages
    for window in [3, 7]:
        if 'readiness_score' in df_features.columns:
            df_features[f'readiness_roll{window}'] = df_features['readiness_score'].rolling(window).mean()
        if 'sleep_score' in df_features.columns:
            df_features[f'sleep_roll{window}'] = df_features['sleep_score'].rolling(window).mean()
    
    # Target: tomorrow's readiness
    if 'readiness_score' in df_features.columns:
        df_features['target_readiness'] = df_features['readiness_score'].shift(-1)
    
    return df_features

def forecast_readiness(df):
    """Forecast tomorrow's readiness score"""
    if not HAS_SKLEARN:
        print("⚠️  scikit-learn required for forecasting")
        return None
    
    print("\n" + "=" * 60)
    print("READINESS FORECASTING")
    print("=" * 60)
    
    # Create features
    df_features = create_forecast_features(df)
    
    # Drop rows where target is NaN (last row) but keep rows with some NaN in features
    df_features = df_features[df_features['target_readiness'].notna()]
    
    # Fill remaining NaN in features with forward fill or median
    feature_cols = [c for c in df_features.columns if 
                    c not in ['date', 'target_readiness', 'readiness_score'] and
                    not c.startswith('id')]
    
    for col in feature_cols:
        if df_features[col].isna().any():
            df_features[col] = df_features[col].fillna(df_features[col].median())
    
    if len(df_features) == 0:
        print("❌ No data after feature engineering")
        return None
    
    # Select features
    feature_cols = [c for c in df_features.columns if 
                    c not in ['date', 'target_readiness', 'readiness_score'] and
                    not c.startswith('id')]
    
    X = df_features[feature_cols].select_dtypes(include=[np.number])
    y = df_features['target_readiness']
    
    print(f"Features: {len(X.columns)}")
    print(f"Samples: {len(X)}")
    
    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, shuffle=False
    )
    
    # Scale
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    print("\nTraining Random Forest model...")
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train_scaled, y_train)
    
    # Predict
    y_pred = model.predict(X_test_scaled)
    
    # Metrics
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\nResults:")
    print(f"  R²:  {r2:.3f}")
    print(f"  MAE: {mae:.2f} points")
    
    return {
        'r2': r2,
        'mae': mae,
        'model': model,
        'predictions': y_pred,
        'actual': y_test
    }

def detect_anomalies(df):
    """Detect unusual health patterns"""
    print("\n" + "=" * 60)
    print("ANOMALY DETECTION")
    print("=" * 60)
    
    if 'readiness_score' not in df.columns:
        print("⚠️  Readiness score not available")
        return None
    
    # Simple statistical anomaly detection
    readiness = df['readiness_score'].dropna()
    
    mean_score = readiness.mean()
    std_score = readiness.std()
    
    # Anomalies: > 2 standard deviations from mean
    threshold_low = mean_score - 2 * std_score
    threshold_high = mean_score + 2 * std_score
    
    anomalies = df[
        (df['readiness_score'] < threshold_low) | 
        (df['readiness_score'] > threshold_high)
    ].copy()
    
    print(f"\nAnomaly Detection Results:")
    print(f"  Mean readiness: {mean_score:.1f}")
    print(f"  Std deviation: {std_score:.1f}")
    print(f"  Threshold: {threshold_low:.1f} - {threshold_high:.1f}")
    print(f"  Anomalies found: {len(anomalies)} days")
    
    if len(anomalies) > 0:
        print(f"\nAnomaly dates:")
        for _, row in anomalies.head(10).iterrows():
            print(f"  {row['date'].date()}: Readiness = {row['readiness_score']:.1f}")
    
    return anomalies

def calculate_personal_baselines(df):
    """Calculate user-specific baselines"""
    print("\n" + "=" * 60)
    print("PERSONAL BASELINES")
    print("=" * 60)
    
    baselines = {}
    
    if 'readiness_score' in df.columns:
        baselines['readiness'] = {
            'mean': df['readiness_score'].mean(),
            'median': df['readiness_score'].median(),
            'std': df['readiness_score'].std()
        }
    
    if 'sleep_score' in df.columns:
        baselines['sleep'] = {
            'mean': df['sleep_score'].mean(),
            'median': df['sleep_score'].median(),
            'std': df['sleep_score'].std()
        }
    
    if 'activity_score' in df.columns:
        baselines['activity'] = {
            'mean': df['activity_score'].mean(),
            'median': df['activity_score'].median(),
            'std': df['activity_score'].std()
        }
    
    print("\nPersonal Baselines:")
    for metric, stats in baselines.items():
        print(f"\n{metric.capitalize()}:")
        print(f"  Mean: {stats['mean']:.1f}")
        print(f"  Median: {stats['median']:.1f}")
        print(f"  Std Dev: {stats['std']:.1f}")
    
    return baselines

def main():
    """Main analytics pipeline"""
    print("=" * 60)
    print("ADVANCED OURA ANALYTICS")
    print("=" * 60)
    
    # Load data
    print("\nLoading processed data...")
    df = load_processed_data()
    
    if df is None:
        return
    
    # Analytics
    print("\n" + "=" * 60)
    print("RUNNING ANALYTICS")
    print("=" * 60)
    
    # Personal baselines
    baselines = calculate_personal_baselines(df)
    
    # Anomaly detection
    anomalies = detect_anomalies(df)
    
    # Forecasting
    forecast_results = forecast_readiness(df)
    
    # Save results
    print("\n" + "=" * 60)
    print("SAVING RESULTS")
    print("=" * 60)
    
    import json
    
    results = {
        'baselines': {k: {kk: float(vv) for kk, vv in v.items()} for k, v in baselines.items()},
        'anomalies_count': len(anomalies) if anomalies is not None else 0,
        'forecast': {
            'r2': float(forecast_results['r2']) if forecast_results else None,
            'mae': float(forecast_results['mae']) if forecast_results else None
        } if forecast_results else None
    }
    
    with open(OUTPUT_DIR / 'analytics_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("✅ Results saved to: analytics_results.json")
    
    print("\n" + "=" * 60)
    print("✅ ANALYTICS COMPLETE!")
    print("=" * 60)

if __name__ == '__main__':
    main()

