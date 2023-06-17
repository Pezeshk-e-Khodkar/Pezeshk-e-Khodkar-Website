from django import forms

# Google recaptcha field
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3

# Tools of Pezeshk-e-khodkar
CHOICES = (
    ("1", "سرطان پوست"),
)


class CreateNewForm(forms.Form):
    """Create New Form
    Fields:
        - image(ImageField)
        - disease_type(ChoiceField)
        - captcha(ReCaptchaField)
    """
    image = forms.ImageField(label="تصویر", )
    disease_type = forms.ChoiceField(label="نوع بیماری", choices=CHOICES)
    captcha = ReCaptchaField(widget=ReCaptchaV3, label="")

    def __init__(self, *args, **kwargs):
        super(CreateNewForm, self).__init__(*args, **kwargs)
        # Add form-control css class to the fields of the form
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
