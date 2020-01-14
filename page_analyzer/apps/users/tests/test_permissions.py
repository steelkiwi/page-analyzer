import pytest
from users.permissions import IsVerified
from users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestIsVerifiedPermission:

    def test_has_permission(self, rf, user):
        request = rf.get("/")
        request.user = user

        assert IsVerified().has_permission(request, None)

        unverified_user = UserFactory()
        request.user = unverified_user

        assert not IsVerified().has_permission(request, None)
