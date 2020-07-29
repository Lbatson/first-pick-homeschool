from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout, Submit
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
        title = _("Profile")
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML(f"<h1>{title}</h1>"),
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
        labels = {"public_reviews": _("Display reviews on public profile")}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        title = _("Privacy")
        public_reviews_text = _(
            """Enabling this setting allows reviews to be displayed as part of your profile. Removing
            reviews from your profile will not remove them from displaying on the curriculums themselves"""
        )
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML(f"<h1>{title}</h1>"),
            "public_reviews",
            HTML(f'<div class="mb-4 text-muted">{public_reviews_text}</div>'),
            Submit("submit", _("Save")),
        )
