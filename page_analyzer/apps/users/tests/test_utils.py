import re

import pytest

from users.utils import generate_random_username

pytestmark = pytest.mark.django_db


def test_generate_random_username(user):
    # User instance has first and last name
    username = generate_random_username(first_name=user.first_name, last_name=user.last_name, email=user.email)
    assert username.startswith(f'{user.first_name}{user.last_name}'.lower())

    # User instance has only last name
    username = generate_random_username(last_name=user.last_name, email=user.email)
    assert username.startswith(f'{user.last_name}'.lower())

    # User instance has only email
    username = generate_random_username(email=user.email)
    assert username.startswith(re.sub(r'\W+', '', user.email.split('@')[0]))

    # User instance has no first name, last name or email
    username = generate_random_username()
    assert len(username) == 38  # random_value_length + salt_length
