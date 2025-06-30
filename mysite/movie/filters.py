from .models import Movie
from django_filters.rest_framework import FilterSet

class MovieFilter(FilterSet):
    class Meta:
        model = Movie
        fields = {
            'country':['exact'],
            'genre': ['exact'],
            'actor': ['exact'],
            'director': ['exact'],
            'status_movie': ['exact'],
            'year': ['gt', 'lt'],
        }