from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# Access to django project settings
from django.conf import settings

# Image Uploader
from libs.controller.img_uploader import ImageUploader

# To work with ASD AI-model
from libs.controller.asd import SkinCancerDetector


# API Page of ASD
class AutomatedSkinCancerDetectorPage(APIView):
    # Start AI model
    asd = SkinCancerDetector(str(settings.BASE_DIR / "models/ASD.h5"))

    # Post Method
    def post(self, request):

        try:
            image = request.data['img'].file

        except:
            return Response({"details": "Request has no resource file attached"}, status=status.HTTP_400_BAD_REQUEST)

        # Verify and upload the image to server
        uploaded_img = ImageUploader(image, str(settings.BASE_DIR / "userfiles"))

        # If the image doesn't upload:
        if uploaded_img.img_status is False:
            return Response({"details": "File upload failed"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            # Return output of the AI model
            return Response({"response": self.asd.detect(uploaded_img.img_address)}, status=status.HTTP_200_OK)

