from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django import forms


class ContactForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    message = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Message"}))
    captcha = ReCaptchaField(widget=ReCaptchaV3(attrs={"required_score": 0.85}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "email", "message", "captcha", Submit("submit", "Send Message")
        )
        self.fields["captcha"].label = False
