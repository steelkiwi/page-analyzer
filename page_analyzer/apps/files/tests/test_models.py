import pytest
from django.core.files.storage import default_storage
from django.urls import reverse

from files.models import Avatar
from files.models import get_file_upload_path
from files.tests.factories import AvatarFactory

pytestmark = pytest.mark.django_db


def test_correct_naming_for_generic_get_file_upload_path():
    avatar = AvatarFactory.build()

    result = get_file_upload_path(avatar, "filename")

    assert result.startswith(avatar.upload_prefix)


class TestAvatar:

    def test_str(self):
        file = AvatarFactory()

        assert str(file) == f"Avatar of user {file.creator.id}"

    def test_absolute_url(self):
        file = AvatarFactory()

        assert file.get_absolute_url() == reverse("api:files:avatars-detail", args=(file.id,))

    def test_delete(self):
        avatar = AvatarFactory()

        file_name = avatar.file.name
        assert default_storage.exists(file_name)

        avatar.delete()
        assert not default_storage.exists(file_name)
        assert not Avatar.objects.exists()


class TestAvatarQuerySet:

    def test_delete(self):
        avatars = AvatarFactory.create_batch(3)
        name1, name2, name3 = avatars[0].file.name, avatars[1].file.name, avatars[2].file.name

        Avatar.objects.delete()

        assert not default_storage.exists(name1)
        assert not default_storage.exists(name2)
        assert not default_storage.exists(name3)
        assert not Avatar.objects.exists()
