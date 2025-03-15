import os
import json
import feedparser
import requests
from datetime import datetime
import sys
from typing import List, Dict, Any

# Config
LETTERBOXD_RSS_URL = os.environ.get("LETTERBOXD_RSS_URL")
# PLURK_API_KEY = os.environ.get("PLURK_API_KEY")
# PLURK_API_SECRET = os.environ.get("PLURK_API_SECRET")
# PLURK_ACCESS_TOKEN = os.environ.get("PLURK_ACCESS_TOKEN")
# PLURK_ACCESS_TOKEN_SECRET = os.environ.get("PLURK_ACCESS_TOKEN_SECRET")
DATA_FILE = "posted_reviews.json"
PLURK_API_URL = "https://www.plurk.com/APP/Timeline/plurkAdd"

class LetterboxdReview:
    def __init__(self, title: str, link: str, description: str, published: str, id: str):
        self.title = title
        self.link = link
        self.description = description
        self.published = published
        self.id = id
    
    def __repr__(self):
        return f"Review('{self.title}', {self.id})"

    def to_dict(self) -> Dict[str, str]:
        return {
            "title": self.title,
            "link": self.link,
            "description": self.description,
            "published": self.published,
            "id": self.id
        }

def load_posted_reviews() -> List[str]:
    """Load the list of already posted review IDs from the data file."""
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            return data.get("posted_reviews", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_posted_reviews(posted_reviews: List[str]) -> None:
    """Save the list of posted review IDs to the data file."""
    with open(DATA_FILE, 'w') as f:
        json.dump({"posted_reviews": posted_reviews}, f, indent=2)

def fetch_letterboxd_reviews() -> List[LetterboxdReview]:
    """Fetch reviews from the Letterboxd RSS feed."""
    if not LETTERBOXD_RSS_URL:
        print("Error: LETTERBOXD_RSS_URL environment variable not set")
        sys.exit(1)
    
    print(f"Fetching reviews from {LETTERBOXD_RSS_URL}")
    feed = feedparser.parse(LETTERBOXD_RSS_URL)
    
    reviews = []
    for entry in feed.entries:
        review = LetterboxdReview(
            title=entry.title,
            link=entry.link,
            description=entry.get('description', ''),
            published=entry.get('published', ''),
            id=entry.id
        )
        reviews.append(review)
    
    print(f"Found {len(reviews)} reviews in the feed")
    return reviews

def post_to_plurk(review: LetterboxdReview) -> bool:
    """Post a review to Plurk using the Plurk API."""
    if not all([PLURK_API_KEY, PLURK_API_SECRET, PLURK_ACCESS_TOKEN, PLURK_ACCESS_TOKEN_SECRET]):
        print("Error: Plurk API credentials are not properly set in environment variables")
        sys.exit(1)
    
    # Format content for Plurk
    content = f"I watched {review.title} - {review.description[:100]}... {review.link}"
    
    # Set up OAuth for Plurk
    from requests_oauthlib import OAuth1
    auth = OAuth1(
        PLURK_API_KEY,
        client_secret=PLURK_API_SECRET,
        resource_owner_key=PLURK_ACCESS_TOKEN,
        resource_owner_secret=PLURK_ACCESS_TOKEN_SECRET
    )
    
    # Post to Plurk
    data = {
        "content": content,
        "qualifier": "watches",
        "limited_to": None
    }
    
    try:
        response = requests.post(PLURK_API_URL, auth=auth, data=data)
        response.raise_for_status()
        print(f"Successfully posted to Plurk: {review.title}")
        return True
    except requests.RequestException as e:
        print(f"Error posting to Plurk: {e}")
        return False

def main():
    # Load previously posted reviews
    posted_review_ids = load_posted_reviews()
    print(f"Found {len(posted_review_ids)} previously posted reviews")
    
    # Fetch recent reviews
    reviews = fetch_letterboxd_reviews()
    
    # Filter out already posted reviews
    new_reviews = [review for review in reviews if review.id not in posted_review_ids]
    print(f"Found {len(new_reviews)} new reviews to post")
    
    # Post new reviews to Plurk
    newly_posted = []
    for review in new_reviews:
        success = post_to_plurk(review)
        if success:
            posted_review_ids.append(review.id)
            newly_posted.append(review.to_dict())
    
    # Save updated list of posted reviews
    save_posted_reviews(posted_review_ids)
    
    # Print summary
    print(f"Posted {len(newly_posted)} new reviews to Plurk")
    print(f"Total posted reviews: {len(posted_review_ids)}")
    
    # Return for logging purposes
    return {
        "timestamp": datetime.now().isoformat(),
        "new_reviews_posted": len(newly_posted),
        "newly_posted": newly_posted,
        "total_posted": len(posted_review_ids)
    }

if __name__ == "__main__":
    result = main()
    print(json.dumps(result, indent=2))
