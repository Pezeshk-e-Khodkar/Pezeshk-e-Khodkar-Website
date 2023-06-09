# Import django test library
import django.test

from libs.controller.asd import SkinCancerDetector
import os
import csv  # Work with csv files
from decouple import config  # Use configs from .env file


class SkinCancerDetectorTest(django.test.TestCase):
    """Test of ASD class
    Raise:
        - ValueError: dataset.csv is broke.
    """
    def setUp(self):
        # Load AI model
        self.asd = SkinCancerDetector("models/"+config("SKINCANCER_AI_MODEL"))

        # directory of test images
        self.dir = "libs/tests/test_images/"

        # Load dataset.csv
        self.csv_file = csv.reader(open(os.path.abspath("libs/tests/dataset.csv"), encoding="utf-8"))

    def test_detect(self):
        for image in self.csv_file:

            # If it was first row
            if image[0] == "\ufeffFileName":
                continue

            elif image[2] == "1":
                right_answer = True

            elif image[2] == "0":
                right_answer = False

            else:
                raise ValueError

            if right_answer is False:
                address = self.dir + image[0]
                self.assertEqual(self.asd.detect(open(address, "rb"), address, image[0].split('.')[1], 1),
                                 "Error: File was not an image.")
