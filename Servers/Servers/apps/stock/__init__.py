from django.urls import path
from .views import *


urlpatterns = [
    path('gettest/', get_test_data),
    path('getmin/', get_Min_data),
]