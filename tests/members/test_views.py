from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from adplist.members.models import Member
from adplist.users.models import Expertise, User
from adplist.members.serializers import MemberSerializer, MemberUpdateSerializer

import json


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
            is_member=True
        )
        self.user.expertise.add(self.expertise)
        self.client.force_authenticate(user=self.user)

        self.member = Member.objects.create(
            user=self.user
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


class GetMembersTest(BaseAPITestClass):
    url = reverse_lazy("members:member_list")

    def setUp(self):
        super(GetMembersTest, self).setUp()

    def test_get_all_members(self):
        queryset = Member.objects.all()
        serializer = MemberSerializer(queryset, many=True)
        response = self.client.get(self.url, {})
        response_data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response_data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetParticularMember(BaseAPITestClass):
    """ Test retrieving a single user profile"""

    url = reverse_lazy("members:member_detail")

    def setUp(self):
        super(GetParticularMember, self).setUp()
        self.url = reverse_lazy('members:member_detail', kwargs={"pk": self.member.pk})

    def test_get_particular_member_profile(self):
        queryset = Member.objects.get(pk=self.member.pk)
        serializer = MemberSerializer(queryset)
        response = self.client.get(self.url, {})
        response_data = json.loads(response.content.decode('utf-8'))
        print(f"response data: {response_data}")
        self.assertEqual(response_data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_profile_does_not_exit(self):
        self.url = reverse_lazy('members:member_detail', kwargs={"pk": self.member.pk + 1})
        response = self.client.get(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateMemberTest(BaseAPITestClass):
    url = reverse_lazy("members:member_list")

    def setUp(self):
        super(CreateMemberTest, self).setUp()

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
        print(f"response data: {response_data}")
        queryset = list(Member.objects.all())[-1]
        serializer = MemberSerializer(queryset)
        self.assertEqual(response_data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UpdateMemberTest(BaseAPITestClass):
    url = reverse_lazy("members:member_detail")

    def setUp(self):
        super(UpdateMemberTest, self).setUp()
        self.url = reverse_lazy('members:member_detail', kwargs={"pk": self.member.pk})

    data = {
        "user": {
            "first_name": "Lewis updated",
            "email": "lewisham@gmail.com",
            "last_name": "Hamilton updated",
            "location": "Stephenage updated",
            "title": "Mr",
            "employer": "Mercedes AMG",
            # "expertise": []
        }
    }

    def test_update_particular_member(self):
        # self.data["user"]["expertise"].append(self.expertise.pk)
        response = self.client.patch(self.url, self.data, format="json")
        response_data = json.loads(response.content.decode('utf-8'))
        print(f"response data: {response_data}")
        queryset = Member.objects.get(pk=self.member.pk)
        serializer = MemberUpdateSerializer(queryset)
        self.assertEqual(response_data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_email_should_not_be_updated(self):
        self.data["user"]["email"] = "anotheremail@gmail.com"
        response = self.client.patch(self.url, self.data, format="json")
        response_data = json.loads(response.content.decode('utf-8'))
        queryset = Member.objects.get(pk=self.member.pk)
        serializer = MemberSerializer(queryset)
        self.assertEqual(response_data['data']["user"]["email"], serializer.data["user"]["email"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteParticularMemberTest(BaseAPITestClass):

    def setUp(self):
        super(DeleteParticularMemberTest, self).setUp()
        self.url = reverse_lazy(
            "members:member_detail",
            kwargs={
                "pk": self.member.pk,
            },
        )

    def test_particular_user_phone_number_delete(self):
        response = self.client.delete(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
