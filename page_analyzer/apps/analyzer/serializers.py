from rest_framework import serializers
from .models import Analysis, Tag, Link


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['tag', 'count']
        model = Tag


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['link_type', 'count', 'inaccessible_count']
        model = Link


class AnalysisTriggerSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    url = serializers.URLField()

    def perform(self):
        analysis = Analysis(**self.validated_data)
        analysis.save()
        analysis.perform_analysis()
        return analysis


class AnalysisSerializer(serializers.ModelSerializer):
    links = LinkSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        fields = '__all__'
        extra_fields = ['links']
        model = Analysis
