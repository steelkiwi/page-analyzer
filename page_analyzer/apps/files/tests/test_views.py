import pytest
from django.urls import reverse
from files.models import Avatar
from files.tests.factories import AvatarFactory
from rest_framework import status

pytestmark = pytest.mark.django_db


class TestAvatarAPIViewSet:
    avatar_upload_url = reverse("api:files:avatars-list")
    avatar_detail_reverse = "api:files:avatars-detail"

    def test_only_authorized_allowed(self, client):
        response = client.get(self.avatar_upload_url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_happy_path(self, mocker, api_client, user):
        # need to mock `url` property of thumbnail to work properly with moto
        mocker.patch("imagekit.cachefiles.ImageCacheFile.url", return_value="/media/thumb.png",
                     new_callable=mocker.PropertyMock)
        assert Avatar.objects.count() == 0

        api_client.force_authenticate(user)
        avatar = AvatarFactory.build()

        response = api_client.post(self.avatar_upload_url, data={"file": avatar.file}, format="multipart")

        assert response.status_code == status.HTTP_201_CREATED
        assert Avatar.objects.filter(creator=user).count() == 1

    def test_cant_upload_with_wrong_extension(self, mocker, temp_file, api_client, user):
        mocker.patch("imagekit.cachefiles.ImageCacheFile.url", return_value="/media/thumb.png",
                     new_callable=mocker.PropertyMock)
        api_client.force_authenticate(user)
        avatar = AvatarFactory.build(file=temp_file)

        response = api_client.post(self.avatar_upload_url, data={"file": avatar.file}, format="multipart")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Avatar.objects.count() == 0

    def test_retrieve(self, mocker, api_client, user):
        mocked_file = mocker.patch("imagekit.cachefiles.ImageCacheFile.url", return_value="/media/thumb.png",
                                   new_callable=mocker.PropertyMock)
        avatar = AvatarFactory(creator=user)
        response = api_client.get(reverse(self.avatar_detail_reverse, args=(avatar.id,)))

        assert response.status_code == status.HTTP_200_OK
        assert response.data["file"].endswith(avatar.file.url)
        assert response.data["thumbnail"].endswith(mocked_file.return_value)
