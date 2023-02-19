from django_filters import rest_framework as filters
from adplist.members.models import Member
import django_filters


class MemberFilter(filters.FilterSet):
    expertise = django_filters.CharFilter(field_name='user__expertise__name',
                                          lookup_expr='icontains')

    class Meta:
        model = Member
        fields = [
            "id",
            "user",
            "expertise"
        ]
