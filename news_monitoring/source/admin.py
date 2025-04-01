from django.contrib import admin

from .models import Source


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "display_tagged_companies", "added_by")
    search_fields = ("name", "url")
    list_filter = ("added_on",)
    ordering = ("-updated_on",)

    def display_tagged_companies(self, obj):
        return ", ".join([company.name for company in obj.tagged_companies.all()])

    display_tagged_companies.short_description = "Tagged Companies"
