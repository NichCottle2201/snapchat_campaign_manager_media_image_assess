# Snapchat Ads API Campaign Manager

## Overview

This Python script integrates with the Snapchat Ads API to automate campaign management based on Return on Ad Spend (ROAS). Specifically, it pauses all campaigns in a specified account that have a ROAS of less than £1 over the last 30 days (excluding today).

## Features

- Fetches all campaigns for a specified Snapchat Ads account
- Calculates ROAS for each campaign over the last 30 days
- Automatically pauses campaigns with ROAS < 1
- Provides logging for actions and errors

## Requirements

- Python 3.6+
- Packages listed in `requirements.txt

## Setup

1. Clone this repository or download the script.

2. Install the required library:

   \`\`\`
   pip install requests
   \`\`\`

3. Set up your Snapchat Ads API credentials:
   - Obtain an access token from the Snapchat Ads API
   - Replace `YOUR_ACCESS_TOKEN_HERE` in the script with your actual access token

4. Configure the account ID:
   - The script is pre-configured with the account ID: `380h9661-436e-51eb-0g7c-42d5b97f219c`
   - If you need to use a different account, update the `ACCOUNT_ID` variable in the script

## Usage

Run the script using Python:

\`\`\`
python media_image_auto_dev_assess_snapAdcampaign_NichCottle.py
\`\`\`

The script will:
1. Fetch all campaigns for the specified account
2. Calculate ROAS for each campaign over the last 30 days
3. Pause any campaigns with ROAS < 1
4. Log all actions and any errors

## Logging

The script uses Python's built-in logging module. Logs are printed to the console and include:
- Information about each campaign's ROAS
- Actions taken (e.g., pausing a campaign)
- Any errors encountered during execution

## Scheduling

To run this script regularly:
- On Unix-like systems, you can set up a cron job
- On Windows, you can use Task Scheduler
- Alternatively, you can use cloud-based scheduling services like AWS Lambda with CloudWatch Events or Google Cloud Functions with Cloud Scheduler

## Security Standardization

- Never commit the access token to version control (gitignore applied)
- In a production & dev enviros, must use environment variables to handle the access token

## Snap Rate Limiting Warning

Be aware of Snapchat Ads API rate limits. If you're dealing with a large number of campaigns, you may need to implement rate limiting in your script.

## Testing

This project includes a suite of unit tests to ensure the correct functioning of the code. 
The tests use Python's built-in `unittest` framework and mock API responses to test the functionality without making actual API calls.

To run the tests:

1. Ensure you're in the project directory
2. Run the following command:

   \`\`\`
   python -m unittest test_snapchat_ads_campaign_manager.py
   \`\`\`

The tests cover:
- Fetching campaigns
- Getting campaign stats
- Pausing campaigns
- The main function's logic for different ROAS scenarios
- Error handling
