# Anti-Virus for checking images of users of Pezeshkeh-Khodkar
# MIT License
# Copyright (c) 2023 Pezeshkeh-Khodkar

__version__ = '0.0.1'
__author__ = 'Yasin Bakhtiar, Radin Reisi'

from libs.sec.signature_getter import SignatureGetter
import os
import virustotal_python
from django.conf import settings


class AntiVirus:
    """ Anti-Virus for checking images of users of Pezeshkeh-Khodkar
    """
    def __init__(self):
        # Open API key from a file
        with open(str(settings.BASE_DIR / "libs/sec/API.key"), "r") as key_file:
            self.api_key = key_file.read()

    @staticmethod
    def __check_virustotal_response(response):
        """Check the response of the virus total API
        Args:
            - response: response of virustotal API
        Returns:
            - True: It has a virus
            - False: It doesn't have a virus
        """
        if response.json()["data"]["attributes"]["total_votes"]["malicious"] == 0:
            return False
        else:
            return True

    def check_for_virus(self, file_address: str):
        """ Check file to find virus...
        Args:
            - file_address: The address of file that needs to check

        Returns:
            - True: It has a virus
            - False: It doesn't have a virus
        """

        # Open virus total API
        try:
            vtotal = virustotal_python.Virustotal(self.api_key)
        except Exception as e:
            print(e)
            return True

        # Get SHA256 signature of file
        FileSignature = SignatureGetter.get_signature(open(file_address, mode="rb"))

        try:
            # Request the API
            response = vtotal.request(f"files/{FileSignature}")
            return self.__check_virustotal_response(response)

        except:
            files = {"file": (os.path.basename(file_address), open(os.path.abspath(file_address), "rb"))}

            # If it has (connection error, ...), it will return True.
            try:
                response = vtotal.request("files", files=files, method="POST")

                try:
                    response = vtotal.request(f"files/{FileSignature}")
                    return self.__check_virustotal_response(response)

                except Exception as e:
                    print(e)
                    return True

            except Exception:
                return True
