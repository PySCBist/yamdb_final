from django_filters import rest_framework as filters
from .models import Title


class GenreFilter(filters.FilterSet):
    genre = filters.CharFilter(
        field_name='genre__slug', lookup_expr='iexact'
    )
    category = filters.CharFilter(
        field_name='category__slug', lookup_expr='iexact'
    )
    year = filters.CharFilter(
        field_name='year', lookup_expr='iexact'
    )
    name = filters.CharFilter(
        field_name='name', lookup_expr='icontains'
    )

    class Meta:
        model = Title

        fields = ['genre', 'category', 'year', 'name']
