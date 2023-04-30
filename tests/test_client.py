from django.test.client import Client  # Use it to test Pezeshk-e-Khodkar-Webaite
from django.test import TestCase # Unittest in Django
import ast
from libs.sec.anti_virus import AntiVirus


class APITest(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)

    def test_pages(self):
        # Test Home Page
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)

        # Test Error Page
        res = self.client.get("/INCORRECT")
        self.assertEqual(res.status_code, 404)

        # Test Post Request
        res = self.client.post("/")
        self.assertEqual(res.status_code, 405)

    def test_api(self):

        # Open test images
        uncorrupted_img = open("tests/uncorrupted.jpg", "rb")
        corrupted_img = open("tests/corrupted.jpg", "rb")
        print(AntiVirus().check_for_virus("tests/uncorrupted.jpg"))

        # Test API with get method
        res = self.client.get("/api/?img=none")
        self.assertEqual(res.status_code, 405)

        # Test API with no disease_type and image
        res = self.client.post("/api/")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(ast.literal_eval(res.content.decode("utf-8"))["details"], "Request has no disease_type")

        # Test API with no disease_type
        uncorrupted_img.seek(0)
        res = self.client.post("/api/", {"img": uncorrupted_img})
        self.assertEqual(res.status_code, 400)
        self.assertEqual(ast.literal_eval(res.content.decode("utf-8"))["details"], "Request has no disease_type")

        # Test API with no image
        res = self.client.post("/api/", {"disease_type": "SkinCancer"})
        self.assertEqual(res.status_code, 400)
        self.assertEqual(ast.literal_eval(res.content.decode("utf-8"))["details"], "Request has no resource file attached called (img)")

        # Test with incorrect disease_type
        uncorrupted_img.seek(0)
        res = self.client.post("/api/", {"img": uncorrupted_img, "disease_type": "INCORRECT"})
        self.assertEqual(res.status_code, 400)
        self.assertEqual(ast.literal_eval(res.content.decode("utf-8"))["details"], "disease_type is wrong")

        # Test with incorrect image
        corrupted_img.seek(0)
        res = self.client.post("/api/", {"img": corrupted_img, "disease_type": "SkinCancer"})
        self.assertEqual(res.status_code, 400)

        # Test with incorrect image and disease_type
        corrupted_img.seek(0)
        res = self.client.post("/api/", {"img": corrupted_img, "disease_type": "INCORRECT"})
        self.assertEqual(res.status_code, 400)

        # Test with correct data
        uncorrupted_img.seek(0)
        res = self.client.post("/api/", {"img": uncorrupted_img, "disease_type": "SkinCancer"})
        self.assertEqual(res.status_code, 200)
