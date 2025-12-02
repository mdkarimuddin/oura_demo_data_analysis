"""
Oura API Client Wrapper
Simplified interface for fetching Oura Ring data
"""

import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List, Any
import warnings
warnings.filterwarnings('ignore')

# Try to import Oura client
try:
    from oura_ring import OuraClient
    HAS_OURA_CLIENT = True
except ImportError:
    HAS_OURA_CLIENT = False
    print("⚠️  oura-ring package not installed. Install with: pip install oura-ring")

# Try to load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    HAS_DOTENV = True
except ImportError:
    HAS_DOTENV = False

class OuraDataFetcher:
    """
    Wrapper for Oura API client with error handling and data processing
    """
    
    def __init__(self, personal_access_token: Optional[str] = None):
        """
        Initialize Oura API client
        
        Args:
            personal_access_token: Oura Personal Access Token. 
                                  If None, tries to load from environment variable OURA_PERSONAL_ACCESS_TOKEN
        """
        if personal_access_token is None:
            personal_access_token = os.getenv("OURA_PERSONAL_ACCESS_TOKEN", "")
        
        if not personal_access_token:
            raise ValueError(
                "Personal Access Token required. "
                "Get one from: https://cloud.ouraring.com/personal-access-tokens\n"
                "Set it as environment variable: OURA_PERSONAL_ACCESS_TOKEN"
            )
        
        if not HAS_OURA_CLIENT:
            raise ImportError("oura-ring package required. Install with: pip install oura-ring")
        
        self.client = OuraClient(personal_access_token)
        self.token = personal_access_token
    
    def get_sleep_data(self, start_date: Optional[str] = None, end_date: Optional[str] = None, 
                       days_back: int = 90) -> List[Dict[str, Any]]:
        """
        Fetch daily sleep data
        
        Args:
            start_date: Start date (YYYY-MM-DD). If None, uses days_back from today
            end_date: End date (YYYY-MM-DD). If None, uses today
            days_back: Number of days to fetch (if start_date not provided)
        
        Returns:
            List of sleep data dictionaries
        """
        if end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")
        
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        
        try:
            sleep_data = self.client.get_daily_sleep(start_date=start_date, end_date=end_date)
            print(f"✅ Fetched {len(sleep_data)} days of sleep data ({start_date} to {end_date})")
            return sleep_data
        except Exception as e:
            print(f"❌ Error fetching sleep data: {e}")
            return []
    
    def get_activity_data(self, start_date: Optional[str] = None, end_date: Optional[str] = None,
                          days_back: int = 90) -> List[Dict[str, Any]]:
        """
        Fetch daily activity data
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            days_back: Number of days to fetch
        
        Returns:
            List of activity data dictionaries
        """
        if end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")
        
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        
        try:
            activity_data = self.client.get_daily_activity(start_date=start_date, end_date=end_date)
            print(f"✅ Fetched {len(activity_data)} days of activity data ({start_date} to {end_date})")
            return activity_data
        except Exception as e:
            print(f"❌ Error fetching activity data: {e}")
            return []
    
    def get_readiness_data(self, start_date: Optional[str] = None, end_date: Optional[str] = None,
                           days_back: int = 90) -> List[Dict[str, Any]]:
        """
        Fetch daily readiness data
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            days_back: Number of days to fetch
        
        Returns:
            List of readiness data dictionaries
        """
        if end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")
        
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        
        try:
            readiness_data = self.client.get_daily_readiness(start_date=start_date, end_date=end_date)
            print(f"✅ Fetched {len(readiness_data)} days of readiness data ({start_date} to {end_date})")
            return readiness_data
        except Exception as e:
            print(f"❌ Error fetching readiness data: {e}")
            return []
    
    def get_heart_rate_data(self, start_datetime: Optional[str] = None, 
                            end_datetime: Optional[str] = None,
                            days_back: int = 7) -> List[Dict[str, Any]]:
        """
        Fetch heart rate data
        
        Args:
            start_datetime: Start datetime (YYYY-MM-DDThh:mm:ss)
            end_datetime: End datetime (YYYY-MM-DDThh:mm:ss)
            days_back: Number of days to fetch
        
        Returns:
            List of heart rate data dictionaries
        """
        if end_datetime is None:
            end_datetime = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        
        if start_datetime is None:
            start_datetime = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%dT%H:%M:%S")
        
        try:
            hr_data = self.client.get_heart_rate(start_datetime=start_datetime, end_datetime=end_datetime)
            print(f"✅ Fetched {len(hr_data)} heart rate records ({start_datetime} to {end_datetime})")
            return hr_data
        except Exception as e:
            print(f"❌ Error fetching heart rate data: {e}")
            return []
    
    def get_all_data(self, days_back: int = 90) -> Dict[str, List[Dict[str, Any]]]:
        """
        Fetch all available Oura data
        
        Args:
            days_back: Number of days of historical data to fetch
        
        Returns:
            Dictionary with keys: 'sleep', 'activity', 'readiness', 'heart_rate'
        """
        print("=" * 60)
        print("FETCHING OURA DATA")
        print("=" * 60)
        
        all_data = {
            'sleep': self.get_sleep_data(days_back=days_back),
            'activity': self.get_activity_data(days_back=days_back),
            'readiness': self.get_readiness_data(days_back=days_back),
            'heart_rate': self.get_heart_rate_data(days_back=min(days_back, 7))  # HR data limited
        }
        
        print("\n" + "=" * 60)
        print("DATA FETCH SUMMARY")
        print("=" * 60)
        for key, data in all_data.items():
            print(f"{key.capitalize()}: {len(data)} records")
        
        return all_data
    
    def close(self):
        """Close the API client session"""
        self.client.close()

def main():
    """Example usage"""
    print("Oura API Client Wrapper")
    print("=" * 60)
    print("\nTo use this client:")
    print("1. Get Personal Access Token from: https://cloud.ouraring.com/personal-access-tokens")
    print("2. Set environment variable: export OURA_PERSONAL_ACCESS_TOKEN='your_token'")
    print("3. Or create .env file with: OURA_PERSONAL_ACCESS_TOKEN=your_token")
    print("\nExample:")
    print("  from api_client import OuraDataFetcher")
    print("  fetcher = OuraDataFetcher()")
    print("  sleep_data = fetcher.get_sleep_data(days_back=30)")
    print("  all_data = fetcher.get_all_data(days_back=90)")

if __name__ == '__main__':
    main()

