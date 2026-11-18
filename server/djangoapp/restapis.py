"""Helpers: récupération des dealers + analyse de sentiment.

Si aucune base Cloudant n'est configurée, une liste MOCK de concessionnaires
est utilisée afin que le projet fonctionne immédiatement en local.
"""

import requests
from django.conf import settings

# ---------------------------------------------------------------- dealers --
# Données mock (remplacer par l'appel à votre base Cloudant/CouchDB)
DEALERS = [
    {"id": 1, "city": "Overland Park", "state": "Kansas", "st": "KS", "address": "1234 Oak Street", "zip": "66210", "lat": 38.9822, "long": -94.6708, "short_name": "Premier Auto", "full_name": "Premier Auto Dealership"},
    {"id": 2, "city": "Wichita", "state": "Kansas", "st": "KS", "address": "456 Elm Avenue", "zip": "67202", "lat": 37.6872, "long": -97.3301, "short_name": "Heartland Motors", "full_name": "Heartland Motors Wichita"},
    {"id": 3, "city": "Dallas", "state": "Texas", "st": "TX", "address": "789 Pine Road", "zip": "75201", "lat": 32.7767, "long": -96.7970, "short_name": "Lone Star Cars", "full_name": "Lone Star Cars Dallas"},
    {"id": 4, "city": "Austin", "state": "Texas", "st": "TX", "address": "1010 Cedar Lane", "zip": "78701", "lat": 30.2672, "long": -97.7431, "short_name": "Hill Country Auto", "full_name": "Hill Country Auto Austin"},
]

# Avis stockés en mémoire (id -> liste d'avis)
REVIEWS = {
    1: [
        {"id": 1, "name": "Alice Martin", "dealership": 1, "review": "Services fantastiques", "purchase": True, "purchase_date": "2026-05-12", "car_make": "Toyota", "car_model": "Camry", "car_year": 2025, "sentiment": "positive"},
    ],
}


def get_request(url):
    try:
        r = requests.get(url, timeout=10)
        return r.status_code, r.json()
    except Exception:
        return 500, []


def get_dealers_from_cf(url=None):
    return DEALERS


def get_dealer_by_id_from_cf(dealer_id):
    return next((d for d in DEALERS if d["id"] == dealer_id), None)


def get_dealers_by_state_from_cf(state):
    return [d for d in DEALERS if d["state"].lower() == state.lower() or d["st"].lower() == state.lower()]


def get_dealer_reviews_from_cf(dealer_id):
    return REVIEWS.get(dealer_id, [])


# ------------------------------------------------------------- sentiment --
def analyze_review_sentiments(text):
    """Analyse de sentiment via Watson NLU si configuré, sinon règles locales."""
    if settings.WATSON_NLU_URL and settings.WATSON_NLU_APIKEY:
        url = f"{settings.WATSON_NLU_URL}/v1/analyze?version=2022-04-07"
        headers = {"Content-Type": "application/json"}
        auth = ("apikey", settings.WATSON_NLU_APIKEY)
        payload = {
            "text": text,
            "features": {"sentiment": {}},
            "language": "fr",
        }
        try:
            r = requests.post(url, json=payload, headers=headers, auth=auth, timeout=15)
            return r.json()["sentiment"]["document"]["label"]
        except Exception:
            pass
    # Fallback local : mots-clés positifs/négatifs
    positive_words = {"fantastique", "fantastiques", "excellent", "parfait", "super", "great", "amazing", "good", "love", "perfect"}
    negative_words = {"mauvais", "horrible", "terrible", "bad", "awful", "worst", "poor"}
    lower = text.lower()
    if any(w in lower for w in negative_words):
        return "negative"
    if any(w in lower for w in positive_words):
        return "positive"
    return "neutral"
