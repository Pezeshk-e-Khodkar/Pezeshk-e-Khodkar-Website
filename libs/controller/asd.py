# Automated skin cancer detector (ASD)
# MIT LICENSE

# Import tensorflow module to work with deep learning model
from tensorflow import keras, expand_dims

from libs.sec.spam_detector import ImageVerifier
from libs.sec.signature_getter import SignatureGetter
import io
from dashboard.models import Result
from django.contrib.auth.models import User


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

    def detect(self, image: io.BytesIO, img_address: str, img_format: str, user_id):
        """Detect skin cancer with deep learning model
        Arg:
            - image(BytesIO) --> Image Bytes
            - img_address(str) --> image address
            - img_format (str) --> image format
            - user_id --> user id in database

        Returns:
            - "Error: File was not an image"
            - Predictions of API (list)
        """
        search_result = self.__search_signature(image, user_id)
        if search_result is not False:
            return search_result

        elif ImageVerifier.verify(open(img_address, "rb")):
            img = keras.preprocessing.image.load_img(img_address, target_size=(180, 180))
            img_array = keras.preprocessing.image.img_to_array(img)
            img_array = expand_dims(img_array, 0)  # Create batch axis
            predictions_array = self.loaded_model.predict(img_array)

            predictions = {"basal cell carcinomas": predictions_array[0][0],
                           "melanoma": predictions_array[0][1],
                           "squamous cell carcinoma": predictions_array[0][2]}
            self.__save_result(image, predictions, img_format, user_id)

            return predictions
        else:
            return "Error: File was not an image."

    @staticmethod
    def __save_result(image, predictions, img_format, user_id):
        """Save Results in DataBase
        Args:
            - image: src of image
            - predictions: results of ai as a dictionary
            - img_format: image format
            - user_id: id of user
        """
        image.seek(0)

        # Get signature of image
        signature = SignatureGetter.get_signature(image)

        result = Result(
                        disease_type="SkinCancer",
                        signature=signature,
                        result=str(predictions),
                        image_format=img_format
                        )
        # Save results
        result.save()

        # Attach user
        query_result = User.objects.filter(pk=user_id)
        result.user.add(query_result[0])
        result.save()

    def __search_signature(self, image, user_id):
        """Search signature of image in database
        Args:
            - image: src of image
            - user_id : id of user
        Returns:
            - False: If signature doesn't exist.
            - Dictionary: result of image
        """
        image.seek(0)

        # Get signature of image
        signature = SignatureGetter.get_signature(image)

        # Search in database
        query_result_1 = Result.objects.filter(disease_type="SkinCancer",
                                               signature=signature)

        # If this signature doesn't exist:
        if len(query_result_1) == 0:
            return False

        else:
            query_result_2 = Result.objects.filter(disease_type="SkinCancer",
                                                   signature=signature, user=user_id)

            if len(query_result_2) == 0:
                query_result_3 = User.objects.filter(pk=user_id)
                if len(query_result_3) == 0:
                    raise Exception("User id not Found")

                query_result_1[0].user.add(query_result_3[0])

            return query_result_1[0].result
