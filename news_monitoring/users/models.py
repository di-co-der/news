from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for News Monitoring.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    first_name = models.CharField(
        _("First Name"),
        max_length=150,
        default="",
    )  # Required field
    last_name = models.CharField(
        _("Last Name"),
        max_length=150,
        blank=True,
        null=True,
    )  # Optional field
    email = models.EmailField(_("Email Address"), unique=True)
    username = None  # Username replaced with email
    company = models.ForeignKey(
        "company.Company",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )  # Fixed reference

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
    ]  # Ensures first_name is required during user creation

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})
