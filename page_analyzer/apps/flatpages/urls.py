from django.urls import path

from rest_framework import routers

from flatpages.views import FlatPageViewSet, SupportCenterViewSet, ContactUsView

router = routers.SimpleRouter()
router.register(r'flatpages', FlatPageViewSet, basename='page', )
router.register(r'support-center', SupportCenterViewSet, basename='support-center',)

urlpatterns = [
    path('contact-us/', ContactUsView.as_view(), name='contact-us'),
] + router.urls
