import datetime
import json

from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from adplist.members.models import Member
from adplist.mentors.choices import SlotStatusChoiceTypes, AppointmentStatusChoiceTypes
from adplist.mentors.models import Mentor, MentorshipAreas, Schedule, Slot, Appointment
from adplist.mentors.serializers import MentorSerializer, MentorUpdateSerializer, ScheduleSerializer, \
    AppointmentSerializer
from adplist.users.models import Expertise, User

from django.conf import settings

print(f"DB: {settings.DATABASES}")


class BaseAPITestClass(APITestCase):
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)
        self.expertise = Expertise.objects.create(
            name="UI/UX",
            description="UI/UX"
        )

        self.user = User.objects.create(
            first_name="Test",
            last_name="User",
            email="exampleuser@gmail.com",
            password="1234567890",
            # expertise=self.expertise,
            title="Mr.",
            location="Random Location",
            is_mentor=True
        )
        self.user.expertise.add(self.expertise)

        self.client.force_authenticate(user=self.user)

        self.user2 = User.objects.create(
            first_name="Test",
            last_name="User",
            email="exampleuser2@gmail.com",
            password="1234567890",
            title="Mr.",
            location="Random Location",
            is_member=True
        )
        self.user2.expertise.add(self.expertise)
        # self.client.force_authenticate(user=self.user)

        self.member = Member.objects.create(
            user=self.user2
        )

        self.mentorship_areas = MentorshipAreas.objects.create(
            name="interviews"
        )

        self.mentor = Mentor.objects.create(
            user=self.user,
            is_approved=False,
        )
        self.mentor.mentorship_areas.add(self.mentorship_areas)
        q = Mentor.objects.all()
        print(f"Q is {q}")
        self.schedule = Schedule.objects.create(
            mentor=self.mentor,
            all_day=False,
            opening_time=datetime.datetime(2023, 2, 2, 10, 0),
            closing_time=datetime.datetime(2023, 2, 2, 15, 0),
        )

        self.slot = Slot.objects.create(
            schedule=self.schedule,
            status=SlotStatusChoiceTypes.FREE,
            start=datetime.datetime(2023, 2, 2, 10, 0),
            end=datetime.datetime(2023, 2, 2, 10, 30),
            comments="random comment"
        )

        self.busy_slot = Slot.objects.create(
            schedule=self.schedule,
            status=SlotStatusChoiceTypes.BUSY,
            start=datetime.datetime(2023, 2, 2, 10, 0),
            end=datetime.datetime(2023, 2, 2, 10, 30),
            comments="random comment"
        )

        self.appointment = Appointment.objects.create(
            mentor=self.mentor,
            member=self.member,
            status=AppointmentStatusChoiceTypes.PENDING,
            slot=self.slot,
            start=datetime.datetime(2023, 2, 2, 10, 0),
            end=datetime.datetime(2023, 2, 2, 10, 30),
            minutes_duration=30

        )


