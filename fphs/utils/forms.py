from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.forms import CharField, EmailInput, Form, Textarea
from django.utils.translation import ugettext_lazy as _

FormHelper.use_custom_control = False


class ContactForm(Form):
    email = CharField(widget=EmailInput(attrs={"placeholder": "Email"}))
    message = CharField(widget=Textarea(attrs={"placeholder": "Message"}))
    captcha = ReCaptchaField(widget=ReCaptchaV3(attrs={"required_score": 0.85}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "email",
            "message",
            "captcha",
            Submit("submit", _("Send Message"), css_class="btn-secondary"),
        )
        self.fields["captcha"].label = False
