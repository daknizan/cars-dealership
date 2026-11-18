import json
import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel
from .restapis import (
    analyze_review_sentiments,
    get_dealer_by_id_from_cf,
    get_dealer_reviews_from_cf,
    get_dealers_by_state_from_cf,
    get_dealers_from_cf,
    REVIEWS,
)

logger = logging.getLogger(__name__)


def safe_json(request):
    try:
        return json.loads(request.body.decode("utf-8"))
    except Exception:
        return {}


# ------------------------------------------------------------ auth ---------
@csrf_exempt
def login_user(request):
    data = safe_json(request)
    user_name = data.get("userName")
    password = data.get("password")
    user = authenticate(username=user_name, password=password)
    data_resp = {"userName": user_name}
    if user is not None:
        login(request, user)
        data_resp["status"] = "Authenticated"
    else:
        data_resp["status"] = "Failed"
    return JsonResponse(data_resp)


def logout_request(request):
    logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
def registration(request):
    data = safe_json(request)
    username = data.get("userName")
    password = data.get("password")
    first_name = data.get("firstName")
    last_name = data.get("lastName")
    email = data.get("email")

    username_exist = User.objects.filter(username=username).exists()
    if username_exist:
        return JsonResponse({"userName": username, "error": "Already Registered"})

    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        password=password,
        email=email,
    )
    login(request, user)
    return JsonResponse({"userName": username, "status": "Authenticated"})


# ------------------------------------------------------------- cars --------
def get_cars(request):
    count = CarMake.objects.filter().count()
    if count == 0:
        # Peupler la base avec quelques marques/modèles par défaut
        for make_name, models in {
            "Toyota": ["Camry", "Corolla", "RAV4"],
            "Honda": ["Civic", "Accord", "CR-V"],
            "Ford": ["F-150", "Mustang", "Explorer"],
        }.items():
            make = CarMake.objects.create(name=make_name, description=f"Véhicules {make_name}")
            for m in models:
                CarModel.objects.create(
                    car_make=make, dealer_id=1, name=m, type="SUV" if "RAV4" in m or "CR-V" in m else "Sedan", year="2025-01-01"
                )
    car_models = [
        {
            "CarModel": m.name,
            "CarMake": m.car_make.name,
            "DealerId": m.dealer_id,
            "Type": m.type,
            "Year": m.year.year,
        }
        for m in CarModel.objects.select_related("car_make")
    ]
    return JsonResponse({"CarModels": car_models})


# ------------------------------------------------------------ dealers ------
def get_dealers(request):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/capstone/dealership-package/get-dealership"
        dealerships = get_dealers_from_cf(url)
        dealer_list = []
        for dealer in dealerships:
            dealer_obj = {
                "id": dealer.get("id"),
                "city": dealer.get("city"),
                "state": dealer.get("state"),
                "st": dealer.get("st"),
                "address": dealer.get("address"),
                "zip": dealer.get("zip"),
                "lat": dealer.get("lat"),
                "long": dealer.get("long"),
                "short_name": dealer.get("short_name"),
                "full_name": dealer.get("full_name"),
            }
            dealer_list.append(dealer_obj)
        return JsonResponse({"status": 200, "dealers": dealer_list})


def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        dealer = get_dealer_by_id_from_cf(dealer_id)
        if dealer:
            return JsonResponse({"status": 200, "dealer": dealer})
        return JsonResponse({"status": 404, "message": "Dealer not found"})


def get_dealers_by_state(request, state):
    if request.method == "GET":
        dealers = get_dealers_by_state_from_cf(state)
        return JsonResponse({"status": 200, "dealers": dealers})


# ------------------------------------------------------------ reviews ------
def get_dealer_reviews(request, dealer_id):
    if request.method == "GET":
        reviews = get_dealer_reviews_from_cf(dealer_id)
        for review in reviews:
            review["sentiment"] = analyze_review_sentiments(review.get("review", ""))
        return JsonResponse({"status": 200, "reviews": reviews})


@csrf_exempt
def add_review(request):
    if request.method != "POST":
        return JsonResponse({"status": 405, "message": "Method not allowed"})
    if not request.user.is_authenticated:
        return JsonResponse({"status": 403, "message": "Unauthorized"})
    data = safe_json(request)
    review_id = int(data.get("id", len(REVIEWS) + 100))
    sentiment = analyze_review_sentiments(data.get("review", ""))
    review = {
        "id": review_id,
        "name": request.user.username,
        "dealership": data.get("dealership"),
        "review": data.get("review"),
        "purchase": data.get("purchase", False),
        "purchase_date": data.get("purchase_date", ""),
        "car_make": data.get("car_make", ""),
        "car_model": data.get("car_model", ""),
        "car_year": data.get("car_year", 2025),
        "sentiment": sentiment,
    }
    REVIEWS.setdefault(int(data.get("dealership")), []).append(review)
    return JsonResponse({"status": 200, "review": review})


def analyze_sentiment(request, text):
    if request.method == "GET":
        sentiment = analyze_review_sentiments(text)
        return JsonResponse({"text": text, "sentiment": sentiment})
