from django.forms.widgets import (
    PasswordInput
)

class CustomPasswordInput(PasswordInput):
    template_name = "mywidgets/custom_password.html"

    # https://docs.djangoproject.com/en/5.2/topics/forms/media/#assets-as-a-static-definition
    class Media:
        js = ["mywidgets/js/custom_password.js"]