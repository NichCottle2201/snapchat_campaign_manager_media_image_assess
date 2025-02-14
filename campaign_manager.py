import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def calculate_roas(campaign: dict) -> float:
    """
    Calculate ROAS for a campaign.
    ROAS = conversion_purchases_value / spend
    If spend is zero, returns 0.
    """
    spend = campaign.get("spend", 0)
    conversion_value = campaign.get("conversion_purchases_value", 0)
    if spend == 0:
        return 0.0
    return conversion_value / spend

def check_and_pause_campaigns(client, roas_threshold: float = 1.0, start_date: str = None, end_date: str = None):
    """
    Retrieves campaign performance stats for the given date range,
    calculates ROAS and pauses campaigns that fall below the threshold.
    """
    campaigns = client.get_campaign_stats(start_date, end_date)
    for campaign in campaigns:
        campaign_id = campaign.get("campaign_id")
        roas = calculate_roas(campaign)
        logger.info(f"Campaign {campaign_id}: ROAS = {roas:.2f}")
        if roas < roas_threshold:
            logger.info(f"Pausing campaign {campaign_id} as ROAS ({roas:.2f}) is below threshold ({roas_threshold}).")
            try:
                pause_response = client.pause_campaign(campaign_id)
                logger.info(f"Campaign {campaign_id} paused successfully. Response: {pause_response}")
            except Exception as e:
                logger.error(f"Error pausing campaign {campaign_id}: {e}")
  
