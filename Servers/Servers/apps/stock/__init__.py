from django.urls import path
from .views import get_test_data


urlpatterns = [
    path('gettest/', get_test_data),
]