from django_filters import FilterSet, NumberFilter, OrderingFilter
from .models import LoanRequest


class LoanRequestFilter(FilterSet):
    term__gte = NumberFilter(field_name='term', lookup_expr='gte')
    term__lte = NumberFilter(field_name='term', lookup_expr='lte')
    interest_rate__gte = NumberFilter(field_name='interest_rate', lookup_expr='gte')
    interest_rate__lte = NumberFilter(field_name='interest_rate', lookup_expr='lte')
    amount__gte = NumberFilter(field_name='amount', lookup_expr='gte')
    amount__lte = NumberFilter(field_name='amount', lookup_expr='lte')

    o = OrderingFilter(
        fields=(
            ('amount', 'amount'),
            ('created_at', 'created_at'),
        ),
        field_labels={
            'amount': 'Amount',
            'created_at': 'Date Created',
        },
    )

    class Meta:
        model = LoanRequest
        fields = []
