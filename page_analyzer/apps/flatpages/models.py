from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from ckeditor.fields import RichTextField
from model_utils import Choices
from model_utils.models import StatusModel, TimeStampedModel


class FlatPageQuerySet(models.QuerySet):
    def active(self):
        return self.exclude(status=self.model.STATUS.hidden)


class FlatPage(StatusModel, TimeStampedModel):
    STATUS = Choices(
        ('published', _('Published')),
        ('hidden', _('Hidden'))
    )

    slug = models.SlugField()
    title = models.CharField(_('Title'), max_length=100)
    content = RichTextField(_('Content'))

    objects = FlatPageQuerySet.as_manager()

    class Meta:
        ordering = ['slug']
        verbose_name = _('Flat Page')
        verbose_name_plural = _('Flat Pages')

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('api:flatpages:page-detail', kwargs={'slug': self.slug})


class SupportCenterCategoryQuerySet(models.QuerySet):
    def active(self):
        return self.exclude(status=self.model.STATUS.hidden)


class SupportCenterCategory(StatusModel, models.Model):
    STATUS = Choices(
        ('published', _('Published')),
        ('hidden', _('Hidden')),
    )

    slug = models.SlugField()
    title = models.CharField(_('Title'), max_length=100)

    objects = SupportCenterCategoryQuerySet.as_manager()

    class Meta:
        ordering = ['slug']
        verbose_name = _('Support Center')
        verbose_name_plural = _('Support Center')

    def __str__(self):
        return self.title


class SupportCenterElementQuerySet(models.QuerySet):
    def active(self):
        return self.exclude(status=self.model.STATUS.hidden)


class SupportCenterElement(StatusModel):
    STATUS = Choices(
        ('published', _('Published')),
        ('hidden', _('Hidden'))
    )

    category = models.ForeignKey(
        'SupportCenterCategory', on_delete=models.CASCADE, related_name='elements', related_query_name='element'
    )
    question = RichTextField(_('Question content'))
    answer = RichTextField(_('Answer text'))
    order = models.PositiveSmallIntegerField(_('Order'))

    objects = SupportCenterElementQuerySet.as_manager()

    class Meta:
        ordering = ('category', 'order')
        verbose_name = _('Support Center Element')
        verbose_name_plural = _('Support Center Elements')


class ContactUsRequest(StatusModel, TimeStampedModel):
    STATUS = Choices(
        ('open', _('Open')),
        ('resolved', _('Resolved'))
    )

    email = models.EmailField(_('Email'))
    title = models.CharField(_('Title'), max_length=250)
    category = models.CharField(_('Category'), max_length=250)
    description = models.TextField(_('Description'))

    class Meta:
        ordering = ['id']
        verbose_name = _('Contact Us Request')
        verbose_name_plural = _('Contact Us Requests')

    def __str__(self):
        return f'Request {self.id} by {self.email}'
