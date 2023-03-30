# Image uploader 


# Import pillow module to work with images
from PIL import Image

import datetime
import os
import io

from libs.sec.sec_manager import SecurityManager
import random

from libs.sec.signature_getter import SignatureGetter

import ast
from api.models import Result
import logging


class ImageUploader(SecurityManager):
    """Upload images to server

    Usage:
        src = open("file/address.png")
        save_address = '/path/'
        img_uploader = ImgUploader(src, save_address)
        print(img_uploader.img_status)

    Arg:
        - src: opened image
        - save_address: saved image address
        - disease_type: Type of disease
    """
    diseases = ['SkinCancer']

    def __init__(self, src: io.BytesIO, save_address: str, disease_type: str):
        super(SecurityManager, self).__init__()

        self.src = src
        self.__img_address = ''
        self.__img_status = False
        self.save_address = save_address

        if disease_type in self.diseases:
            self.disease_type = disease_type
        else:
            raise ValueError(disease_type + " doesn't exist.")

        self.__upload_and_validate_image()

    def __upload_and_validate_image(self):
        """Upload Image
        """

        # If file was an image and its size was smaller than 4mg:
        if self.verify(self.src) and self.verifyFileSize(self.src):
            # Search signature database to find image if it exists
            self.search_result = self.__search_signature()
            if self.search_result is not False:
                self.__img_status = None
                self.__img_address = None
            else:
                # Upload the image to server
                self.__upload()

                # If the image has a virus:
                if self.check_for_virus(self.__img_address):
                    self.__remove_img()
                    self.__img_status = False
                    self.__img_address = None
                else:
                    self.__img_status = True

        else:
            self.__img_status = False
            self.__img_address = None

    @property
    def img_status(self):
        """Did image saved or not?

        Returns:
            - True: It saved successfully.
            - False: It didn't saved.
        """
        return self.__img_status

    @property
    def img_address(self):
        """ The address of the saved image
        Returns:
            - The address of the saved image
        """
        return self.__img_address

    def __upload(self):
        """Upload the image to server
        """
        self.__name_image()

        img = Image.open(self.src)
        img.save(self.__img_address)

    def __remove_img(self):
        """Remove the image from server
        """
        os.remove(self.__img_address)

    def __name_image(self):
        """Name the image
        """
        img = Image.open(self.src)

        # Create a name and address for image (it uses date to name images)
        if self.save_address[-1] != "/":
            self.save_address += "/"

        name = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + str(random.randint(1, 9999999999))

        self.__img_address = self.save_address + name + '.' + img.format

    def __search_signature(self):
        """Search signature of image in database
        Returns:
            - False: If signature doesn't exist.
            - Dictionary: result of image
        """
        self.src.seek(0)

        # Get signature of image
        signature = SignatureGetter.get_signature(self.src)

        # Search in database
        query_result = Result.objects.filter(disease_type=self.disease_type,
                                             signature=signature)

        # If this signature doesn't exist:
        if len(query_result) == 0:
            return False

        else:
            # Result as a dictionary
            result = ast.literal_eval(query_result[0].result)

            return result
