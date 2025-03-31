from django.urls import path

from .views import add_company

app_name = "company"
urlpatterns = [
    path("add/", add_company, name="add_company"),
]
