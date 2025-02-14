import requests
import datetime

class SnapAdsAPIClient:
    def __init__(self, access_token: str, account_id: str, base_url: str = "https://adsapi.snapchat.com/v1"):
        self.access_token = access_token
        self.account_id = account_id
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
    
    def get_campaign_stats(self, start_date: str, end_date: str):
        """
        Fetches campaign performance stats for the given date range.
        The API is assumed to return a JSON payload with a list of campaigns, each having:
         - campaign_id (str)
         - conversion_purchases_value (float)
         - spend (float)
        """
        # Build URL – adjust endpoint as per actual API documentation.
        url = f"{self.base_url}/stats"
        params = {
            "account_id": self.account_id,
            "start_date": start_date,
            "end_date": end_date,
            # Additional query parameters may be needed
        }
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Assume data structure: {"campaigns": [{...}, {...}, ...]}
        return data.get("campaigns", [])
    
    def pause_campaign(self, campaign_id: str):
        """
        Pauses a campaign by its ID.
        """
        # Build URL – adjust endpoint as per actual API documentation.
        url = f"{self.base_url}/campaigns/{campaign_id}/pause"
        
        response = requests.post(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
