"""
Process Real Oura Data
Clean, merge, and prepare data for analysis
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Directories
BASE_DIR = Path(__file__).parent.parent
RAW_DIR = BASE_DIR / 'data' / 'raw'
PROCESSED_DIR = BASE_DIR / 'data' / 'processed'
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def load_oura_data():
    """Load all Oura data files"""
    data = {}
    
    for data_type in ['sleep', 'activity', 'readiness', 'heart_rate']:
        csv_file = RAW_DIR / f'oura_{data_type}.csv'
        if csv_file.exists():
            df = pd.read_csv(csv_file)
            data[data_type] = df
            print(f"✅ Loaded {data_type}: {len(df)} records")
        else:
            print(f"⚠️  {data_type} data not found: {csv_file}")
            data[data_type] = None
    
    return data

def process_sleep_data(sleep_df):
    """Process sleep data"""
    if sleep_df is None or len(sleep_df) == 0:
        return None
    
    df = sleep_df.copy()
    
    # Flatten contributors if needed
    if 'contributors.deep_sleep' in df.columns:
        # Already flattened
        pass
    elif 'contributors' in df.columns:
        # Need to flatten
        contributors = pd.json_normalize(df['contributors'])
        df = pd.concat([df.drop('contributors', axis=1), contributors.add_prefix('contributor_')], axis=1)
    
    # Convert date
    if 'day' in df.columns:
        df['date'] = pd.to_datetime(df['day'])
    elif 'timestamp' in df.columns:
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        df['date'] = pd.to_datetime(df['date'])
    
    # Select key columns
    key_cols = ['date', 'score']
    contributor_cols = [c for c in df.columns if 'contributor' in c.lower()]
    key_cols.extend(contributor_cols)
    
    df_processed = df[[c for c in key_cols if c in df.columns]].copy()
    df_processed = df_processed.sort_values('date').reset_index(drop=True)
    
    return df_processed

def process_activity_data(activity_df):
    """Process activity data"""
    if activity_df is None or len(activity_df) == 0:
        return None
    
    df = activity_df.copy()
    
    # Flatten contributors
    if 'contributors' in df.columns:
        contributors = pd.json_normalize(df['contributors'])
        df = pd.concat([df.drop('contributors', axis=1), contributors.add_prefix('contributor_')], axis=1)
    
    # Convert date
    if 'day' in df.columns:
        df['date'] = pd.to_datetime(df['day'])
    elif 'timestamp' in df.columns:
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        df['date'] = pd.to_datetime(df['date'])
    
    # Select key columns
    key_cols = ['date', 'score', 'steps', 'total_calories', 'active_calories']
    contributor_cols = [c for c in df.columns if 'contributor' in c.lower()]
    key_cols.extend(contributor_cols)
    
    df_processed = df[[c for c in key_cols if c in df.columns]].copy()
    df_processed = df_processed.sort_values('date').reset_index(drop=True)
    
    return df_processed

def process_readiness_data(readiness_df):
    """Process readiness data"""
    if readiness_df is None or len(readiness_df) == 0:
        return None
    
    df = readiness_df.copy()
    
    # Flatten contributors
    if 'contributors' in df.columns:
        contributors = pd.json_normalize(df['contributors'])
        df = pd.concat([df.drop('contributors', axis=1), contributors.add_prefix('contributor_')], axis=1)
    
    # Convert date
    if 'day' in df.columns:
        df['date'] = pd.to_datetime(df['day'])
    elif 'timestamp' in df.columns:
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        df['date'] = pd.to_datetime(df['date'])
    
    # Select key columns
    key_cols = ['date', 'score', 'temperature_deviation', 'temperature_trend_deviation']
    contributor_cols = [c for c in df.columns if 'contributor' in c.lower()]
    key_cols.extend(contributor_cols)
    
    df_processed = df[[c for c in key_cols if c in df.columns]].copy()
    df_processed = df_processed.sort_values('date').reset_index(drop=True)
    
    return df_processed

def merge_all_data(sleep_df, activity_df, readiness_df):
    """Merge all Oura data by date"""
    dfs = []
    
    if sleep_df is not None:
        sleep_df = sleep_df.rename(columns={'score': 'sleep_score'})
        dfs.append(sleep_df)
    
    if activity_df is not None:
        activity_df = activity_df.rename(columns={'score': 'activity_score'})
        dfs.append(activity_df)
    
    if readiness_df is not None:
        readiness_df = readiness_df.rename(columns={'score': 'readiness_score'})
        dfs.append(readiness_df)
    
    if not dfs:
        print("⚠️  No data to merge")
        return None
    
    # Merge on date
    merged = dfs[0]
    for df in dfs[1:]:
        merged = pd.merge(merged, df, on='date', how='outer', suffixes=('', '_dup'))
        # Remove duplicate columns
        merged = merged.loc[:, ~merged.columns.str.endswith('_dup')]
    
    merged = merged.sort_values('date').reset_index(drop=True)
    
    return merged

def main():
    """Main data processing pipeline"""
    print("=" * 60)
    print("PROCESSING OURA DATA")
    print("=" * 60)
    
    # Load raw data
    print("\nLoading raw data...")
    raw_data = load_oura_data()
    
    # Check if any data exists
    has_data = any(
        v is not None and (isinstance(v, pd.DataFrame) and len(v) > 0 or isinstance(v, list) and len(v) > 0)
        for v in raw_data.values()
    )
    
    if not has_data:
        print("\n❌ No data files found!")
        print("   Run data_fetcher.py first to fetch data from Oura API")
        print("   Or run create_demo_data.py to generate demo data")
        return
    
    # Process each data type
    print("\n" + "=" * 60)
    print("PROCESSING DATA")
    print("=" * 60)
    
    processed_sleep = process_sleep_data(raw_data.get('sleep'))
    processed_activity = process_activity_data(raw_data.get('activity'))
    processed_readiness = process_readiness_data(raw_data.get('readiness'))
    
    # Save processed data
    if processed_sleep is not None:
        output_file = PROCESSED_DIR / 'sleep_processed.csv'
        processed_sleep.to_csv(output_file, index=False)
        print(f"\n✅ Saved: {output_file}")
    
    if processed_activity is not None:
        output_file = PROCESSED_DIR / 'activity_processed.csv'
        processed_activity.to_csv(output_file, index=False)
        print(f"✅ Saved: {output_file}")
    
    if processed_readiness is not None:
        output_file = PROCESSED_DIR / 'readiness_processed.csv'
        processed_readiness.to_csv(output_file, index=False)
        print(f"✅ Saved: {output_file}")
    
    # Merge all data
    print("\n" + "=" * 60)
    print("MERGING DATA")
    print("=" * 60)
    
    merged_df = merge_all_data(processed_sleep, processed_activity, processed_readiness)
    
    if merged_df is not None:
        output_file = PROCESSED_DIR / 'oura_merged.csv'
        merged_df.to_csv(output_file, index=False)
        print(f"\n✅ Merged dataset saved: {output_file}")
        print(f"   Records: {len(merged_df)}")
        print(f"   Columns: {len(merged_df.columns)}")
        print(f"   Date range: {merged_df['date'].min()} to {merged_df['date'].max()}")
        
        # Summary
        print("\n" + "=" * 60)
        print("DATA SUMMARY")
        print("=" * 60)
        print(merged_df.describe())
    
    print("\n" + "=" * 60)
    print("✅ DATA PROCESSING COMPLETE!")
    print("=" * 60)

if __name__ == '__main__':
    main()

