from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import CustomUser


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "password",
            "referred_by",
        )

    def clean_referred_by(self, referred_by):
        if not CustomUser.objects.filter(referral_code=referred_by).exists():
            raise forms.ValidationError("Invalid referral code")

    def save(self, commit=True):
        user = CustomUser.objects.create_user(**self.cleaned_data)
        return user

    def save_m2m(self):
        pass


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=("Password"),
        help_text=(
            "Raw passwords are not stored, so there is no way to see this "
            "user’s password, but you can change the password using "
            '<a href="{}">this form</a>.'
        ),
    )

    class Meta:
        model = CustomUser
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get("password")
        if password:
            password.help_text = password.help_text.format(
                f"../../{self.instance.pk}/password/"
            )

    def clean_referred_by(self):
        referred_by = self.cleaned_data.get("referred_by")
        if not CustomUser.objects.filter(referral_code=referred_by).exists():
            raise forms.ValidationError("Invalid referral code")
        return referred_by
