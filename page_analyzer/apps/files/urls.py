from rest_framework import routers
from django.urls import path, include
from files.views import AvatarAPIViewSet

router = routers.SimpleRouter()
router.register("avatars", AvatarAPIViewSet, "avatars")

urlpatterns = [
    path("files/", include(router.urls))
]
