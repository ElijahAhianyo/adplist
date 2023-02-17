from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from adplist.users.api.serializers import UserSerializer, UserUpdateSerializer

from adplist.members.models import Member


class MemberSerializer(WritableNestedModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Member
        fields = ["user"]

        extra_kwargs = {
            "id": {"read_only": True},
        }


class MemberUpdateSerializer(WritableNestedModelSerializer):
    user = UserUpdateSerializer(required=True)

    class Meta:
        model = Member
        exclude = ["created_at", "updated_at"]

        extra_kwargs = {
            "id": {"read_only": True},
        }
