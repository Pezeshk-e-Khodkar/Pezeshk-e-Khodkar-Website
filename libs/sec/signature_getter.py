# To hash images
import hashlib


class SignatureGetter:
    """Get the signatures of the files
    """
    @staticmethod
    def get_signature(src):
        """Get Signature
        Args:
            - src: file address or opened file
        Returns:
            - Sha256 signature of the file(str)
        """
        # If src is a string
        if type(src) == str:
            with open(src, 'rb') as file:
                byte = file.read()  # read entire file as bytes
                readable_hash = hashlib.sha256(byte).hexdigest()
                return readable_hash
        else:
            byte = src.read()  # read entire file as bytes
            readable_hash = hashlib.sha256(byte).hexdigest()
            return readable_hash
