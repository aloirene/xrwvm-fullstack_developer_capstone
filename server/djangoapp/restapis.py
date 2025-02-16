import requests
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/")

def get_request(endpoint, **kwargs):
    params = ""
    if(kwargs):
        for key,value in kwargs.items():
            params=params+key+"="+value+"&"

    request_url = backend_url+endpoint+"?"+params

    print("GET from {} ".format(request_url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except:
        # If any error occurs
        print("Network exception occurred")

def analyze_review_sentiments(text):
    """
    Analyze the sentiment of a given text using the sentiment analyzer microservice.
    """
    if not text:
        return "Neutral"  # Default sentiment if text is empty

    request_url = f"{sentiment_analyzer_url}analyze/{text}"
    print(f"Analyzing sentiment for: {text}")

    try:
        response = requests.get(request_url)
        response.raise_for_status()
        sentiment_response = response.json()
        return sentiment_response.get("sentiment", "Neutral")  # Default to Neutral if missing
    except requests.exceptions.RequestException as e:
        print(f"Error analyzing sentiment: {e}")
        return "Neutral"

def post_review(data_dict):
    """
    Posts a dealership review to the backend.
    """
    request_url = backend_url + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        print(response.json())  # Debug print
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Network exception occurred: {e}")
        return {"error": "Network error"}