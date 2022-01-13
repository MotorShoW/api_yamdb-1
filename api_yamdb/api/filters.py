from django_filters import rest_framework as filters

from api.models.models import Titles


class TitleFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
    )
    year = filters.NumberFilter(field_name='year',)
    category = filters.CharFilter(field_name='category__slug',)
    genre = filters.CharFilter(field_name='genre__slug',)

    class Meta:
        model = Titles

        fields = ('name', 'year', 'category', 'genre')
