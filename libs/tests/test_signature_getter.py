import django.test
from libs.sec.signature_getter import SignatureGetter
import csv  # Work with csv files
import os


class SignatureGetterTest(django.test.TestCase):

    def setUp(self):
        # directory of test images
        self.dir = "libs/tests/test_images/"

        # Load csv file
        self.csv_file = csv.reader(open(os.path.abspath("libs/tests/dataset.csv"), encoding="utf-8"))

    def test_get_signature(self):
        for image in self.csv_file:

            if image[0] == "\ufeffFileName":
                continue

            # It generates signature twice: 1. with opened file
            #                               2. with file address
            # Len of sha256 should be 64.
            signature = SignatureGetter.get_signature(self.dir+image[0])
            signature_2 = SignatureGetter.get_signature(open(self.dir+image[0], mode="rb"))
            self.assertEqual(len(signature), 64)
            self.assertEqual(len(signature_2), 64)
