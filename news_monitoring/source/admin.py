from django.contrib import admin

from .models import Source


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "added_by")
    search_fields = ("name", "url")
    list_filter = ("added_on",)
    ordering = ("-updated_on",)
