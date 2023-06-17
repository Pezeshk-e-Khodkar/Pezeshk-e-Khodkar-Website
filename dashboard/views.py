from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from django.conf import settings
from django.contrib import messages

# To get configs from .env file
from decouple import config

# To use the result table of the database
from .models import *

# To use AI model and uploade image to server
from libs.controller.img_uploader import ImageUploader
from libs.controller.asd import SkinCancerDetector


class DashboardView(View):
    """Dashboard Page
    """
    def get(self, request):
        # If user logged in, it should show the dashboard.
        if request.user.is_authenticated:
            # Get user's images from database (by user id)
            data = Result.objects.filter(user=request.user.pk)
            if len(data) != 0:
                return render(request, 'dashboard.html', {"model": data})
            else:
                return render(request, 'dashboard.html')
        # If user didn't log in, it should go to the login page
        else:
            return redirect("login")


class CreateNewView(View):
    """# Create New View
    """

    # Start AI model of ASD at the beginning.
    ASD = SkinCancerDetector(str(settings.BASE_DIR / "models/" / config("SKINCANCER_AI_MODEL")))

    def get(self, request):
        # If user didn't log in, it should show the log-in form.
        if request.user.is_authenticated is False:
            return redirect("login")

        # Return create new form
        form = CreateNewForm()
        return render(request, "create_new.html", {"form": form})

    def post(self, request):
        # If user didn't log in, it should show the log-in form.
        if request.user.is_authenticated is False:
            return redirect("login")

        # Get the create new form of the POST request
        form = CreateNewForm(request.POST, request.FILES)

        # If form is valid
        if form.is_valid():
            disease_type = ""
            # Get cleaned data from the fom
            cd = form.cleaned_data

            # Get the image
            image = cd["image"]

            if cd["disease_type"] == "1":
                disease_type = "SkinCancer"

            # Verify and upload the image to the server
            uploaded_img = ImageUploader(image, str(settings.BASE_DIR / "media"),
                                         disease_type)

            # If the image doesn't upload:
            if uploaded_img.img_status is False:
                # Return an error message
                messages.error(request, "خطا: تصویر بارگذاری نشد.", 'alert-danger')

            else:
                self.ASD.detect(image, uploaded_img.img_address, uploaded_img.image_format, request.user.pk)
                # Return a success message
                messages.success(request, "تصویر با موفقیت بارگذاری و پردازش شد.", 'alert-success')

            return redirect("dashboard")
        return render(request, "create_new.html", {"form": form})


class DeleteImageView(View):
    """Delete image view
    """
    def post(self, request, image_id):
        # If user didn't log in, it should show the log-in form.
        if request.user.is_authenticated is False:
            return redirect("login")

        else:
            # Try to get int value of image_id
            try:
                id = int(image_id)
            except:
                messages.error(request, "خطا: تصویر موردنظر یافت نشد.", 'alert-danger')
                return redirect("dashboard")

            # Search image id and user in the database
            query_result = Result.objects.filter(pk=id, user=request.user.pk)
            if len(query_result) == 0:
                # Return an error message
                messages.error(request, "خطا: تصویر موردنظر یافت نشد.", 'alert-danger')
                return redirect("dashboard")
            else:
                # Remove the image from the database
                query_result[0].user.remove(request.user.pk)
                query_result[0].save()

                # Return a success message
                messages.success(request, "تصویر با موفقیت حذف شد.", 'alert-success')
                return redirect("dashboard")

    def get(self, request, image_id):
        # If method is get, return a 404 error
        return render(request, "404.html")
