from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from adplist.members.serializers import MemberSerializer, MemberUpdateSerializer
from adplist.members.models import Member

from rest_framework.permissions import AllowAny


class MemberList(generics.ListCreateAPIView):
    search_fields = ['user__first_name']
    filterset_fields = ["user__first_name", ]
    filter_backends = (filters.SearchFilter,DjangoFilterBackend)
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [AllowAny]


class MemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        return MemberUpdateSerializer if self.request.method in ["PUT", "PATCH"] else MemberSerializer
