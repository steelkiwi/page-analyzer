from django.contrib import admin
from django.utils.translation import gettext as _

from imagekit.admin import AdminThumbnail

from files.models import Avatar


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ("id", "file_name", "creator", "created")
    list_display_links = ("file_name",)
    fieldsets = (
        (None, {'fields': ("id", "creator", "created")}),
        ("Original image", {'fields': ("file", "size", "file_name", "width", "height", "image")}),
        ("Thumbnail", {'fields': ("thumbnail_url", "thumbnail_width", "thumbnail_height", "thumbnail")}),
    )
    readonly_fields = (
        "size", "file_name", "width", "height", "image", "thumbnail", "created", "id",
        "thumbnail_width", "thumbnail_height", "thumbnail_url",
    )

    image = AdminThumbnail(image_field="file")
    thumbnail = AdminThumbnail(image_field="thumbnail")
    image.short_description = _("image")

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return [[None, {"fields": ["file", "creator"]}]]
        return self.fieldsets

    @staticmethod
    def file_name(obj):
        return obj.file.name

    @staticmethod
    def width(obj):
        return f"{obj.file.width} px"

    @staticmethod
    def height(obj):
        return f"{obj.file.height} px"

    def size(self, obj):
        return self._human_readable_size(obj.file.size, 2)

    def thumbnail_url(self, obj):
        # pylint: disable=no-self-use
        return obj.thumbnail.url

    thumbnail_url.short_description = _("url")

    def thumbnail_width(self, obj):
        # pylint: disable=no-self-use
        return obj.thumbnail.width

    thumbnail_width.short_description = _("width")

    def thumbnail_height(self, obj):
        # pylint: disable=no-self-use
        return obj.thumbnail.height

    thumbnail_height.short_description = _("height")

    @staticmethod
    def _human_readable_size(size, decimal_places=3):
        for unit in ['B', 'KiB', 'MiB', 'GiB', 'TiB']:
            if size < 1024.0:
                break
            size /= 1024.0
        return f"{size:.{decimal_places}f} {unit}"
