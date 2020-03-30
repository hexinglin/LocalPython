from django.urls import path
from .views import get_home_pic


urlpatterns = [
    path('getpic/', get_home_pic),
]