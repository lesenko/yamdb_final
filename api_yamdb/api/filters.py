from django_filters import rest_framework as db_filters
from reviews.models import Title


class TitleFilter(db_filters.FilterSet):
    category = db_filters.CharFilter(field_name='category__slug',
                                     lookup_expr='icontains')
    genre = db_filters.CharFilter(field_name='genre__slug',
                                  lookup_expr='icontains')
    name = db_filters.CharFilter(field_name='name', lookup_expr='icontains')
    year = db_filters.NumberFilter

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
