from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
import logging
import json
from .populate import initiate
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review  # Import functions

# Get an instance of a logger
logger = logging.getLogger(__name__)

# 🚀 Login user
@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    
    user = authenticate(username=username, password=password)
    response_data = {"userName": username}

    if user is not None:
        login(request, user)
        response_data["status"] = "Authenticated"
    
    return JsonResponse(response_data)

# 🚀 Logout user
def logout_request(request):
    logout(request)
    user_name = request.user.username if request.user.is_authenticated else ""
    return JsonResponse({"userName": user_name})

# 🚀 Register user
@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']

    try:
        User.objects.get(username=username)
        return JsonResponse({"error": "Username already registered", "userName": username})
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email
        )
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})

#Update the `get_dealerships` render list of dealerships all by default, particular state if state is passed
def get_dealerships(request, state="All"):
    """
    Fetch list of dealerships.
    """
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)

    # Debugging output
    print(f"🔍 API Request: {endpoint}")  # What API path is called?
    print(f"🔍 Raw API Response: {dealerships}")  # What does the API return?

    return JsonResponse({"status": 200, "dealers": dealerships})
# 🚀 Get dealer details by ID
def get_dealer_details(request, dealer_id):
    if(dealer_id):
        endpoint = "/fetchDealer/"+str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status":200,"dealer":dealership})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})
        
# 🚀 Get dealer reviews by ID
def get_dealer_reviews(request, dealer_id):
    """
    Fetch dealer reviews using the /fetchReviews/dealer/<dealer_id> endpoint.
    Analyze the sentiment of each review and return the results.
    """
    reviews_endpoint = f"/fetchReviews/dealer/{dealer_id}"
    reviews_data = get_request(reviews_endpoint)

    if not reviews_data:
        return JsonResponse({"error": "No reviews found"}, status=404)

    processed_reviews = []
    for review in reviews_data:
        sentiment = analyze_review_sentiments(review.get("review", ""))
        review_detail = {
            "id": review.get("id"),
            "dealer_id": review.get("dealer_id"),
            "review": review.get("review"),
            "sentiment": sentiment,
            "name": review.get("name"),
            "purchase": review.get("purchase"),
            "purchase_date": review.get("purchase_date"),
            "car_make": review.get("car_make"),
            "car_model": review.get("car_model"),
            "car_year": review.get("car_year")
        }
        processed_reviews.append(review_detail)

    return JsonResponse({"reviews": processed_reviews}, safe=False)

# 🚀 Submit a dealership review
@csrf_exempt
def add_review(request):
    if request.user.is_authenticated:
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status": 200, "message": "Review submitted successfully", "response": response})
        except Exception as e:
            return JsonResponse({"status": 500, "message": f"Error in posting review: {str(e)}"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})

def get_cars(request):
    """
    Fetch a list of car models from the database.
    """
    cars = list(CarModel.objects.all().values())  # Convert QuerySet to list
    return JsonResponse({"cars": cars})