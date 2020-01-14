from django.contrib import admin

from flatpages.models import FlatPage, SupportCenterElement, SupportCenterCategory, ContactUsRequest


@admin.register(FlatPage)
class FlatPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'created', 'modified')
    list_filter = ('status',)
    readonly_fields = ('status_changed', 'created', 'modified')
    search_fields = ('slug', 'title')
    prepopulated_fields = {
        'slug': ('title',)
    }


class SupportCenterElementInline(admin.StackedInline):
    model = SupportCenterElement
    fields = ('category', 'order', 'question', 'answer', 'status', 'status_changed')
    readonly_fields = ('status_changed',)
    extra = 0


@admin.register(SupportCenterCategory)
class SupportCenterCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status')
    readonly_fields = ('id', 'status_changed')
    prepopulated_fields = {
        'slug': ('title',)
    }
    inlines = (SupportCenterElementInline,)


def resolve_request(modeladmin, request, queryset):
    queryset.update(status=ContactUsRequest.STATUS.resolved)


resolve_request.short_description = "Resolve request"


@admin.register(ContactUsRequest)
class ContactUsRequestAdmin(admin.ModelAdmin):
    list_display = ('email', 'status', 'title', 'category')
    list_filter = ('status', )
    readonly_fields = ('status_changed',)
    actions = [resolve_request, ]
