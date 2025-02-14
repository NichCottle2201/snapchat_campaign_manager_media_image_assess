import requests
from datetime import datetime, timedelta
import logging

# logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Snapchat Ads API configuration
BASE_URL = "https://adsapi.snapchat.com/v1"
ACCOUNT_ID = "380h9661-436e-51eb-0g7c-42d5b97f219c"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN_HERE"  # NOT MAKING USE OF STANDARD ENVIRONMENT FILE AS PER USUAL IN DEV & PROD ENVIROS

# date range
end_date = datetime.now().date() - timedelta(days=1)
start_date = end_date - timedelta(days=30)

def get_campaigns():
    url = f"{BASE_URL}/adaccounts/{ACCOUNT_ID}/campaigns"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["campaigns"]

def get_campaign_stats(campaign_id):
    url = f"{BASE_URL}/campaigns/{campaign_id}/stats"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    params = {
        "fields": "spend,conversion_purchases_value",
        "start_time": start_date.isoformat(),
        "end_time": end_date.isoformat(),
        "granularity": "TOTAL"
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()["timeseries_stats"][0]

def pause_campaign(campaign_id):
    url = f"{BASE_URL}/campaigns/{campaign_id}"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {"campaign": {"status": "PAUSED"}}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

def main():
    try:
        campaigns = get_campaigns()
        logging.info(f"Found {len(campaigns)} campaigns")

        for campaign in campaigns:
            campaign_id = campaign["campaign"]["id"]
            stats = get_campaign_stats(campaign_id)
            
            spend = float(stats["spend"])
            conversion_value = float(stats["conversion_purchases_value"])
            
            if spend > 0:
                roas = conversion_value / spend
            else:
                roas = 0

            logging.info(f"Campaign {campaign_id} - ROAS: £{roas:.2f}")

            if roas < 1:
                logging.info(f"Pausing campaign {campaign_id} due to low ROAS")
                pause_campaign(campaign_id)
            else:
                logging.info(f"Campaign {campaign_id} ROAS is above threshold, no action taken")

    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise

if __name__ == "__main__":
    main()
