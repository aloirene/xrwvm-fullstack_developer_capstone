import requests
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/")

def get_request(endpoint, **kwargs):
    """
    Generic function to make GET requests to an external API.
    """
    request_url = backend_url + endpoint
    print(f"🔍 GET request to: {request_url}")

    try:
        response = requests.get(request_url, params=kwargs)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching data: {e}")
        return None

def analyze_review_sentiments(text):
    """
    Analyze the sentiment of a given text using the sentiment analyzer microservice.
    """
    if not text:
        return "Neutral"

    request_url = f"{sentiment_analyzer_url}/analyze/{text}"
    print(f"🔍 Analyzing sentiment for: {text}")

    try:
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json().get("sentiment", "Neutral")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error analyzing sentiment: {e}")
        return "Neutral"

def post_review(data_dict):
    """
    Posts a dealership review to the backend.
    """
    request_url = backend_url + "/insert_review"
    print(f"🚀 Posting review to {request_url}")

    try:
        response = requests.post(request_url, json=data_dict)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Network exception occurred: {e}")
        return {"error": "Network error"}