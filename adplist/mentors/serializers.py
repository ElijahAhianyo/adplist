from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework import status

from drf_writable_nested.serializers import WritableNestedModelSerializer

from adplist.mentors.models import Mentor, MentorshipAreas, Schedule, Slot, Appointment  # , NotAvailable
from adplist.users.api.serializers import UserSerializer, UserUpdateSerializer
from adplist.mentors.choices import SlotStatusChoiceTypes


class MentorshipAreasSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorshipAreas
        exclude = ["created_at", "updated_at"]

        extra_kwargs = {
            "id": {"read_only": True},
        }


class MentorSerializer(WritableNestedModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Mentor
        fields = '__all__'

        extra_kwargs = {
            "id": {"read_only": True},
            "is_approved": {"read_only": True}
        }

    def create(self, validated_data):
        validated_data["user"]["is_mentor"] = True
        return super().create(validated_data)


class MentorUpdateSerializer(WritableNestedModelSerializer):
    user = UserUpdateSerializer(required=False)

    class Meta:
        model = Mentor
        exclude = ["created_at", "updated_at"]

        extra_kwargs = {
            "id": {"read_only": True},
        }


class ScheduleSerializer(WritableNestedModelSerializer):
    # days_of_week = DaysOfWeekSerializer(required=False)
    # not_available = NotAvailableSerializer(required=False)

    class Meta:
        model = Schedule
        fields = ["mentor", "all_day", "opening_time", "closing_time",
                  ]

        extra_kwargs = {
            "id": {"read_only": True},
        }


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ["id", "schedule", "status", "start", "end", "comments"]

        extra_kwargs = {
            "id": {"read_only": True},
        }


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        exclude = ["created_at", "updated_at"]

        extra_kwargs = {
            "id": {"read_only": True},
            "minutes_duration": {"read_only": True},
        }

    def create(self, validated_data):
        slot = validated_data.get("slot")
        mentor = validated_data.get("mentor")
        if slot and slot.status == SlotStatusChoiceTypes.BUSY:
            raise ValidationError(detail="cant create appointment for already booked slot",
                                  code=status.HTTP_400_BAD_REQUEST)
        if mentor and not mentor.is_approved:
            raise ValidationError(detail="mentor is not approved",
                                  code=status.HTTP_400_BAD_REQUEST)

        return super().create(validated_data)
