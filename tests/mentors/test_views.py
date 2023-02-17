import datetime
import json

from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from adplist.members.models import Member
from adplist.mentors.choices import SlotStatusChoiceTypes, AppointmentStatusChoiceTypes
from adplist.mentors.models import Mentor, MentorshipAreas, Schedule, Slot, Appointment
from adplist.mentors.serializers import MentorSerializer, ScheduleSerializer, AppointmentSerializer
from adplist.users.models import Expertise, User


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

        self.schedule = Schedule.objects.create(
            mentor=self.mentor,
            all_day=False,
            opening_time= datetime.datetime(2023, 2, 2, 10, 0),
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

        # self.language = Language.objects.create(
        #     name="Test Language",
        #     code2="TL"
        # )
        # self.country = Country(
        #     name='Country',
        #     name_ascii='Country',
        #     geoname_id='123456',
        #     continent='EU')
        # self.country.save()
        #
        # self.region = Region(
        #     name='Region',
        #     name_ascii='Region',
        #     geoname_id='123457',
        #     display_name='Region',
        #     country=self.country
        # )
        # self.region.save()
        #
        # self.subregion = SubRegion(
        #     name='SubRegion',
        #     name_ascii='SubRegion',
        #     geoname_id='987654',
        #     display_name='SubRegion',
        #     region=self.region,
        #     country=self.country
        # )
        # self.subregion.save()
        #
        # self.city = City(
        #     name='First City',
        #     name_ascii='First City',
        #     geoname_id='123458',
        #     display_name='First City',
        #     search_names='firstcityregioncountry',
        #     region=self.region,
        #     country=self.country,
        #     subregion=self.subregion
        # )
        # self.city.save()
        #
        # self.account = Account.objects.create(
        #     email="user@test.com",
        #     password="secret_password",
        # )
        #
        # self.user_profile = self.account.user_profile
        # self.client.force_authenticate(user=self.account)
        #
        # self.user_phone_number = UserPhoneNumber.objects.create(
        #     user_profile=self.user_profile,
        #     number="+442083666177"
        # )
        # self.user_language = UserLanguage.objects.create(
        #     user_profile=self.user_profile,
        #     language=self.language
        # )
        # self.user_work_experience = UserWorkExperience.objects.create(
        #     title="software Engineer",
        #     contract_type="FT",
        #     employment_type="PM",
        #     organisation_name="Google",
        #     description="worked on IOT projects",
        #     start_date="2020-05-01",
        #     end_date="2021-05-06",
        #     is_current_position=False,
        #     country=self.country,
        #     city=self.city,
        #     user_profile=self.user_profile
        # )
        #
        # self.user_address = UserAddress.objects.create(
        #     city=self.city,
        #     subregion=self.subregion,
        #     region=self.region,
        #     country=self.country,
        #     building_name="Eiffel Tower",
        #     street_number=90,
        #     street_name="Westminster",
        #     town_name="Paris",
        #     postal_code="0023",
        #     user_profile=self.user_profile
        # )
        #
        # self.user_licence = UserLicence.objects.create(
        #     licence_number="320945",
        #     expiry_date="2020-05-19",
        #     verified_date="2016-03-01",
        #     user_profile=self.user_profile
        # )
        #
        # self.skill_type = SkillType.objects.create(
        #     name="Test Skill",
        #     summary="This is a test skill"
        # )
        # self.user_skill = UserSkill.objects.create(
        #     skill_type=self.skill_type,
        #     experience="XX",
        #     competence="AW",
        #     user_profile=self.user_profile
        # )
        # self.user_job_preference = UserJobPreference.objects.create(
        #     employment_type="XX",
        #     contract_type="XX",
        #     salary_is_range=True,
        #     salary_max_per_week=4000,
        #     salary_min_per_week=2000,
        #     salary_display_rate="PH",
        #     user_profile=self.user_profile
        # )
        # self.user_job_preference_location = UserJobPreferenceLocation.objects.create(
        #     postal_code="0023",
        #     latitude="2.32412341",
        #     longitude="1.12477341",
        #     search_radius="AA",
        #     user_job_preference=self.user_job_preference
        # )
        # self.user_qualification = UserQualification.objects.create(
        #     organisation_name="TestOrganisation",
        #     grade="TestGrade",
        #     start_date="2017-02-02",
        #     end_date="2020-03-02",
        #     has_ended=True,
        #     is_draft=False,
        #     city=self.city,
        #     country=self.country,
        #     user_profile=self.user_profile
        # )


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
    url = reverse_lazy("mentor_list")

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
        }
    }

    def test_create_user_phone_number_with_all_data(self):
        self.data["user"]["expertise"].append(self.expertise.pk)
        response = self.client.post(self.url, self.data, format="json")
        response_data = json.loads(response.content.decode('utf-8'))
        queryset = list(Mentor.objects.all())[-1]
        serializer = MentorSerializer(queryset)
        self.assertEqual(response_data['data'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UpdateMentorTest(BaseAPITestClass):
    url = reverse_lazy("mentor_detail")

    def setUp(self):
        super(UpdateMentorTest, self).setUp()
        self.url = reverse_lazy('mentor_detail', kwargs={"pk": self.mentor.pk})

    data = {
        "user": {
            "first_name": "Lewis updated",
            "email": "lewisham@gmail.com",
            "last_name": "Hamilton updated",
            "location": "Stephenage updated",
            "title": "Mr",
            "employer": "Mercedes AMG",
        }
    }

    def test_update_particular_mentor(self):
        response = self.client.patch(self.url, self.data, format="json")
        response_data = json.loads(response.content.decode('utf-8'))
        queryset = Mentor.objects.get(pk=self.mentor.pk)
        serializer = MentorSerializer(queryset)
        self.assertEqual(response_data['data'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_email_should_not_be_updated(self):
        self.data["user"]["email"] = "anotheremail@gmail.com"
        response = self.client.patch(self.url, self.data, format="json")
        response_data = json.loads(response.content.decode('utf-8'))
        queryset = Mentor.objects.get(pk=self.mentor.pk)
        serializer = MentorSerializer(queryset)
        self.assertEqual(response_data['data']["user"]["email"], serializer.data["user"]["email"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteParticularMentorTest(BaseAPITestClass):

    def setUp(self):
        super(DeleteParticularMentorTest, self).setUp()
        self.url = reverse_lazy(
            "mentor_detail",
            kwargs={
                "pk": self.mentor.pk,
            },
        )

    def test_particular_user_phone_number_delete(self):
        response = self.client.delete(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class GetSchedulesTest(BaseAPITestClass):
    url = reverse_lazy("schedule_list")

    def setUp(self):
        super(GetSchedulesTest, self).setUp()

    def test_get_all_schedules(self):
        queryset = Schedule.objects.all()
        serializer = ScheduleSerializer(queryset, many=True)
        response = self.client.get(self.url, {})
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data['data'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetParticularSchedule(BaseAPITestClass):
    """ Test retrieving a single user profile"""

    url = reverse_lazy("schedule_detail")

    def setUp(self):
        super(GetParticularSchedule, self).setUp()
        self.url = reverse_lazy('schedule_detail', kwargs={"pk": self.schedule.pk})

    def test_get_particular_schedule(self):
        queryset = Schedule.objects.get(pk=self.schedule.pk)
        serializer = ScheduleSerializer(queryset)
        response = self.client.get(self.url, {})
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data['data'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_profile_does_not_exit(self):
        self.url = reverse_lazy('schedule_detail', kwargs={"pk": self.schedule.pk + 1})
        response = self.client.get(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateScheduleTest(BaseAPITestClass):
    url = reverse_lazy("schedule_list")

    def setUp(self):
        super(CreateScheduleTest, self).setUp()

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
        }
    }

    def test_create_user_phone_number_with_all_data(self):
        self.data["user"]["expertise"].append(self.expertise.pk)
        response = self.client.post(self.url, self.data, format="json")
        response_data = json.loads(response.content.decode('utf-8'))
        queryset = list(Schedule.objects.all())[-1]
        serializer = ScheduleSerializer(queryset)
        self.assertEqual(response_data['data'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UpdateScheduleTest(BaseAPITestClass):
    url = reverse_lazy("schedule_detail")

    def setUp(self):
        super(UpdateScheduleTest, self).setUp()
        self.url = reverse_lazy('schedule_detail', kwargs={"pk": self.schedule.pk})

    data = {
        "user": {
            "first_name": "Lewis updated",
            "email": "lewisham@gmail.com",
            "last_name": "Hamilton updated",
            "location": "Stephenage updated",
            "title": "Mr",
            "employer": "Mercedes AMG",
        }
    }

    def test_update_particular_schedule(self):
        response = self.client.patch(self.url, self.data, format="json")
        response_data = json.loads(response.content.decode('utf-8'))
        queryset = Schedule.objects.get(pk=self.schedule.pk)
        serializer = ScheduleSerializer(queryset)
        self.assertEqual(response_data['data'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_email_should_not_be_updated(self):
        self.data["user"]["email"] = "anotheremail@gmail.com"
        response = self.client.patch(self.url, self.data, format="json")
        response_data = json.loads(response.content.decode('utf-8'))
        queryset = Schedule.objects.get(pk=self.schedule.pk)
        serializer = ScheduleSerializer(queryset)
        self.assertEqual(response_data['data']["user"]["email"], serializer.data["user"]["email"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteParticularScheduleTest(BaseAPITestClass):

    def setUp(self):
        super(DeleteParticularScheduleTest, self).setUp()
        self.url = reverse_lazy(
            "schedule_detail",
            kwargs={
                "pk": self.schedule.pk,
            },
        )

    def test_particular_user_phone_number_delete(self):
        response = self.client.delete(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class GetAppointmentsTest(BaseAPITestClass):
    url = reverse_lazy("appointment_list")

    def setUp(self):
        super(GetAppointmentsTest, self).setUp()

    def test_get_all_appointments(self):
        queryset = Appointment.objects.all()
        serializer = AppointmentSerializer(queryset, many=True)
        response = self.client.get(self.url, {})
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data['data'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetParticularAppointment(BaseAPITestClass):
    """ Test retrieving a single user profile"""

    url = reverse_lazy("appointment_detail")

    def setUp(self):
        super(GetParticularAppointment, self).setUp()
        self.url = reverse_lazy('appointment_detail', kwargs={"pk": self.appointment.pk})

    def test_get_particular_appointment(self):
        queryset = Appointment.objects.get(pk=self.appointment.pk)
        serializer = AppointmentSerializer(queryset)
        response = self.client.get(self.url, {})
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data['data'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_profile_does_not_exit(self):
        self.url = reverse_lazy('appointment_detail', kwargs={"pk": self.appointment.pk + 1})
        response = self.client.get(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateAppointmentTest(BaseAPITestClass):
    url = reverse_lazy("appointment_list")

    def setUp(self):
        super(CreateAppointmentTest, self).setUp()

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
        }
    }

    def test_create_user_phone_number_with_all_data(self):
        self.data["user"]["expertise"].append(self.expertise.pk)
        response = self.client.post(self.url, self.data, format="json")
        response_data = json.loads(response.content.decode('utf-8'))
        queryset = list(Appointment.objects.all())[-1]
        serializer = AppointmentSerializer(queryset)
        self.assertEqual(response_data['data'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UpdateAppointmentTest(BaseAPITestClass):
    url = reverse_lazy("appointment_detail")

    def setUp(self):
        super(UpdateAppointmentTest, self).setUp()
        self.url = reverse_lazy('appointment_detail', kwargs={"pk": self.appointment.pk})

    data = {
        "user": {
            "first_name": "Lewis updated",
            "email": "lewisham@gmail.com",
            "last_name": "Hamilton updated",
            "location": "Stephenage updated",
            "title": "Mr",
            "employer": "Mercedes AMG",
        }
    }

    def test_update_particular_appointment(self):
        response = self.client.patch(self.url, self.data, format="json")
        response_data = json.loads(response.content.decode('utf-8'))
        queryset = Appointment.objects.get(pk=self.appointment.pk)
        serializer = AppointmentSerializer(queryset)
        self.assertEqual(response_data['data'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_email_should_not_be_updated(self):
        self.data["user"]["email"] = "anotheremail@gmail.com"
        response = self.client.patch(self.url, self.data, format="json")
        response_data = json.loads(response.content.decode('utf-8'))
        queryset = Appointment.objects.get(pk=self.appointment.pk)
        serializer = AppointmentSerializer(queryset)
        self.assertEqual(response_data['data']["user"]["email"], serializer.data["user"]["email"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteParticularAppointmentTest(BaseAPITestClass):

    def setUp(self):
        super(DeleteParticularAppointmentTest, self).setUp()
        self.url = reverse_lazy(
            "appointment_detail",
            kwargs={
                "pk": self.appointment.pk,
            },
        )

    def test_particular_user_phone_number_delete(self):
        response = self.client.delete(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
