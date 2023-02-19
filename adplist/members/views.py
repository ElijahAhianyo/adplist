from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from adplist.members.serializers import MemberSerializer, MemberUpdateSerializer
from adplist.members.models import Member
from adplist.members.filters import MemberFilter

from rest_framework.permissions import AllowAny, IsAuthenticated


class MemberList(generics.ListCreateAPIView):
    search_fields = ['user__expertise__name']
    filterset_class = MemberFilter
    filter_backends = (filters.SearchFilter,DjangoFilterBackend)
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [AllowAny]


class MemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return MemberUpdateSerializer if self.request.method in ["PUT", "PATCH"] else MemberSerializer
