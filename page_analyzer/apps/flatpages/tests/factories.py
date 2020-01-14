import factory
from django.utils.text import slugify

from flatpages.models import FlatPage, SupportCenterElement, SupportCenterCategory, ContactUsRequest


class FlatPageFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('text', max_nb_chars=10, ext_word_list=None)
    content = factory.Faker('paragraphs', nb=3, ext_word_list=None)
    slug = factory.LazyAttribute(lambda o: slugify(o.title))

    class Meta:
        model = FlatPage


class SupportCenterCategoryFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('text', max_nb_chars=20, ext_word_list=None)
    slug = factory.LazyAttribute(lambda o: slugify(o.title))

    class Meta:
        model = SupportCenterCategory


class SupportCenterElementFactory(factory.django.DjangoModelFactory):
    category = factory.SubFactory(SupportCenterCategoryFactory)
    question = factory.Faker('text', max_nb_chars=250, ext_word_list=None)
    answer = factory.Faker('text', max_nb_chars=250, ext_word_list=None)
    order = factory.Sequence(lambda n: n)

    class Meta:
        model = SupportCenterElement


class ContactsUsFactory(factory.django.DjangoModelFactory):
    email = factory.Faker('email')
    title = factory.Faker('text', max_nb_chars=250, ext_word_list=None)
    category = factory.Faker('text', max_nb_chars=100, ext_word_list=None)
    description = factory.Faker('text', max_nb_chars=250, ext_word_list=None)

    class Meta:
        model = ContactUsRequest
