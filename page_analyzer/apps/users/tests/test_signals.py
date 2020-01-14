import pytest

from users.models import Profile, User
from users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestCreateProfileReceiver:

    def test_creates_profile(self):
        proto_user = UserFactory.build()
        user = User.objects.create_user(
            email=proto_user.email, password=proto_user._password, first_name=proto_user.first_name,
            last_name=proto_user.last_name, username=proto_user.username
        )

        assert Profile.objects.filter(user=user).count() == 1

        user.first_name = user.first_name[:-1]
        user.save()
        # assert doesn't create additional model
        assert Profile.objects.filter(user=user).count() == 1
