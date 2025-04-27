from django.db import models
from news_monitoring.company.models import Company
from news_monitoring.source.models import Source
from news_monitoring.users.models import User


class Story(models.Model):
    tagged_companies = models.ManyToManyField(Company, related_name="tagged_stories")

    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name="stories", null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="stories")
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="added_stories")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="updated_stories")

    published_date = models.DateField()
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=255)
    body_text = models.TextField()
    article_url = models.URLField(max_length=500)

    class Meta:
        unique_together = ("company", "article_url")  # Ensuring uniqueness per company

    def __str__(self):
        return self.title
