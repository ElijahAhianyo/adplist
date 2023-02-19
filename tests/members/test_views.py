from django.urls import reverse_lazy
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from adplist.members.models import Member
from adplist.users.models import Expertise, User
from adplist.members.serializers import MemberSerializer, MemberUpdateSerializer

import json


class BaseAPITestClass(APITestCase):
    def setUp(self):
        settings.TEST = True
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

    url = reverse_lazy("members:member_detail")

    def setUp(self):
        super(GetParticularMember, self).setUp()
        self.url = reverse_lazy('members:member_detail', kwargs={"pk": self.member.pk})

    def test_get_particular_member(self):
        queryset = Member.objects.get(pk=self.member.pk)
        serializer = MemberSerializer(queryset)
        response = self.client.get(self.url, {})
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_member_does_not_exit(self):
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

    def test_create_member_with_all_data(self):
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
        }
    }

    def test_update_particular_member(self):
        response = self.client.patch(self.url, self.data, format="json")
        response_data = json.loads(response.content.decode('utf-8'))
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

    def test_particular_member_delete(self):
        response = self.client.delete(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
