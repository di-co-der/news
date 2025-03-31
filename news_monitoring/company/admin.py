from django.contrib import admin

from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "domain",
        "added_by",
        "added_on",
        "updated_by",
        "updated_on",
    )
    search_fields = ("name", "domain", "added_by__email")
    list_filter = ("added_on", "updated_on")
    ordering = ("-added_on",)
