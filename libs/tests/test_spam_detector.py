import django.test
from libs.sec.spam_detector import ImageVerifier, FileSizeVerifier
import csv  # Work with csv file
import os


class ImageVerifierTest(django.test.TestCase):
    def setUp(self):
        # directory of test images
        self.dir = "libs/tests/test_images/"

        # Load dataset.csv
        self.csv_file = csv.reader(open(os.path.abspath("libs/tests/dataset.csv"), encoding="utf-8"))

    def test_verify(self):
        for image in self.csv_file:

            # If it was first row
            if image[0] == "\ufeffFileName":
                continue

            elif image[3] == "1":
                right_answer = True

            elif image[3] == "0":
                right_answer = False

            else:
                raise ValueError

            image = open(self.dir + image[0], "rb")

            self.assertEqual(ImageVerifier.verify(image), right_answer)


class FileSizeVerifierTest(django.test.TestCase):
    def setUp(self):
        # directory of test images
        self.dir = "libs/tests/test_images/"

        # Load dataset.csv
        self.csv_file = csv.reader(open(os.path.abspath("libs/tests/dataset.csv"), encoding="utf-8"))

    def test_verifyFileSize(self):

        for file in self.csv_file:

            # If it was first row
            if file[0] == "\ufeffFileName":
                continue

            elif file[4] == "1":
                right_answer = True

            elif file[4] == "0":
                right_answer = False

            else:
                raise ValueError

            image = open(self.dir + file[0], "rb")
            self.assertEqual(FileSizeVerifier.verifyFileSize(image), right_answer)
