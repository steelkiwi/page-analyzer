from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import caches
from django.conf import settings
from .serializers import AnalysisTriggerSerializer, AnalysisSerializer
from .models import Analysis



class AnalysisTriggerView(GenericAPIView):
    serializer_class = AnalysisTriggerSerializer
    permission_classes = (AllowAny,)

    cache = caches[settings.ANALYSIS_CACHE]
    ttl = getattr(settings, "ANALYSIS_CACHE_TTL", None)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        url = serializer.validated_data['url']
        cached_id = self.cache.get(url)
        if cached_id:
            try:
                analysis = Analysis.objects.get(pk=cached_id)
            except Analysis.DoesNotExist:
                analysis = serializer.perform()
                self.cache.set(url, analysis.pk, self.ttl)
        else:
            analysis = serializer.perform()
            self.cache.set(url, analysis.pk, self.ttl)
        response_serializer = AnalysisSerializer(analysis)
        return Response(data=response_serializer.data, status=status.HTTP_200_OK)
