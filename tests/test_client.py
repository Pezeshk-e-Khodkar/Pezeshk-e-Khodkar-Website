# Use it to test Pezeshk-e-Khodkar-Website
from django.test.client import Client

# Unittest in Django
from django.test import TestCase

from decouple import config


class ClientTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_pages(self):
        # Test home page
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)

        # Test help page
        res = self.client.get("/help/")
        self.assertEqual(res.status_code, 200)

        # Test login page
        res = self.client.get("/login/")
        self.assertEqual(res.status_code, 200)

        # Test register page
        res = self.client.get("/register/")
        self.assertEqual(res.status_code, 200)

        # Test incorrect activate page
        res = self.client.get("/activate/INCORRECT/INCORRECT/")
        self.assertEqual(res.status_code, 200)

        # Test incorrect password_reset page
        res = self.client.get("/password_reset/INCORRECT/INCORRECT/")
        self.assertEqual(res.status_code, 200)

        # Test error page
        res = self.client.get("/INCORRECT/")
        self.assertEqual(res.status_code, 404)
