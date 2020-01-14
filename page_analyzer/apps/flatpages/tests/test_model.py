import pytest

from flatpages.models import ContactUsRequest, FlatPage, SupportCenterElement
from flatpages.tests.factories import ContactsUsFactory, FlatPageFactory, SupportCenterElementFactory

pytestmark = pytest.mark.django_db


class TestContactUsRequest:
    @staticmethod
    def test__str__(mocker):
        mocker.patch('flatpages.tasks.send_admin_request_notification.apply_async')
        contact_us_request = ContactsUsFactory()
        assert str(contact_us_request) == f'Request {contact_us_request.id} by {contact_us_request.email}'

    @staticmethod
    def test_default_status(mocker):
        mocker.patch('flatpages.tasks.send_admin_request_notification.apply_async')
        contact_us_request = ContactsUsFactory()
        assert contact_us_request.status == ContactUsRequest.STATUS.open


class TestFlatPage:
    @staticmethod
    def test_manager_only_public():
        FlatPageFactory(status=FlatPage.STATUS.hidden)
        FlatPageFactory(status=FlatPage.STATUS.published)
        assert FlatPage.objects.active().count() == 1

    def test__str__(self):
        flatpage = FlatPageFactory(status=FlatPage.STATUS.published)
        assert str(flatpage) == flatpage.slug

    def test_get_absolute_url(self):
        flatpage = FlatPageFactory(status=FlatPage.STATUS.published)
        assert flatpage.get_absolute_url() == f'/api/v1/flatpages/{flatpage.slug}/'


class TestSupportCenterElement:
    @staticmethod
    def test_manager_only_public():
        SupportCenterElementFactory(status=SupportCenterElement.STATUS.published)
        SupportCenterElementFactory(status=SupportCenterElement.STATUS.hidden)
        assert SupportCenterElement.objects.active().count() == 1
