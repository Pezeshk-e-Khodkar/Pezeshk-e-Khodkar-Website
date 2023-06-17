# Image uploader
# MIT License
# Copyright (c) 2023 Pezeshk-e-Khodkar

# Import pillow module to work with images
from PIL import Image

import os
import io

# Import security tools of Pezeshk-e-khodkar
from libs.sec.sec_manager import SecurityManager
from libs.sec.signature_getter import SignatureGetter

# Import result table of the database
from dashboard.models import Result


class ImageUploader(SecurityManager):
    """Upload images to server

    Usage:
        src = open("file/address.png")
        save_address = '/path/'
        img_uploader = ImgUploader(src, save_address, "SkinCancer")
        print(img_uploader.img_status)

    Args:
        - src(BytesIO): opened image
        - save_address(str): saved image address
        - disease_type(str): Type of disease
    Raise:
        - ValueError: disease_type doesn't exist.
    """

    # List of supported diseases
    diseases = ['SkinCancer']

    def __init__(self, src: io.BytesIO, save_address: str, disease_type: str):
        super(SecurityManager, self).__init__()

        self.src = src
        self.__img_address = ''
        self.__img_status = False
        self.save_address = save_address
        self.image_format = ''

        # Check is disease type correct or not.
        if disease_type in self.diseases:
            self.disease_type = disease_type
        else:
            raise ValueError(disease_type + " doesn't exist.")

        # Start process of uploading the image
        self.__upload_and_validate_image()

    def __upload_and_validate_image(self):
        """Upload image
        """

        # If file was an image and size of it was smaller than 4MB
        if self.verify(self.src) and self.verifyFileSize(self.src):
            # Search signature database to find image if it exists
            self.search_result = self.__search_signature()
            if self.search_result is not False:
                self.__img_status = None
                self.__img_address = None
                self.image_format = None
            else:
                # Upload the image to the server
                self.__upload()

                # If the image has a virus:
                if self.check_for_virus(self.__img_address):
                    # Remove the image form the server
                    self.__remove_img()
                    self.__img_status = False
                    self.__img_address = None
                    self.image_format = None
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
            - None: File didn't save
        """
        return self.__img_address

    def __upload(self):
        """Upload the image to server
        """
        # Choose a name for the image
        self.__name_image()

        # Save the image
        img = Image.open(self.src)
        img.save(self.__img_address)

    def __remove_img(self):
        """Remove the image from server
        """
        os.remove(self.__img_address)

    def __name_image(self):
        """Name the image
        """
        # Open the image
        img = Image.open(self.src)

        # Create a name and address for image (it uses signature to name images)
        if self.save_address[-1] != "/":
            self.save_address += "/"

        self.src.seek(0)

        # use signature to name
        name = SignatureGetter.get_signature(self.src)
        self.image_format = img.format.lower()

        # Create img_address
        self.__img_address = self.save_address + name + '.' + self.image_format

    def __search_signature(self):
        """Search signature of image in the database
        Returns:
            - False: If signature doesn't exist.
            - True: If signature exists.
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
            return True
