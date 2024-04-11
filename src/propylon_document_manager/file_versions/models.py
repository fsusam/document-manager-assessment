from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import logging


logger = logging.getLogger(__name__)

class User(AbstractUser):
    """
    Default custom user model for Propylon Document Manager.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})


def get_upload_to(instance, filename):
    logger.info(f'{instance.url}/{filename}')
    # if url is home, then add the file directly to user_pk
    if instance.url == '/':
        return f"user_pk/{filename}"
    else:
        return f"user_pk/{instance.url}/{filename}"

class FileVersion(models.Model):
    file_name = models.fields.CharField(max_length=512, null=True)
    url = models.fields.CharField(max_length=2048, null=False,default="/")
    version_number = models.fields.IntegerField(null=True,default=0)
    file = models.FileField(upload_to=get_upload_to, blank=False, null=False)
