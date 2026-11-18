from django.test import TestCase


class SmokeTest(TestCase):
    def test_get_dealers(self):
        response = self.client.get("/djangoapp/get_dealers")
        self.assertEqual(response.status_code, 200)

    def test_sentiment(self):
        response = self.client.get("/djangoapp/sentiment/Services fantastiques")
        self.assertEqual(response.json()["sentiment"], "positive")
