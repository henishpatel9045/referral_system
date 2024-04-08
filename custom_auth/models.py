import random, string
import uuid
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models
from django.core.exceptions import ValidationError


class CustomUserManager(BaseUserManager):
    def generate_referral_code(self):
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
        while self.filter(referral_code=code).exists():
            code = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
        return code

    def create_user(self, email, password=None, referred_by=None, **extra_fields):
        if not email:
            raise ValidationError("The Email field must be set")
        if (
            referred_by
            and not self.model.objects.filter(referral_code=referred_by).exists()
        ):
            raise ValidationError("Invalid referred_by code.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.referral_code = self.generate_referral_code()
        user.referred_by = referred_by
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("staff", True)
        extra_fields.setdefault("admin", True)

        if extra_fields.get("staff") is not True:
            raise ValueError("Superuser must have staff=True.")
        if extra_fields.get("admin") is not True:
            raise ValueError("Superuser must have admin=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    email = models.EmailField(unique=True, db_index=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    referral_code = models.CharField(max_length=50, blank=True)
    referred_by = models.CharField(max_length=50, blank=True, null=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    class Meta(AbstractBaseUser.Meta):
        verbose_name = "User"
