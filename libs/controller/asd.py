# Automated skin cancer detector (ASD) API
# MIT LICENSE

# Import tensorflow module to load deep learning model
from tensorflow import keras, expand_dims

from libs.sec.spam_detector import ImageVerifier
import logging


class SkinCancerDetector(ImageVerifier):
    """Automated Skin Cancer Detector
    Args:
        - model_address: Address of AI model
    """
    def __init__(self, model_address: str):
        super(ImageVerifier, self).__init__()
        try:
            self.loaded_model = keras.models.load_model(model_address)
        except Exception as e:
            raise e

    def detect(self, src: str):
        """Detect skin cancer with deep learning model

        Usage:
            src = "./address/file.png"
            print(SkinCancerDetector().detector(src))

        Arg:
            - src(str) --> image address

        Returns:
            - "Error: File was not an image"
            - Predictions of API (list)
        """
        if self.verify(open(src,mode="rb")):
            img = keras.preprocessing.image.load_img(src, target_size=(180, 180))
            img_array = keras.preprocessing.image.img_to_array(img)
            img_array = expand_dims(img_array, 0)  # Create batch axis
            predictions_array = self.loaded_model.predict(img_array)
            logging.debug(predictions_array)
            predictions = {"basal cell carcinomas": predictions_array[0][0],
                           "melanoma": predictions_array[0][1],
                           "squamous cell carcinoma": predictions_array[0][2]}

            return predictions
        else:
            return "Error: File was not an image"
