import pytest

from users.forms import UserCreationForm
from users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestUserCreationForm:
    def test_form(self):
        # A user with proto_user params does not exist yet.
        proto_user = UserFactory.build()
        form_payload = {
            'email': proto_user.email,
            'password1': proto_user._password,
            'password2': proto_user._password,
        }

        form = UserCreationForm(form_payload)

        assert form.is_valid()

        # Creating a user.
        form.save()

        # The user with proto_user params already exists, hence cannot be created.
        form = UserCreationForm(form_payload)

        assert not form.is_valid()
        assert len(form.errors) == 1
