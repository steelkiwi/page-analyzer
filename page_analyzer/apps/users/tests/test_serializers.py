import pytest

from users.serializers import ProfileSerializer
from users.tests.factories import UserFactory, ProfileFactory

pytestmark = pytest.mark.django_db


class TestProfileSerializer:
    def test_to_representation(self):
        profile = ProfileFactory()

        data = ProfileSerializer(profile).data

        assert data["username"] == profile.user.username
        assert data["last_name"] == profile.user.last_name
        assert data["first_name"] == profile.user.first_name
        assert data["description"] == profile.description

    def test_partial_update(self):
        user = UserFactory()
        profile = ProfileFactory(user=user)

        new_profile_data = ProfileFactory.build()
        new_user_data = UserFactory.build()

        data = {
            "description": new_profile_data.description,
            "last_name": new_user_data.last_name,
        }

        serializer = ProfileSerializer(instance=profile, data=data, partial=True)
        assert serializer.is_valid(), serializer.errors
        serializer.save()

        user.refresh_from_db()
        assert user.last_name == data["last_name"]

        profile.refresh_from_db()
        assert profile.description == data["description"]

    def test_update(self):
        user = UserFactory()
        profile = ProfileFactory(user=user)

        new_profile_data = ProfileFactory.build()
        new_user_data = UserFactory.build()

        data = {
            "birth_date": new_profile_data.birth_date,
            "description": new_profile_data.description,
            "first_name": new_user_data.first_name,
            "last_name": new_user_data.last_name,
            "username": new_user_data.username,
        }

        serializer = ProfileSerializer(instance=profile, data=data)
        assert serializer.is_valid(), serializer.errors
        profile = serializer.save()

        assert profile.description == data["description"]
        assert profile.birth_date == data["birth_date"]
        assert profile.user.last_name == data["last_name"]
        assert profile.user.first_name == data["first_name"]
        assert profile.user.username == data["username"]

    def test_username_uniqueness_validation(self):
        user = UserFactory()
        profile = ProfileFactory(user=user)

        new_user_data = UserFactory()

        data = {"username": new_user_data.username}

        serializer = ProfileSerializer(instance=profile, data=data, partial=True)
        assert not serializer.is_valid()
        assert "username" in serializer.errors
