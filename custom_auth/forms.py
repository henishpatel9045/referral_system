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

    def save(self, commit=True):
        user = CustomUser.objects.create_user(**self.cleaned_data)
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "password",
            "active",
            "admin",
            "referred_by",
        )
