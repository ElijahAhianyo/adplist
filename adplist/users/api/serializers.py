from django.contrib.auth import get_user_model
from rest_framework import serializers
from adplist.users.models import Expertise

User = get_user_model()


class ExpertiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expertise
        exclude = ["created_at", "updated_at"]

        extra_kwargs = {
            "id": {"read_only": True},
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", "location", "title", "employer", "expertise"]

        extra_kwargs = {
            "password": {"write_only": True},
            "id": {"read_only": True},
        }


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "location", "title", "employer", "expertise"]

        extra_kwargs = {
            "password": {"write_only": True},
            "id": {"read_only": True},
            "expertise": {"required": False}
        }
