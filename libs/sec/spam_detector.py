# Spam Detector

# Import pillow module to work with images
from PIL import Image
import os
import io


class FileSizeVerifier:
    """ImageSizeVerifier
    """

    @staticmethod
    def verifyFileSize(src: io.BytesIO):
        """Verify size of image ( The maximum file size should be 4 MB )
        Usage:
            file = open(/path/, "rb")
            VerifyImageSize.verifyFileSize(file)

        Args:
            - src: src of file (opened in rb mode)
        Returns:
            - True: verified
            - False: Didn't verified (file should open with "rb" mode)
        """
        src.seek(0, os.SEEK_END)
        if src.tell() <= 4000000:
            return True
        else:
            return False


class ImageVerifier:
    """Image verifier
    """

    @staticmethod
    def verify(src: io.BytesIO):
        """Is it an image or no?
        Usage:
            src = open("/path/", "rb")
            VerifyImage.verify(src)

        Args:
            - src: opened file
        Returns:
            - True: It 's an image
            - False: It isn't an image
        """
        try:
            src.seek(0)
            img = Image.open(src)
            img.verify()
            return True

        except Exception as e:
            return False
