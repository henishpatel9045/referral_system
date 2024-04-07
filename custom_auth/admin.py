from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.contrib import admin

from .forms import UserAdminCreationForm, UserAdminChangeForm

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = (
        "email",
        "name",
        "staff",
    )
    list_filter = ()
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    (
                        "first_name",
                        "last_name",
                    ),
                    "referral_code",
                    "referred_by",
                )
            },
        ),
        ("Permissions", {"fields": ("admin", "staff", "active")}),
    )
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("email","password", "referred_by",)}),)
    readonly_fields = ("referral_code",)
    

    search_fields = (
        "email",
        "first_name",
        "last_name",
    )
    ordering = (
        "email",
        "first_name",
        "last_name",
    )

    def name(self, obj):
        return obj.get_full_name()
