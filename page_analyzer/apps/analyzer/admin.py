from django.contrib import admin
from .models import Analysis, Tag, Link


# Register your models here.


class HeadingsInline(admin.TabularInline):
    model = Tag


class LinksInline(admin.TabularInline):
    model = Link


class AnalysisAdmin(admin.ModelAdmin):
    inlines = [HeadingsInline, LinksInline]


admin.site.register(Analysis, AnalysisAdmin)
