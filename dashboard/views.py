from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from libs.controller.img_uploader import ImageUploader
from libs.controller.asd import SkinCancerDetector
from django.conf import settings
from django.contrib import messages
from decouple import config
from .models import Result


# Dashboard view:
class DashboardView(View):
    def get(self, request):
        # If user logged in, it should show dashboard.
        if request.user.is_authenticated:
            data = Result.objects.filter(user=request.user.pk)
            if len(data) != 0:
                return render(request, 'dashboard.html', {"model": data})
            else:
                return render(request, 'dashboard.html')
        else:
            return redirect("login")


# Create New View
class CreateNewView(View):

    # Start AI model
    asd = SkinCancerDetector(str(settings.BASE_DIR / "models/" / config("SKINCANCER_AI_MODEL")))

    def get(self, request):
        # If user didn't log in, it should show log-in form.
        if request.user.is_authenticated is False:
            return redirect("login")

        form = CreateNewForm()
        return render(request, "create_new.html", {"form": form})

    def post(self, request):
        # If user didn't log in, it should show log-in form.
        if request.user.is_authenticated is False:
            return redirect("login")

        form = CreateNewForm(request.POST, request.FILES)
        if form.is_valid():
            disease_type = ""
            cd = form.cleaned_data
            image = cd["image"]
            if cd["disease_type"] == "1":
                disease_type = "SkinCancer"

            # Verify and upload the image to server
            uploaded_img = ImageUploader(image, str(settings.BASE_DIR / "media"),
                                         disease_type)

            # If the image doesn't upload:
            if uploaded_img.img_status is False:
                messages.error(request, "خطا: تصویر بارگذاری نشد.", 'alert-danger')

            else:
                self.asd.detect(image, uploaded_img.img_address, uploaded_img.image_format, request.user.pk)
                messages.success(request, "تصویر با موفقیت بارگذاری و پردازش شد.", 'alert-success')

            return redirect("dashboard")
        return render(request, "create_new.html", {"form": form})