# Anti-Virus for checking images of users of Pezeshk-e-Khodkar
# MIT License
# Copyright (c) 2023 Pezeshk-e-Khodkar

# To get signature of the file
from libs.sec.signature_getter import SignatureGetter
import os

# To use virus_total API
import virustotal_python

# To get configs form .env file
from decouple import config


class AntiVirus:
    """ Anti-Virus for checking users' images of Pezeshk-e-Khodkar
    """
    def __init__(self):
        # Open API key from .env file
        self.api_key = config("VIRUSTOTAL_API_KEY")

    @staticmethod
    def __check_virustotal_response(response):
        """Check the response of the virus total API
        Args:
            - response: response of the virustotal API
        Returns:
            - True: It has a virus
            - False: It doesn't have a virus
        """
        if response.json()["data"]["attributes"]["total_votes"]["malicious"] == 0:
            return False
        else:
            return True

    def check_for_virus(self, file_address: str):
        """ Check the file to find virus...
        Args:
            - file_address: The address of file that needs to check

        Returns:
            - True: It has a virus
            - False: It doesn't have a virus
        """

        # Try to open virus total API
        try:
            vtotal = virustotal_python.Virustotal(self.api_key)
        except Exception as e:
            print(e)
            return True

        # Get SHA256 signature of the file
        FileSignature = SignatureGetter.get_signature(open(file_address, mode="rb"))

        # Try to request the API
        try:
            # Request the API
            response = vtotal.request(f"files/{FileSignature}")
            return self.__check_virustotal_response(response)

        except:
            files = {"file": (os.path.basename(file_address), open(os.path.abspath(file_address), "rb"))}

            # If it (connection error, ...), it will return True.
            try:
                vtotal.request("files", files=files, method="POST")

                try:
                    response = vtotal.request(f"files/{FileSignature}")
                    return self.__check_virustotal_response(response)

                except Exception as e:
                    print(e)
                    return True

            except Exception as e:
                print(e)
                return True
