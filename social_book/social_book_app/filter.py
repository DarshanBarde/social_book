import django_filters
from .models import CustomUser

class AuthnSellFilter(django_filters.FilterSet):
    public_visiblity = django_filters.BooleanFilter(field_name='public_visiblity', label='public_visiblity')

    class Meta:
        model = CustomUser
        fields = ['public_visiblity']