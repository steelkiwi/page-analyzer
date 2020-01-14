from allauth.account.models import EmailAddress
from django.db.models.signals import post_save
from factory import DjangoModelFactory, Faker, PostGenerationMethodCall, SubFactory, post_generation
from factory.django import mute_signals

USER_PASSWORD = 'Password1'


class UserFactory(DjangoModelFactory):
    username = Faker('user_name')
    email = Faker('email')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    password = PostGenerationMethodCall('set_password', USER_PASSWORD)

    class Meta:
        model = 'users.User'
        django_get_or_create = ('email',)

    @post_generation
    def populate_email(self, create, extracted, **kwargs):
        if not create:
            return

        if kwargs.get("if_create_email", True):
            EmailAddress.objects.create(user=self, email=self.email, verified=kwargs.get("is_email_verified", True))


@mute_signals(post_save)
class ProfileFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    description = Faker("sentence", nb_words=4)
    birth_date = Faker("date_of_birth", maximum_age=100)

    class Meta:
        model = 'users.Profile'
        django_get_or_create = ('user',)
