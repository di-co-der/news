
from django.db import models

from news_monitoring.company.models import Company
from news_monitoring.users.models import User


class Source(models.Model):
    tagged_companies = models.ManyToManyField(Company, related_name="tagged_sources", blank=True)

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="sources",null=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="added_sources")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="updated_sources",)

    name = models.CharField(max_length=255)
    url = models.URLField(max_length=500)

    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("company", "url")

    def __str__(self):
        return f"Name - {self.name} and URL - {self.url}"
