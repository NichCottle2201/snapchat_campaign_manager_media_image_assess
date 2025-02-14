import os
from datetime import datetime, timedelta
from api_client import SnapAdsAPIClient
from campaign_manager import check_and_pause_campaigns

def main():
    # Configuration – these would normally be set as environment variables or config file.
    ACCESS_TOKEN = os.getenv("SNAPCHAT_ACCESS_TOKEN", "YOUR_ACCESS_TOKEN")
    ACCOUNT_ID = "380h9661-436e-51eb-0g7c-42d5b97f219c"
    
    # Calculate date range: last 30 days (excluding today)
    today = datetime.utcnow().date()
    end_date = today - timedelta(days=1)
    start_date = today - timedelta(days=30)
    
    # Format dates as required by the API (e.g., YYYY-MM-DD)
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")
    
    client = SnapAdsAPIClient(access_token=ACCESS_TOKEN, account_id=ACCOUNT_ID)
    
    # Check campaigns and pause those below ROAS threshold.
    check_and_pause_campaigns(client, roas_threshold=1.0, start_date=start_date_str, end_date=end_date_str)

if __name__ == "__main__":
    main()
