from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy


def validate_persian(value):
    """Persian Validator
    Info:
        Default validator of Django doesn't allow to write persian letters.
        We should use this.
    """

    # Black_list
    black_list = [" ", "`", "~", "!", "@", "#", "$", "%", "^", "&", "*",
                  "(", ")", "[", "]", "{", "}", "\\", "|", ":", ";", "\"",
                  "\'", ">", "<", ".", "?", "؟", "+", "=", ",", "-", "/"
                  "،", "؛", "«", "»", "÷"]

    for i in black_list:
        if i in value:
            raise ValidationError(
                gettext_lazy("فقط از حروف و اعداد و _ استفاده کنید.")
            )
