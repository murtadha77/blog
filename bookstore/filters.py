
import django_filters

from.models import *


class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = '__all__'          #to all tabels and fields
        # fields = ['book', 'status']   #just 2 field in table order