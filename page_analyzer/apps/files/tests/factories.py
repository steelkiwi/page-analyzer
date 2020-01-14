import factory

from files.models import Avatar
from users.tests.factories import UserFactory


class AvatarFactory(factory.DjangoModelFactory):
    creator = factory.SubFactory(UserFactory)
    file = factory.django.ImageField()

    class Meta:
        model = Avatar
