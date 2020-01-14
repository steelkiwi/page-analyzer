from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from flatpages.models import FlatPage, SupportCenterCategory
from flatpages.serializer import (
    ContactUsSerializer, SupportCenterElementSerializer, FlatPageSerializer, FlatPageListSerializer,
    SupportCenterCategorySerializer
)


class FlatPageViewSet(ReadOnlyModelViewSet):
    queryset = FlatPage.objects.active()
    permission_classes = (AllowAny,)
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return FlatPageListSerializer
        return FlatPageSerializer


class SupportCenterViewSet(ListModelMixin, GenericViewSet):
    """
    list:
        List of all available support centre categories.
    articles:
        List of all available support centre articles for a category.
    """
    permission_classes = (AllowAny,)
    queryset = SupportCenterCategory.objects.active()
    serializer_class = SupportCenterCategorySerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    @action(detail=True, serializer_class=SupportCenterElementSerializer)
    def elements(self, request, *args, **kwargs):
        category = self.get_object()
        queryset = category.elements.active()

        page = self.paginate_queryset(queryset)
        if page is not None:  # pragma: no cover
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ContactUsView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ContactUsSerializer
