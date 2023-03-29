import django.test

from libs.controller.img_uploader import ImageUploader
import os
import csv  # Work with csv files


class ImageUploaderTest(django.test.TestCase):
    def setUp(self):
        # directory of test images
        self.dir = "libs/tests/test_images/"

        # Load dataset.csv
        self.csv_file = csv.reader(open(os.path.abspath("libs/tests/dataset.csv"), encoding="utf-8"))

    def test_img_status(self):
        for i in self.csv_file:

            # If it was first row
            if i[0] == "\ufeffFileName":
                continue

            elif i[5] == "1":
                right_answer = True

            elif i[5] == "0":
                right_answer = False

            else:
                raise ValueError

            # Open image
            image = open(self.dir + i[0], "rb")

            # Upload
            uploader = ImageUploader(image, os.path.abspath("libs/tests/output_images").replace("\\", "/"), "SkinCancer")
            self.assertEqual(uploader.img_status, right_answer)

    def test_img_address(self):
        for i in self.csv_file:

            # If it was first row
            if i[0] == "\ufeffFileName":
                continue

            elif i[5] == "1":
                right_answer = True

            elif i[5] == "0":
                right_answer = False

            else:
                raise ValueError

            # Open Image
            image = open(self.dir + i[0], mode="rb")

            # Upload
            uploader = ImageUploader(image, os.path.abspath("libs/tests/output_images").replace("\\", "/"), "SkinCancer")

            if right_answer:
                self.assertNotEqual(open(uploader.img_address, "rb"), OSError)
            else:
                self.assertEqual(uploader.img_address, None)
