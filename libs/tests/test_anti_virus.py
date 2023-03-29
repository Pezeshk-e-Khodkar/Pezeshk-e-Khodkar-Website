import django.test
from libs.sec.anti_virus import AntiVirus
import os
import csv  # Work with csv files


class AntiVirusTest(django.test.TestCase):
    """Test of Anti-Virus
    """
    def setUp(self):
        # directory of test images
        self.dir = "libs/tests/test_images/"

        # Load dataset.csv
        self.csv_file = csv.reader(open(os.path.abspath("libs/tests/dataset.csv"), encoding="utf-8"))

        # AntiVirus
        self.av = AntiVirus()

    def test_check_for_virus(self):
        for image in self.csv_file:

            # If it was first row
            if image[0] == "\ufeffFileName":
                continue

            elif image[1] == "1":
                right_answer = True

            elif image[1] == "0":
                right_answer = False

            else:
                raise ValueError

            self.assertEqual(self.av.check_for_virus(os.path.abspath(self.dir + image[0])), right_answer)
