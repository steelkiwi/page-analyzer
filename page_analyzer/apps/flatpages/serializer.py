from rest_framework import serializers

from flatpages.models import ContactUsRequest, FlatPage, SupportCenterElement, SupportCenterCategory


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUsRequest
        fields = ('email', 'title', 'category', 'description',)


class FlatPageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlatPage
        fields = ('title', 'slug')
        read_only_fields = ('title', 'slug')


class FlatPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlatPage
        fields = ('title', 'slug', 'content')
        read_only_fields = ('title', 'slug', 'content')


class SupportCenterCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportCenterCategory
        fields = ('title', 'slug')
        read_only_fields = ('title', 'slug')


class SupportCenterElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportCenterElement
        fields = ('question', 'answer', 'order')
        read_only_fields = ('question', 'answer', 'order')
