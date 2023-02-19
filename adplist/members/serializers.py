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

    def create(self, validated_data):
        validated_data["user"]["is_member"] = True
        return super().create(validated_data)


class MemberUpdateSerializer(WritableNestedModelSerializer):
    user = UserUpdateSerializer(required=True)

    class Meta:
        model = Member
        exclude = ["created_at", "updated_at"]

        extra_kwargs = {
            "id": {"read_only": True},
        }
