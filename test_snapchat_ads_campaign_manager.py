import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import json

# Import the functions we want to test
from snapchat_ads_campaign_manager import get_campaigns, get_campaign_stats, pause_campaign, main

class TestSnapchatAdsCampaignManager(unittest.TestCase):

    def setUp(self):
        self.mock_campaign = {
            "campaign": {
                "id": "test_campaign_id",
                "name": "Test Campaign"
            }
        }
        self.mock_stats = {
            "timeseries_stats": [{
                "spend": "100.0",
                "conversion_purchases_value": "150.0"
            }]
        }

    @patch('snapchat_ads_campaign_manager.requests.get')
    def test_get_campaigns(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"campaigns": [self.mock_campaign]}
        mock_get.return_value = mock_response

        campaigns = get_campaigns()
        self.assertEqual(len(campaigns), 1)
        self.assertEqual(campaigns[0]['campaign']['id'], 'test_campaign_id')

    @patch('snapchat_ads_campaign_manager.requests.get')
    def test_get_campaign_stats(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = self.mock_stats
        mock_get.return_value = mock_response

        stats = get_campaign_stats('test_campaign_id')
        self.assertEqual(stats['spend'], '100.0')
        self.assertEqual(stats['conversion_purchases_value'], '150.0')

    @patch('snapchat_ads_campaign_manager.requests.post')
    def test_pause_campaign(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"campaign": {"status": "PAUSED"}}
        mock_post.return_value = mock_response

        result = pause_campaign('test_campaign_id')
        self.assertEqual(result['campaign']['status'], 'PAUSED')

    @patch('snapchat_ads_campaign_manager.get_campaigns')
    @patch('snapchat_ads_campaign_manager.get_campaign_stats')
    @patch('snapchat_ads_campaign_manager.pause_campaign')
    @patch('snapchat_ads_campaign_manager.logging')
    def test_main_function(self, mock_logging, mock_pause, mock_stats, mock_campaigns):
        # Test case 1: ROAS > 1, should not pause
        mock_campaigns.return_value = [self.mock_campaign]
        mock_stats.return_value = {"spend": "100.0", "conversion_purchases_value": "150.0"}
        
        main()
        
        mock_pause.assert_not_called()
        mock_logging.info.assert_any_call("Campaign test_campaign_id - ROAS: £1.50")
        mock_logging.info.assert_any_call("Campaign test_campaign_id ROAS is above threshold, no action taken")

        # Test case 2: ROAS < 1, should pause
        mock_stats.return_value = {"spend": "100.0", "conversion_purchases_value": "50.0"}
        
        main()
        
        mock_pause.assert_called_once_with('test_campaign_id')
        mock_logging.info.assert_any_call("Campaign test_campaign_id - ROAS: £0.50")
        mock_logging.info.assert_any_call("Pausing campaign test_campaign_id due to low ROAS")

    @patch('snapchat_ads_campaign_manager.requests.get')
    def test_api_error_handling(self, mock_get):
        mock_get.side_effect = Exception("API Error")

        with self.assertRaises(Exception):
            get_campaigns()

if __name__ == '__main__':
    unittest.main()
