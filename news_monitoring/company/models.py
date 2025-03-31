from urllib.parse import urlparse

from django.db import models

from news_monitoring.users import models as user_model


class Company(models.Model):
    added_by = models.ForeignKey(
        user_model.User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="added_companies",
    )
    updated_by = models.ForeignKey(
        user_model.User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="updated_companies",
    )

    name = models.CharField(max_length=255, unique=True)
    domain = models.URLField(unique=True)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """Extract only the domain from the entered URL before saving."""
        parsed_url = urlparse(self.domain)
        self.company_url = parsed_url.netloc  # Extract domain (e.g., example.com)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
