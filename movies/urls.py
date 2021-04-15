from django.urls import path
from .views import Trending

urlpatterns = [
    path('trending/', Trending.as_view({'get': 'top'})),
]