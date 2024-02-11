import django_filters
from .models import LoanRequest


class LoanRequestFilter(django_filters.FilterSet):
    term__gte = django_filters.NumberFilter(field_name='term', lookup_expr='gte')
    term__lte = django_filters.NumberFilter(field_name='term', lookup_expr='lte')
    interest_rate__gte = django_filters.NumberFilter(field_name='interest_rate', lookup_expr='gte')
    interest_rate__lte = django_filters.NumberFilter(field_name='interest_rate', lookup_expr='lte')
    amount__gte = django_filters.NumberFilter(field_name='amount', lookup_expr='gte')
    amount__lte = django_filters.NumberFilter(field_name='amount', lookup_expr='lte')

    class Meta:
        model = LoanRequest
        fields = ['term__gte', 'term__lte', 'interest_rate__gte', 'interest_rate__lte', 'amount__gte', 'amount__lte']
