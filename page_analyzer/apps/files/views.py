from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import GenericViewSet

from files.serializers import AvatarSerializer
from files.models import Avatar


class AvatarAPIViewSet(RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = AvatarSerializer
    queryset = Avatar.objects.all()

    def get_permissions(self):
        if self.action == "retrieve":
            self.permission_classes = (AllowAny,)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
