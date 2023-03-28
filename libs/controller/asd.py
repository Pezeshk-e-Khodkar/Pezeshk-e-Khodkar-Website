# Automated skin cancer detector (ASD) API
# MIT LICENSE

# Import tensorflow module to work with deep learning model
from tensorflow import keras, expand_dims

from libs.sec.spam_detector import ImageVerifier
from api.models import Result
from libs.sec.signature_getter import SignatureGetter
import io


class SkinCancerDetector:
    """Automated Skin Cancer Detector
    Args:
        - model_address: Address of AI model
    """
    def __init__(self, model_address: str):
        try:
            self.loaded_model = keras.models.load_model(model_address)
        except Exception as e:
            raise e

    def detect(self, image: io.BytesIO, img_address: str):
        """Detect skin cancer with deep learning model

        Usage:
            src = "./address/file.png"
            print(SkinCancerDetector().detector(src))

        Arg:
            - image(BytesIO) --> Image Bytes
            - img_address(str) --> image address

        Returns:
            - "Error: File was not an image"
            - Predictions of API (list)
        """
        if ImageVerifier.verify(open(img_address, "rb")):
            img = keras.preprocessing.image.load_img(img_address, target_size=(180, 180))
            img_array = keras.preprocessing.image.img_to_array(img)
            img_array = expand_dims(img_array, 0)  # Create batch axis
            predictions_array = self.loaded_model.predict(img_array)

            predictions = {"basal cell carcinomas": predictions_array[0][0],
                           "melanoma": predictions_array[0][1],
                           "squamous cell carcinoma": predictions_array[0][2]}

            self.__save_result(image, predictions)
            return predictions
        else:
            return "Error: File was not an image"

    @staticmethod
    def __save_result(image, predictions):
        """Save Results in DataBase
        """
        image.seek(0)
        # Get signature of image
        signature = SignatureGetter.get_signature(image)

        result = Result(
                        disease_type="SkinCancer",
                        signature=signature,
                        result=str(predictions)
                        )
        # Save results
        result.save()