class GetMentorsTest(BaseAPITestClass):
    url = reverse_lazy("mentors:mentor_list")

    def setUp(self):
        super(GetMentorsTest, self).setUp()

    def test_get_all_mentors(self):
        queryset = Mentor.objects.all()
        serializer = MentorSerializer(queryset, many=True)
        response = self.client.get(self.url, {})
        response_data = json.loads(response.content.decode('utf-8'))
        print(f"response data: {response_data}")
        self.assertEqual(response_data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetParticularMentor(BaseAPITestClass):
    """ Test retrieving a single user profile"""

    url = reverse_lazy("mentors:mentor_detail")

    def setUp(self):
        super(GetParticularMentor, self).setUp()
        self.url = reverse_lazy('mentors:mentor_detail', kwargs={"pk": self.mentor.pk})

    def test_get_particular_mentor_profile(self):
        queryset = Mentor.objects.get(pk=self.mentor.pk)
        serializer = MentorSerializer(queryset)
        response = self.client.get(self.url, {})
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_profile_does_not_exit(self):
        self.url = reverse_lazy('mentors:mentor_detail', kwargs={"pk": self.mentor.pk + 1})
        response = self.client.get(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateMentorTest(BaseAPITestClass):
    url = reverse_lazy("mentors:mentor_list")

    def setUp(self):
        super(CreateMentorTest, self).setUp()

    data = {
        "user": {
            "first_name": "Lewis",
            "last_name": "Hamilton",
            "email": "lewisham@gmail.com",
            "location": "Stephenage",
            "title": "Mr",
            "password": "123456789",
            "employer": "Mercedes",
            "expertise": []
        },
        "mentorship_areas": []
    }

    def test_create_user_phone_number_with_all_data(self):
        self.data["user"]["expertise"].append(self.expertise.pk)
        self.data["mentorship_areas"].append(self.mentorship_areas.pk)
        response = self.client.post(self.url, self.data, format="json")
        response_data = json.loads(response.content.decode('utf-8'))
        queryset = list(Mentor.objects.all())[-1]
        serializer = MentorSerializer(queryset)
        self.assertEqual(response_data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UpdateMentorTest(BaseAPITestClass):
    url = reverse_lazy("mentors:mentor_detail")

    def setUp(self):
        super(UpdateMentorTest, self).setUp()
        self.url = reverse_lazy('mentors:mentor_detail', kwargs={"pk": self.mentor.pk})

    data = {
        "user": {
            "first_name": "Lewis",
            "last_name": "Hamilton",
            "email": "lewisham@gmail.com",
            "location": "Stephenage",
            "title": "Mr",
            "password": "123456789",
            "employer": "Mercedes",
            "expertise": []
        },
        "mentorship_areas": []
    }

    def test_update_particular_mentor(self):
        self.data["user"]["expertise"].append(self.expertise.pk)
        self.data["mentorship_areas"].append(self.mentorship_areas.pk)
        response = self.client.patch(self.url, self.data, format="json")
        response_data = json.loads(response.content.decode('utf-8'))
        queryset = Mentor.objects.get(pk=self.mentor.pk)
        serializer = MentorUpdateSerializer(queryset)
        self.assertEqual(response_data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_email_should_not_be_updated(self):
        self.data["user"]["email"] = "anotheremail@gmail.com"
        response = self.client.patch(self.url, self.data, format="json")
        response_data = json.loads(response.content.decode('utf-8'))
        queryset = Mentor.objects.get(pk=self.mentor.pk)
        serializer = MentorSerializer(queryset)
        self.assertEqual(response_data['data']["user"]["email"], serializer.data["user"]["email"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ApproveMentorTest(BaseAPITestClass):
    url = reverse_lazy("mentors:mentor_approve")

    def setUp(self):
        super(ApproveMentorTest, self).setUp()
        self.url = reverse_lazy('mentors:mentor_approve', kwargs={"pk": self.mentor.pk})
        self.data = {}

    def test_update_particular_mentor(self):
        response = self.client.patch(self.url, self.data, format="json")
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertTrue(response_data["is_approved"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteParticularMentorTest(BaseAPITestClass):

    def setUp(self):
        super(DeleteParticularMentorTest, self).setUp()
        self.url = reverse_lazy(
            "mentors:mentor_detail",
            kwargs={
                "pk": self.mentor.pk,
            },
        )

    def test_particular_user_phone_number_delete(self):
        response = self.client.delete(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class GetSchedulesTest(BaseAPITestClass):
    url = reverse_lazy("mentors:schedule_list")

    def setUp(self):
        super(GetSchedulesTest, self).setUp()

    def test_get_all_schedules(self):
        queryset = Schedule.objects.all()
        serializer = ScheduleSerializer(queryset, many=True)
        response = self.client.get(self.url, {})
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetParticularSchedule(BaseAPITestClass):
    """ Test retrieving a single user profile"""

    url = reverse_lazy("mentors:schedule_detail")

    def setUp(self):
        super(GetParticularSchedule, self).setUp()
        self.url = reverse_lazy('mentors:schedule_detail', kwargs={"pk": self.schedule.pk})

    def test_get_particular_schedule(self):
        queryset = Schedule.objects.get(pk=self.schedule.pk)
        serializer = ScheduleSerializer(queryset)
        response = self.client.get(self.url, {})
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_profile_does_not_exit(self):
        self.url = reverse_lazy('mentors:schedule_detail', kwargs={"pk": self.schedule.pk + 1})
        response = self.client.get(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateScheduleTest(BaseAPITestClass):
    url = reverse_lazy("mentors:schedule_list")

    def setUp(self):
        super(CreateScheduleTest, self).setUp()

    data = {
        "all_day": False,
        "opening_time": "2023-02-17T01:30:40.862Z",
        "closing_time": "2023-02-17T05:30:40.862Z",
    }

    def test_create_user_phone_number_with_all_data(self):
        self.data["mentor"] = self.mentor.pk
        response = self.client.post(self.url, self.data, format="json")
        response_data = json.loads(response.content.decode('utf-8'))
        queryset = list(Schedule.objects.all())[-1]
        serializer = ScheduleSerializer(queryset)
        self.assertEqual(response_data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UpdateScheduleTest(BaseAPITestClass):
    url = reverse_lazy("mentors:schedule_detail")

    def setUp(self):
        super(UpdateScheduleTest, self).setUp()
        self.url = reverse_lazy('mentors:schedule_detail', kwargs={"pk": self.schedule.pk})

    data = {
        "all_day": True,
        "opening_time": None,
        "closing_time": None,
    }

    def test_update_particular_schedule(self):
        response = self.client.patch(self.url, self.data, format="json")
        response_data = json.loads(response.content.decode('utf-8'))
        queryset = Schedule.objects.get(pk=self.schedule.pk)
        serializer = ScheduleSerializer(queryset)
        self.assertEqual(response_data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteParticularScheduleTest(BaseAPITestClass):

    def setUp(self):
        super(DeleteParticularScheduleTest, self).setUp()
        self.url = reverse_lazy(
            "mentors:schedule_detail",
            kwargs={
                "pk": self.schedule.pk,
            },
        )

    def test_particular_schedule_delete(self):
        response = self.client.delete(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class GetAppointmentsTest(BaseAPITestClass):
    url = reverse_lazy("mentors:appointment_list")

    def setUp(self):
        super(GetAppointmentsTest, self).setUp()

    def test_get_all_appointments(self):
        queryset = Appointment.objects.all()
        serializer = AppointmentSerializer(queryset, many=True)
        response = self.client.get(self.url, {})
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetParticularAppointment(BaseAPITestClass):
    """ Test retrieving a single user profile"""

    url = reverse_lazy("mentors:appointment_detail")

    def setUp(self):
        super(GetParticularAppointment, self).setUp()
        self.url = reverse_lazy('mentors:appointment_detail', kwargs={"pk": self.appointment.pk})

    def test_get_particular_appointment(self):
        queryset = Appointment.objects.get(pk=self.appointment.pk)
        serializer = AppointmentSerializer(queryset)
        response = self.client.get(self.url, {})
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_profile_does_not_exit(self):
        self.url = reverse_lazy('mentors:appointment_detail', kwargs={"pk": self.appointment.pk + 1})
        response = self.client.get(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateAppointmentTest(BaseAPITestClass):
    url = reverse_lazy("mentors:appointment_list")

    def setUp(self):
        super(CreateAppointmentTest, self).setUp()

    data = {
        "status": "PENDING",
        "start": "2023-02-17T12:17:14.370Z",
        "end": "2023-02-17T12:17:14.370Z",
        # "minutes_duration": 30,
        # "mentor": 2,
        # "member": 2,
        # "slot": 1
    }

    def test_create_user_phone_number_with_all_data(self):
        self.data["mentor"] = self.mentor.pk
        self.data["member"] = self.member.pk
        self.data["slot"] = self.slot.pk

        response = self.client.post(self.url, self.data, format="json")
        response_data = json.loads(response.content.decode('utf-8'))
        queryset = list(Appointment.objects.all())[-1]
        serializer = AppointmentSerializer(queryset)
        self.assertEqual(response_data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UpdateAppointmentTest(BaseAPITestClass):
    url = reverse_lazy("mentors:appointment_detail")

    def setUp(self):
        super(UpdateAppointmentTest, self).setUp()
        self.url = reverse_lazy('mentors:appointment_detail', kwargs={"pk": self.appointment.pk})

    data = {
        "status": "BOOKED",
        "start": "2023-02-17T12:17:14.370Z",
        "end": "2023-02-17T12:17:14.370Z",
    }

    def test_update_particular_appointment(self):
        response = self.client.patch(self.url, self.data, format="json")
        response_data = json.loads(response.content.decode('utf-8'))
        queryset = Appointment.objects.get(pk=self.appointment.pk)
        serializer = AppointmentSerializer(queryset)
        self.assertEqual(response_data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteParticularAppointmentTest(BaseAPITestClass):

    def setUp(self):
        super(DeleteParticularAppointmentTest, self).setUp()
        self.url = reverse_lazy(
            "mentors:appointment_detail",
            kwargs={
                "pk": self.appointment.pk,
            },
        )

    def test_particular_user_phone_number_delete(self):
        response = self.client.delete(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
