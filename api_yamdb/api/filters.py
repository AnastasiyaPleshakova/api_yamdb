import django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__slug',)
    genre = django_filters.CharFilter(field_name='genre__slug',)
    year = django_filters.RangeFilter()

    class Meta:
        model = Title
        fields = ('name', 'category', 'genre', 'year',)
