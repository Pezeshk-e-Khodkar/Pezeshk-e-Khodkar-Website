from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# Access to django project settings
from django.conf import settings

# Image Uploader
from libs.controller.img_uploader import ImageUploader

# To work with ASD AI-model
from libs.controller.asd import SkinCancerDetector
from decouple import config


class APIPage(APIView):
    """The page of API
    API Usage:
        import requests
        src = open("path/to/image", mode="rb")

        data = {
            "disease_type": "Disease type"
        }
        res = requests.post(files= {"img": src},
                            url="http://example.com/api/",
                            data=data)
    Response:
        - results as a dictionary (status-code = 200)
    Raises:
        - "details": "Request has no disease_type" (status-code = 400)
        - "details": "disease_type is wrong" (status-code = 400)
        - "details": "Request has no resource file attached called (img)" (status-code = 400)
        - "details": "Upload failed" (status-code == 400)
    """
    # Start AI model
    asd = SkinCancerDetector(str(settings.BASE_DIR / "models/" / config("SKINCANCER_AI_MODEL")))

    # Throttle
    if settings.TEST is False:
        throttle_scope = 'uploads'

    # Post Method
    def post(self, request):

        if 'disease_type' not in request.data:
            return Response({"details": "Request has no disease_type"},
                            status=status.HTTP_400_BAD_REQUEST)

        if request.data['disease_type'] not in ImageUploader.diseases:
            return Response({"details": "disease_type is wrong", "Available disease_types": ImageUploader.diseases},
                            status=status.HTTP_400_BAD_REQUEST)

        # Try to get image
        try:
            image = request.data['img'].file

        except:
            return Response({"details": "Request has no resource file attached called (img)"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Verify and upload the image to server
        uploaded_img = ImageUploader(image, str(settings.BASE_DIR / "media"),
                                     request.data["disease_type"])

        # If the image doesn't upload:
        if uploaded_img.img_status is False:
            return Response({"details": "Upload failed"},
                            status=status.HTTP_400_BAD_REQUEST)

        # If signature of image exists:
        elif uploaded_img.img_status is None:
            result = uploaded_img.search_result
            return Response({"response": result},
                            status=status.HTTP_200_OK)

        else:
            # Return output of the AI model
            if request.data['disease_type'] == "SkinCancer":
                result = self.asd.detect(image, uploaded_img.img_address)
                return Response({"response": result}, status=status.HTTP_200_OK)
