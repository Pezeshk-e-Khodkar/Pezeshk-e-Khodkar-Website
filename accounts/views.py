from django.shortcuts import render, redirect
from django.views import View
from .forms import RegistrationForm
from django.contrib.auth.models import User
from django.contrib import messages

from .token import token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str


class RegistrationPage(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, "registration.html", {"form": form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        # If form is valid
        if form.is_valid():
            # Cleaned data of form
            cd = form.cleaned_data

            # Search username:
            query_result = User.objects.filter(username=cd["username"])
            if len(query_result) != 0:
                messages.success(request, "این نام کاربری قبلا ثبت شده.", 'alert-danger')
                return render(request, "registration.html", {"form": form})

            # Search email:
            query_result = User.objects.filter(email=cd["email"])
            if len(query_result) != 0:
                messages.success(request, "این ایمیل، قبلا ثبت شده.", 'alert-danger')
                return render(request, "registration.html", {"form": form})

            # Create user
            user = User.objects.create_user(cd["username"], cd["email"], cd["password"])
            user.first_name = cd["first_name"]
            user.last_name = cd["last_name"]
            user.is_active = False
            user.save()

            # Send Email
            form.send_activation_email(self.request, user)

            # Send a message
            messages.success(request, "ثبت نام با موفقیت انجام شد. لطفا از طریق ایمیل ارسال شده، حساب کاربری را تایید نمایید.", 'alert-success')

            # Back to signup page
            return redirect("sign_up")

        return render(request, "registration.html", {"form": form})


class ActivateView(View):
    def get(self, request, uidb64, token):

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            # Send a message
            messages.success(request, "حساب کاربری با موفقیت تایید شد.", 'alert-success')

            # Back to login page
            return redirect("log_in")

        else:
            return render(request, 'activate_account_invalid.html')
