from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.contrib.auth import forms, get_user_model
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(forms.UserCreationForm):

    error_message = forms.UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken.")}
    )

    class Meta(forms.UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])


class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = [
            "name",
            "bio",
            "location",
            "occupation",
            "website",
            "facebook",
            "instagram",
            "twitter",
            "pintrest",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "name",
            "bio",
            "location",
            "occupation",
            "website",
            "facebook",
            "instagram",
            "twitter",
            "pintrest",
            Submit("submit", _("Save")),
        )


class UserPrivacyForm(ModelForm):
    class Meta:
        model = User
        fields = ["public_reviews"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout("public_reviews", Submit("submit", _("Save")))
