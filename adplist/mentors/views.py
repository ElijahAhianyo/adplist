from django.http import Http404

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from adplist.mentors.serializers import MentorSerializer, ScheduleSerializer, AppointmentSerializer, \
    MentorUpdateSerializer, SlotSerializer
from adplist.mentors.models import Mentor, Schedule, Appointment, Slot
from rest_framework.permissions import AllowAny


#
# class MentorListView(APIView):
#     def get(self, request):
#         queryset = Mentor.object.all()
#         serializer = MentorSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = MentorSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

class MentorList(generics.ListCreateAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    permission_classes = [AllowAny]


class MentorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        return MentorUpdateSerializer if self.request.method in ["PUT", "PATCH"] else MentorSerializer


class MentorApproveView(APIView):
    permission_classes = [AllowAny]
    serializer_class = MentorSerializer

    def get_object(self, pk):
        try:
            return Mentor.objects.get(pk=pk)
        except Mentor.DoesNotExist:
            raise Http404

    def patch(self, request, pk=None):
        queryset = self.get_object(pk)
        queryset.is_approved = True
        queryset.save()
        serializer = self.serializer_class(queryset)
        return Response(serializer.data)


class AppointmentList(generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [AllowAny]


class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [AllowAny]

    # def get_serializer_class(self):
    #     return MentorUpdateSerializer if self.request.action in ["PUT", "PATCH"] else MentorSerializer


class ScheduleList(generics.ListCreateAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [AllowAny]


class ScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [AllowAny]

    # def get_serializer_class(self):
    #     return MentorUpdateSerializer if self.request.action in ["PUT", "PATCH"] else MentorSerializer


class SlotList(generics.ListAPIView):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer
    permission_classes = [AllowAny]


class SlotDetailView(generics.RetrieveAPIView):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer
    permission_classes = [AllowAny]
