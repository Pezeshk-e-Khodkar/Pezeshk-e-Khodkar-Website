# To hash images
import hashlib


class SignatureGetter:
    """It gets signature of files
    """
    @staticmethod
    def get_signature(src):
        """Get Signature
        Args:
            - src: file address or opened file
        Returns:
            - Sha256 signature of file
        """
        if type(src) == str:
            with open(src, 'rb') as file:
                print(file)
                byte = file.read()  # read entire file as bytes
                readable_hash = hashlib.sha256(byte).hexdigest()
                return readable_hash
        else:
            byte = src.read()  # read entire file as bytes
            readable_hash = hashlib.sha256(byte).hexdigest()
            return readable_hash
