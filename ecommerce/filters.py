import django_filters
from .models import Order


class OrderFilter(django_filters.FilterSet):
    order_date = django_filters.DateFromToRangeFilter(field_name='order_date')
       

    class Meta:
        model = Order
        fields = ['__all__']
