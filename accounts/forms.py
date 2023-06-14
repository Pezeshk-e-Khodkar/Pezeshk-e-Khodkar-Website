# Django forms
from django import forms

# To add configs from .env file
from decouple import config

# To use Google Captcha
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3

# To use email validation
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .token import token_generator
from django.core.mail import send_mail

# To use persian validator in fields
from .validators import validate_persian


class RegistrationForm(forms.Form):
    """ Registration Form
    Fields:
        - username(CharField)
        - first_name(CharField)
        - last_name(CharField)
        - email(EmailField)
        - password(CharField)
        - confirm_password(CharField)
        - captcha(ReCaptchaField)
    """
    username = forms.CharField(label="نام کاربری",
                               max_length=30,
                               min_length=3,
                               validators=[validate_persian])

    first_name = forms.CharField(label="نام",
                                 max_length=20,
                                 min_length=3,
                                 validators=[validate_persian])

    last_name = forms.CharField(label="نام خانوادگی",
                                max_length=20,
                                min_length=3,
                                validators=[validate_persian])

    email = forms.EmailField(label="پست الکترونیک",
                             max_length=200)

    password = forms.CharField(label="رمز عبور",
                               widget=forms.PasswordInput,
                               max_length=40,
                               min_length=8,
                               validators=[validate_persian])

    confirm_password = forms.CharField(label="تکرار رمز عبور",
                                       widget=forms.PasswordInput(),
                                       max_length=40,
                                       min_length=8,
                                       validators=[validate_persian])

    captcha = ReCaptchaField(widget=ReCaptchaV3,
                             label="")

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        # Add "form-control" css class to each field
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        # Get password and confirm_password form fields
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # If confirm password was wrong
        if password != "" and password != confirm_password:
            self.add_error('confirm_password', "تکرار رمز عبور اشتباه وارد شده است.")

        return cleaned_data

    def send_activation_email(self, request, user):
        """send activation email for user
        Args:
            - request: Request object of Django
            - user: User
        """
        # Get link of this page
        current_site = get_current_site(request)
        # The subject of the email
        subject = 'فعالسازی حساب کاربری پزشک خودکار'
        # Create email message with activate_account_email_page.html and user information
        message = render_to_string(
            'activate_account_email_page.html',
            {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token_generator.make_token(user),
            }
        )
        # Send email
        send_mail(subject, message, html_message=message, from_email=config("EMAIL_HOST_USER"),
                  recipient_list=[user.email])


class LoginForm(forms.Form):
    """Login form
    Fields:
        - username(CharField)
        - password(CharField)
        - captcha(ReCaptchaField)
    """
    username = forms.CharField(label="نام کاربری",
                               max_length=30,
                               min_length=3,
                               validators=[validate_persian])

    password = forms.CharField(label="رمز عبور",
                               widget=forms.PasswordInput,
                               max_length=40,
                               min_length=8,
                               validators=[validate_persian])

    captcha = ReCaptchaField(widget=ReCaptchaV3,
                             label="")

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        # Add "form-control" css class to each field
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ResetPasswordForm(forms.Form):
    """Reset password form
    """
    email = forms.EmailField(label="پست الکترونیک", max_length=200)
    captcha = ReCaptchaField(widget=ReCaptchaV3, label="")

    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        # Add "form-control" css class to each field
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def send_reset_password_email(self, request, user):
        """Send reset password email
        Args:
            - request: Request object of Django
            - user: User
        """
        # Get link of this page
        current_site = get_current_site(request)
        # Subject of email
        subject = 'تغییر رمز عبور حساب کاربری پزشک خودکار'
        # Create email message with reset_password_email_page.html and user information
        message = render_to_string(
            'reset_password_email_page.html',
            {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token_generator.make_token(user),
            }
        )
        # Send email
        send_mail(subject, message, html_message=message, from_email=config("EMAIL_HOST_USER"),
                  recipient_list=[user.email])


class ChangePasswordForm(forms.Form):
    """Change Password Form
    Fields:
        - password(CharField)
        - confirm_password(CharField)
        - captcha(ReCaptchaField)
    """
    password = forms.CharField(label="رمز عبور جدید",
                               widget=forms.PasswordInput,
                               max_length=40,
                               min_length=8,
                               validators=[validate_persian])

    confirm_password = forms.CharField(label="تکرار رمز عبور جدید",
                                       widget=forms.PasswordInput(),
                                       max_length=40,
                                       min_length=8,
                                       validators=[validate_persian])

    captcha = ReCaptchaField(widget=ReCaptchaV3,
                             label="")

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        # Add "form-control" css class to each field
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        # Get password and confirm_password from fields
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # If confirm_password was wrong
        if password != "" and password != confirm_password:
            self.add_error('confirm_password', "تکرار رمز عبور اشتباه وارد شده است.")

        return cleaned_data
