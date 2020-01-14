import boto3
import django
import pytest
from django.conf import settings as base_settings
from django.test import RequestFactory
from moto import mock_s3
from rest_framework.test import APIClient

from users.tests.factories import UserFactory


def pytest_configure():
    base_settings.AWS_STORAGE_BUCKET_NAME = 'test-bucket'
    base_settings.AWS_ACCESS_KEY_ID = 'test-key'
    base_settings.AWS_SECRET_ACCESS_KEY = 'test-secret'
    base_settings.AWS_S3_CUSTOM_DOMAIN = 'test.com'
    django.setup()


@pytest.fixture(autouse=True)
def mock_boto3():
    mock = mock_s3()
    mock.start()

    conn = boto3.resource('s3',
                          aws_access_key_id=base_settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=base_settings.AWS_SECRET_ACCESS_KEY, )
    conn.create_bucket(Bucket='test-bucket')
    yield conn
    mock.stop()


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> base_settings.AUTH_USER_MODEL:
    return UserFactory(is_verified=True)


@pytest.fixture
def request_factory() -> RequestFactory:
    return RequestFactory()


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()
