from django import forms
from django.core import validators
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3

# Email Validation
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .token import token_generator


# Registration Form
class RegistrationForm(forms.Form):
    username = forms.CharField(label="نام کاربری", max_length=30, min_length=3, validators=[validators.validate_slug],)
    first_name = forms.CharField(label="نام", max_length=20, min_length=3, validators=[validators.validate_slug])
    last_name = forms.CharField(label="نام خانوادگی", max_length=20, min_length=3, validators=[validators.validate_slug])
    email = forms.EmailField(label="پست الکترونیک", max_length=200)

    password = forms.CharField(label="رمز عبور", widget=forms.PasswordInput, max_length=40, min_length=8, validators=[validators.validate_slug])
    confirm_password = forms.CharField(label="تکرار رمز عبور", widget=forms.PasswordInput(), max_length=40, validators=[validators.validate_slug])
    captcha = ReCaptchaField(widget=ReCaptchaV3, label="")

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != "" and password != confirm_password:
            self.add_error('confirm_password', "تکرار رمز عبور اشتباه وارد شده است.")

        return cleaned_data

    def send_activation_email(self, request, user):
        current_site = get_current_site(request)
        subject = 'Activate Your Account'
        message = render_to_string(
            'activate_account_email_page.html',
            {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token_generator.make_token(user),
            }
        )

        user.email_user(subject, message, html_message=message)