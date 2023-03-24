import hashlib


class SignatureGetter:

    @staticmethod
    def get_signature(src):
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
