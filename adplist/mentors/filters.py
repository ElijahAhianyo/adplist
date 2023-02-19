from django_filters import rest_framework as filters
from django_filters import DateFromToRangeFilter
from adplist.mentors.models import Slot


class SlotFilter(filters.FilterSet):
    start = DateFromToRangeFilter()
    end = DateFromToRangeFilter()

    class Meta:
        model = Slot
        fields = [
            'id',
            'start',
            'end',
            'status',
            'schedule',
        ]
