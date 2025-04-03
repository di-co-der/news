from django.urls import path

from .views import add_company, search_companies

app_name = "company"
urlpatterns = [
    path("add/", add_company, name="add_company"),
    path("search/", search_companies, name="search_companies"),
]
