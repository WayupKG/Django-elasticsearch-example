from django.urls import path
from .views import index, search_elastic, search_django


urlpatterns = [
    path('', index),
    path('search_elastic/', search_elastic, name='search_elastic'),
    path('search_django/', search_django, name='search_django'),
]
