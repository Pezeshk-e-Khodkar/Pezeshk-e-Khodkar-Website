from django.shortcuts import render, redirect
from django.views import View
from .forms import *

# To use tools related to users
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# To use email validation
from .token import token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str


class RegistrationView(View):
    """Registration Page
    """
    def get(self, request):
        # If user logged in, it should show the dashboard.
        if request.user.is_authenticated:
            return redirect("dashboard")

        # Return the register form
        form = RegistrationForm()
        return render(request, "registration.html", {"form": form})

    def post(self, request):
        # If user logged in, it should show the dashboard.
        if request.user.is_authenticated:
            return redirect("dashboard")

        # Get the register form from the post method
        form = RegistrationForm(request.POST)

        # If form is valid
        if form.is_valid():
            # Get cleaned data of form
            cd = form.cleaned_data

            # Search username (Username have not to be duplicated):
            query_result = User.objects.filter(username=cd["username"])
            if len(query_result) != 0:
                # Return an error
                messages.error(request, "این نام کاربری قبلا ثبت شده.", 'alert-danger')
                return render(request, "registration.html", {"form": form})

            # Search email (Email have not to be duplicated):
            query_result = User.objects.filter(email=cd["email"])
            if len(query_result) != 0:
                # Return an error
                messages.error(request, "این ایمیل، قبلا ثبت شده.", 'alert-danger')
                return render(request, "registration.html", {"form": form})

            # Create the user with info of form
            user = User.objects.create_user(cd["username"], cd["email"], cd["password"])
            user.first_name = cd["first_name"]
            user.last_name = cd["last_name"]
            user.is_active = False
            # Save the user
            user.save()

            # Send an activation email
            form.send_activation_email(self.request, user)

            # Send a success message
            messages.success(request,
                             "ثبت نام با موفقیت انجام شد. لطفا از طریق ایمیل ارسال شده، حساب کاربری را تایید نمایید.",
                             'alert-success')

            # Back to the signup page
            return redirect("login")

        return render(request, "registration.html", {"form": form})


class ActivateView(View):
    """Activation Page
    """
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        # If the activation link was correct
        if user is not None and token_generator.check_token(user, token):
            # If user id wasn't active:
            if user.is_active is False:
                user.is_active = True
                user.save()

                # Send a success message
                messages.success(request, "حساب کاربری با موفقیت تایید شد.", 'alert-success')

                # Back to the login page
                return redirect("log_in")
            # If it was active:
            else:
                # Send a success message
                messages.success(request, "حساب کاربری شما، قبلا تایید شده.", 'alert-warning')

                # Back to the login page
                return redirect("log_in")

        else:
            return render(request, 'activate_account_invalid.html')


class LoginView(View):
    """Login Page
    """
    def get(self, request):
        # If user logged in, it should show the dashboard.
        if request.user.is_authenticated:
            return redirect("dashboard")

        # Return Login form
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        # If user logged in, it should show the dashboard.
        if request.user.is_authenticated:
            return redirect("dashboard")

        # Get form for the POST request
        form = LoginForm(request.POST)

        # If form was valid
        if form.is_valid():
            # Get cleaned data from the form
            cd = form.cleaned_data

            # Search username and password in database
            user = authenticate(request, username=cd["username"], password=cd["password"])

            # If user found:
            if user is not None:
                # login the user
                login(request, user)

                # Send a success message
                messages.success(request, "ورود با موفقیت انجام گردید.", 'alert-success')
                return redirect("dashboard")

            else:
                # Send an error message
                messages.error(request, "نام کاربری یا رمز عبور اشتباه است.", "alert-danger")

        return render(request, "login.html", {"form": form})


class ResetPasswordView(View):
    """Reset Password page
    """
    def get(self, request):
        # If user logged in, it should show the dashboard.
        if request.user.is_authenticated:
            return redirect("dashboard")

        # Return the reset password form
        form = ResetPasswordForm()
        return render(request, "password_reset.html", {"form": form})

    def post(self, request):
        # If user logged in, it should show the dashboard.
        if request.user.is_authenticated:
            return redirect("dashboard")

        # Get the reset password form from the POST request
        form = ResetPasswordForm(request.POST)

        # If form is valid
        if form.is_valid():
            # Get the cleaned data from the form
            cd = form.cleaned_data

            # Search email (Email should be in the database):
            query_result = User.objects.filter(email=cd["email"])
            if len(query_result) != 0:
                # Send an email
                form.send_reset_password_email(self.request, query_result[0])

                # Send a success message
                messages.success(request,
                                 "ایمیل ارسال گردید. لطفا از طریق ایمیل، رمز عبور خود را تغییر دهید.",
                                 'alert-success')

            else:
                # Send an error message
                messages.error(request, "خطا: ایمیل یافت نشد.", 'alert-danger')
                return render(request, "password_reset.html", {"form": form})

            # Back to reset password page
            return redirect("reset_password")

        return render(request, "password_reset.html", {"form": form})


class ChangePasswordView(View):
    """Change Password Page
    """
    def find_user(self, uidb64):
        """Find user from id
        Args:
            - uidb64
        Return:
            - user: User object of Django
            - None: If user doesn't exist
        """
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        return user

    def check_link(self, uidb64, token):
        """It checks is the page link correct and related to a user or not.
        Args:
            - uidb64
            - token
        Returns:
            - True: Link is correct
            - False: Link isn't correct
        """
        # Find the user
        user = self.find_user(uidb64)
        if user is not None and token_generator.check_token(user, token):
            return True
        else:
            return False

    def get(self, request, uidb64, token):
        # If link was correct
        if self.check_link(uidb64, token):
            # Return change password form
            form = ChangePasswordForm()
            return render(request, "change_password.html", {"form": form})

        else:
            # Return an error page
            return render(request, 'activate_account_invalid.html')

    def post(self, request, uidb64, token):
        # If link was correct
        if self.check_link(uidb64, token):
            # Get the change password form from the POST request
            form = ChangePasswordForm(request.POST)

            # If form is valid
            if form.is_valid():
                # Get the cleaned data from the form
                cd = form.cleaned_data

                # Find the user from id
                user = self.find_user(uidb64)

                # Change password and save the user:
                user.set_password(cd['password'])
                user.save()

                # Send a success message and go to login form
                messages.success(request, "رمز عبور با موفقیت تغییر کرد.",
                                 'alert-success')

                return redirect("login")

            return render(request, "change_password.html", {"form": form})
        else:
            return render(request, 'activate_account_invalid.html')


class LogoutView(View):
    """Logout Page
    """
    def get(self, request):
        # Logout and go to home page
        logout(request)
        return redirect("home")
