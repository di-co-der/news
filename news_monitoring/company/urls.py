from django.urls import path

from news_monitoring.company import views

app_name = "company"
urlpatterns = [
    path("add/", views.add_company, name="add_company"),
    path("search/", views.search_companies, name="search_companies"),
]
