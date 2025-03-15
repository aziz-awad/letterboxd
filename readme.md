# Letterboxd to Plurk Automation

This repository contains a script that automatically fetches your Letterboxd reviews via RSS and posts them to your Plurk account. The script runs every 15 minutes via GitHub Actions and keeps track of which reviews have already been posted to avoid duplicates.

## Setup Instructions

### 1. Fork this repository

Start by forking this repository to your GitHub account.

### 2. Set up GitHub Secrets

You need to add the following secrets to your GitHub repository:

- `LETTERBOXD_RSS_URL`: Your Letterboxd RSS feed URL (typically `https://letterboxd.com/[username]/rss/`)
- `PLURK_API_KEY`: Your Plurk API key
- `PLURK_API_SECRET`: Your Plurk API secret
- `PLURK_ACCESS_TOKEN`: Your Plurk access token
- `PLURK_ACCESS_TOKEN_SECRET`: Your Plurk access token secret

To add these secrets:
1. Go to your repository on GitHub
2. Click on "Settings" > "Secrets and variables" > "Actions"
3. Click on "New repository secret" and add each of the required secrets

### 3. Getting Plurk API Credentials

1. Register a new Plurk app at: https://www.plurk.com/PlurkApp/
2. After registration, you'll get an API key and API secret
3. Use these credentials to generate an access token and access token secret (this typically requires implementing the OAuth flow)

### 4. Enable GitHub Actions

GitHub Actions should be enabled by default for your forked repository. The workflow will run automatically every 15 minutes.

## How It Works

1. The script fetches your recent Letterboxd reviews from your RSS feed
2. It checks against a list of previously posted reviews stored in `posted_reviews.json`
3. New reviews are posted to your Plurk account
4. The list of posted reviews is updated and committed back to the repository

## Manually Running the Workflow

You can manually trigger the workflow:
1. Go to the "Actions" tab in your repository
2. Select the "Letterboxd to Plurk" workflow
3. Click on "Run workflow"

## Local Development

To run the script locally:

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set the required environment variables
4. Run the script: `python main.py`
