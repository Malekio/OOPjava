import django_filters
from .models import GuideProfile
from locations.models import Wilaya


class GuideProfileFilter(django_filters.FilterSet):
    """
    Filter for guide profiles with various search criteria
    """

    wilaya = django_filters.ModelChoiceFilter(
        field_name="coverage_areas",
        queryset=Wilaya.objects.all(),
        help_text="Filter by coverage area (wilaya)",
    )

    min_rating = django_filters.NumberFilter(
        field_name="average_rating",
        lookup_expr="gte",
        help_text="Minimum average rating",
    )

    max_price = django_filters.NumberFilter(
        field_name="half_day_price",
        lookup_expr="lte",
        help_text="Maximum half-day price",
    )

    language = django_filters.CharFilter(
        method="filter_by_language", help_text="Filter by spoken language"
    )

    years_experience = django_filters.NumberFilter(
        field_name="years_of_experience",
        lookup_expr="gte",
        help_text="Minimum years of experience",
    )

    class Meta:
        model = GuideProfile
        fields = []

    def filter_by_language(self, queryset, name, value):
        """
        Filter guides by spoken language
        """
        return queryset.filter(languages__icontains=value)
