"""
Fetch Real Oura Data from API
Main script to download and save Oura Ring data
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

from api_client import OuraDataFetcher

# Directories
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data' / 'raw'
DATA_DIR.mkdir(parents=True, exist_ok=True)

def save_data(data: list, filename: str):
    """Save data to JSON and CSV"""
    if not data:
        print(f"⚠️  No data to save for {filename}")
        return
    
    # Save as JSON
    json_file = DATA_DIR / f"{filename}.json"
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"✅ Saved JSON: {json_file}")
    
    # Save as CSV (flatten nested structures)
    try:
        df = pd.json_normalize(data)
        csv_file = DATA_DIR / f"{filename}.csv"
        df.to_csv(csv_file, index=False)
        print(f"✅ Saved CSV: {csv_file} ({len(df)} rows, {len(df.columns)} columns)")
    except Exception as e:
        print(f"⚠️  Could not save CSV: {e}")

def main():
    """Main data fetching pipeline"""
    print("=" * 60)
    print("OURA REAL DATA FETCHER")
    print("=" * 60)
    
    try:
        # Initialize fetcher
        print("\nInitializing Oura API client...")
        fetcher = OuraDataFetcher()
        
        # Fetch all data (last 90 days)
        print("\nFetching data from Oura API...")
        all_data = fetcher.get_all_data(days_back=90)
        
        # Save each data type
        print("\n" + "=" * 60)
        print("SAVING DATA")
        print("=" * 60)
        
        for data_type, data_list in all_data.items():
            if data_list:
                save_data(data_list, f"oura_{data_type}")
        
        # Create summary
        summary = {
            'fetch_date': datetime.now().isoformat(),
            'data_types': {k: len(v) for k, v in all_data.items()},
            'total_records': sum(len(v) for v in all_data.values())
        }
        
        summary_file = DATA_DIR / 'fetch_summary.json'
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n✅ Summary saved: {summary_file}")
        print("\n" + "=" * 60)
        print("✅ DATA FETCH COMPLETE!")
        print("=" * 60)
        
        # Close client
        fetcher.close()
        
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\n" + "=" * 60)
        print("NO TOKEN? USE DEMO MODE!")
        print("=" * 60)
        print("\nSince you don't have an Oura Ring yet, you can:")
        print("1. Generate demo data matching real API structure:")
        print("   python src/create_demo_data.py")
        print("\n2. Then process the demo data:")
        print("   python src/data_processor.py")
        print("\nWhen you get your Oura Ring:")
        print("1. Get Personal Access Token from: https://cloud.ouraring.com/personal-access-tokens")
        print("2. Set environment variable:")
        print("   export OURA_PERSONAL_ACCESS_TOKEN='your_token_here'")
        print("3. Run this script again to fetch real data!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()

