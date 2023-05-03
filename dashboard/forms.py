from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from accounts.validators import validate_persian

CHOICES = (
    ("1", "سرطان پوست"),
)


class CreateNewForm(forms.Form):
    image = forms.ImageField(label="تصویر", )
    disease_type = forms.ChoiceField(label="نوع بیماری", choices=CHOICES)
    captcha = ReCaptchaField(widget=ReCaptchaV3, label="")

    def __init__(self, *args, **kwargs):
        super(CreateNewForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
