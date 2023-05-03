from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .token import token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str


class RegistrationPage(View):
    def get(self, request):
        # If user logged in, it should show dashboard.
        if request.user.is_authenticated:
            return redirect("dashboard")

        form = RegistrationForm()
        return render(request, "registration.html", {"form": form})

    def post(self, request):
        # If user logged in, it should show dashboard.
        if request.user.is_authenticated:
            return redirect("dashboard")

        form = RegistrationForm(request.POST)
        # If form is valid
        if form.is_valid():
            # Cleaned data of form
            cd = form.cleaned_data

            # Search username:
            query_result = User.objects.filter(username=cd["username"])
            if len(query_result) != 0:
                messages.error(request, "این نام کاربری قبلا ثبت شده.", 'alert-danger')
                return render(request, "registration.html", {"form": form})

            # Search email:
            query_result = User.objects.filter(email=cd["email"])
            if len(query_result) != 0:
                messages.error(request, "این ایمیل، قبلا ثبت شده.", 'alert-danger')
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
            return redirect("login")

        return render(request, "registration.html", {"form": form})


class ActivateView(View):
    def get(self, request, uidb64, token):

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            if user.is_active is False:
                user.is_active = True
                user.save()

                # Send a message
                messages.success(request, "حساب کاربری با موفقیت تایید شد.", 'alert-success')

                # Back to login page
                return redirect("log_in")
            else:
                # Send a message
                messages.success(request, "حساب کاربری شما، قبلا تایید شده.", 'alert-warning')

                # Back to login page
                return redirect("log_in")

        else:
            return render(request, 'activate_account_invalid.html')


class LoginView(View):
    def get(self, request):
        # If user logged in, it should show dashboard.
        if request.user.is_authenticated:
            return redirect("dashboard")

        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        # If user logged in, it should show dashboard.
        if request.user.is_authenticated:
            return redirect("dashboard")

        form = LoginForm(request.POST)
        # If form was valid
        if form.is_valid():
            cd = form.cleaned_data
            # Search username and password
            user = authenticate(request, username=cd["username"], password=cd["password"])
            # If user found:
            if user is not None:
                # login
                login(request, user)
                # Send a message
                messages.success(request, "ورود با موفقیت انجام گردید.", 'alert-success')
                return redirect("dashboard")

            else:
                messages.error(request, "نام کاربری یا رمز عبور اشتباه است.", "alert-danger")

        return render(request, "login.html", {"form": form})


class ResetPasswordView(View):
    def get(self, request):
        # If user logged in, it should show dashboard.
        if request.user.is_authenticated:
            return redirect("dashboard")

        form = ResetPasswordForm()
        return render(request, "password_reset.html", {"form": form})

    def post(self, request):
        # If user logged in, it should show dashboard.
        if request.user.is_authenticated:
            return redirect("dashboard")

        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            # Search email:
            query_result = User.objects.filter(email=cd["email"])
            if len(query_result) != 0:
                # Send Email
                form.send_reset_password_email(self.request, query_result[0])

                # Send a message
                messages.success(request, "ایمیل ارسال گردید. لطفا از طریق ایمیل، رمز عبور خود را تغییر دهید.", 'alert-success')

            else:
                messages.error(request, "خطا: ایمیل یافت نشد.", 'alert-danger')
                return render(request, "password_reset.html", {"form": form})

            # Back to reset password page
            return redirect("reset_password")

        return render(request, "password_reset.html", {"form": form})


class ChangePasswordView(View):
    def find_user(self, uidb64):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        return user

    def check_link(self, uidb64, token):
        # Find user
        user = self.find_user(uidb64)
        if user is not None and token_generator.check_token(user, token):
            return True
        else:
            return False

    def get(self, request, uidb64, token):
        if self.check_link(uidb64, token):
            # Change password form
            form = ChangePasswordForm()
            return render(request, "change_password.html", {"form": form})

        else:
            return render(request, 'activate_account_invalid.html')

    def post(self, request, uidb64, token):
        if self.check_link(uidb64, token):
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                user = self.find_user(uidb64)
                # Change password:
                user.set_password(cd['password'])
                user.save()

                messages.success(request, "رمز عبور با موفقیت تغییر کرد.",
                                 'alert-success')

                return redirect("login")

            return render(request, "change_password.html", {"form": form})
        else:
            return render(request, 'activate_account_invalid.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("home")
