# company/api_urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import CompanyViewSet

app_name = "company_api"

router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='company')

urlpatterns = [
    path('', include(router.urls)),
]
