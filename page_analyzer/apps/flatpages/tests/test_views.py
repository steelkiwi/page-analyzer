from django.urls import reverse

import pytest
from rest_framework import status

from flatpages.models import SupportCenterElement, SupportCenterCategory
from flatpages.tests.factories import FlatPageFactory, SupportCenterElementFactory, SupportCenterCategoryFactory

pytestmark = pytest.mark.django_db


class TestContactUsView:
    def setup(self):
        self.contact_us_url = reverse('api:flatpages:contact-us')

    def test_contact_us_post(self, api_client, mocker):
        mocker.patch('flatpages.tasks.send_admin_request_notification.apply_async')
        payload = {"email": "JohnDoe@example.com",
                   "title": "Minor request",
                   "category": "Web",
                   "description": "lorem ipsum"}

        response = api_client.post(self.contact_us_url, payload, 'json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['email'] == payload['email']

    def test_contact_us_post_invalid_email(self, api_client):
        payload = {"email": "JohnDoe.com",
                   "title": "Minor request",
                   "category": "Web",
                   "description": "lorem ipsum"}

        response = api_client.post(self.contact_us_url, payload, 'json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['email'][0] == "Enter a valid email address."

    def test_contact_us_not_allowed_method(self, api_client):
        response = api_client.get(self.contact_us_url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


class TestFlatPageViewSet:
    def setup(self):
        self.flatpages_url = reverse('api:flatpages:page-list')

    def test_flatpage_get_active_list(self, api_client):
        FlatPageFactory.create_batch(size=3)
        response = api_client.get(self.flatpages_url)
        assert response.status_code == status.HTTP_200_OK
        assert 3 == len(response.data['results'])

    def test_flatpage_get_detailed(self, api_client):
        flatpage = FlatPageFactory()
        response = api_client.get(flatpage.get_absolute_url())
        assert response.status_code == status.HTTP_200_OK
        assert flatpage.title == response.data['title']

    def test_flatpage_post_method(self, api_client):
        response = api_client.post(self.flatpages_url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


class TestSupportCenterViewSet:
    def setup(self):
        self.support_center_url = reverse('api:flatpages:support-center-list')

    def test_list(self, api_client):
        SupportCenterCategoryFactory.create_batch(size=2, status=SupportCenterCategory.STATUS.published,)
        SupportCenterCategoryFactory(status=SupportCenterCategory.STATUS.hidden)

        response = api_client.get(self.support_center_url)
        assert response.status_code == status.HTTP_200_OK
        assert 2 == len(response.data['results'])

    def test_elements(self, api_client):
        support_center_category = SupportCenterCategoryFactory()
        SupportCenterElementFactory(category=support_center_category)
        element_hidden = SupportCenterElementFactory(
            category=support_center_category, status=SupportCenterElement.STATUS.hidden
        )

        elements_url = reverse('api:flatpages:support-center-elements', kwargs={'slug': support_center_category.slug})
        response = api_client.get(elements_url)
        assert 1 == len(response.data['results'])
        assert element_hidden.question != len(response.data['results'][0]['question'])
