import os
import uuid

from django.conf import settings
from django.core.files.storage import default_storage
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _

from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFit, Anchor
from model_utils.models import TimeStampedModel


def get_file_upload_path(instance, filename):
    _, ext = os.path.splitext(filename)

    return '{0}/{1}/{2}{3}'.format(
        instance.upload_prefix,
        timezone.now().strftime('%y/%m'),
        uuid.uuid4().hex,
        ext.lower())


class FileQuerySet(models.QuerySet):  # pragma: no cover

    def delete(self):
        for obj in self.iterator():
            default_storage.delete(obj.file.name)
        return super().delete()


class File(TimeStampedModel):
    creator = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to=get_file_upload_path)

    objects = FileQuerySet.as_manager()

    class Meta:
        abstract = True
        verbose_name = _("file")
        verbose_name_plural = _("files")

    def __str__(self):
        return f"File - user {self.creator_id}"

    def delete(self, using=None, keep_parents=False):
        default_storage.delete(self.file.name)
        return super().delete(using, keep_parents)

    @property
    def upload_prefix(self):
        return self.__class__.__name__.lower()


class AvatarQuerySet(models.QuerySet):

    def delete(self):
        for obj in self.iterator():
            default_storage.delete(obj.thumbnail.name)
            default_storage.delete(obj.file.name)
        return super().delete()


class Avatar(File):
    file = models.ImageField(upload_to=get_file_upload_path)
    thumbnail = ImageSpecField(source='file',
                               processors=[ResizeToFit(*settings.FILES_AVATAR_THUMB_SIZE,
                                                       anchor=Anchor.CENTER, upscale=False)],
                               format=settings.FILES_AVATAR_EXTENSION,
                               options={'quality': settings.FILES_AVATAR_THUMB_QUALITY})
    objects = AvatarQuerySet.as_manager()

    class Meta:
        verbose_name = _("user's avatar")
        verbose_name_plural = _("users' avatars")

    def __str__(self):
        return f"Avatar of user {self.creator_id}"

    def delete(self, using=None, keep_parents=False):
        default_storage.delete(self.thumbnail.name)  # pylint: disable=no-member
        return super().delete(using, keep_parents)

    def get_absolute_url(self):
        return reverse("api:files:avatars-detail", args=(self.id,))
