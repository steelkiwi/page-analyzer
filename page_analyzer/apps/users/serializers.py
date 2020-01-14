from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext as _

from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress
from allauth.account.utils import setup_user_email
from allauth.utils import email_address_exists
from rest_auth.models import TokenModel
from rest_auth.serializers import TokenSerializer as BaseTokenSerializer
from rest_auth.serializers import PasswordResetSerializer as BasePasswordResetSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from users.models import User, Profile


class RegisterSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    email = serializers.EmailField(required=True, help_text=_('Email address'))
    password1 = serializers.CharField(write_only=True, help_text=_('Password'))
    password2 = serializers.CharField(write_only=True, help_text=_('Password Confirmation'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cleaned_data = {}

    @staticmethod
    def validate_email(email):
        email = get_adapter().clean_email(email)
        if email and email_address_exists(email):
            raise serializers.ValidationError(_("A user is already registered with this e-mail address."))
        return email

    @staticmethod
    def validate_password1(password):
        return get_adapter().clean_password(password)

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return attrs

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', '')
        }

    def save(self, request):  # pylint: disable=arguments-differ
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


class EmailVerificationSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    email = serializers.EmailField()

    class Meta:
        model = EmailAddress
        fields = ("email",)

    @staticmethod
    def validate_email(value):
        try:
            email = EmailAddress.objects.get(email=value)
        except EmailAddress.DoesNotExist:
            raise ValidationError(_("Email is not registered."))
        else:
            if email.verified:
                raise ValidationError(_("Email was already verified."))
        return value

    def send_email(self):
        obj = EmailAddress.objects.get(email=self.validated_data["email"])
        obj.send_confirmation()


class UserShortSerializer(serializers.ModelSerializer):
    is_email_verified = serializers.BooleanField(read_only=True, source="get_is_email_verified")

    class Meta:
        model = User
        fields = ("id", "email", "is_email_verified")
        read_only_fields = fields

    @staticmethod
    def get_is_email_verified(obj):
        if hasattr(obj, "is_email_verified"):
            return getattr(obj, "is_email_verified")
        return EmailAddress.objects.filter(email=obj.email, user=obj, verified=True).exists()


class TokenSerializer(BaseTokenSerializer):
    user = UserShortSerializer(read_only=True)

    class Meta:
        model = TokenModel
        fields = ("key", "user")
        read_only_fields = fields


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[
            UnicodeUsernameValidator(),
            UniqueValidator(queryset=User.objects.all()),
        ],
    )
    first_name = serializers.CharField(max_length=30, allow_blank=True)
    last_name = serializers.CharField(max_length=150, allow_blank=True)

    class Meta:
        model = Profile
        user_fields = ("username", "first_name", "last_name")
        fields = ("description", "birth_date", "avatar") + user_fields

    def update(self, instance, validated_data):
        validated_data = self._update_user(instance, validated_data)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        self.fields["username"] = serializers.CharField(source="user.username")
        self.fields["first_name"] = serializers.CharField(source="user.first_name")
        self.fields["last_name"] = serializers.CharField(source="user.last_name")
        return super().to_representation(instance)

    def _update_user(self, instance, validated_data):
        user = instance.user
        data = {field: validated_data.get(field, "") for field in self.Meta.user_fields}

        for field, value in data.items():
            if not self.partial and not value:
                continue
            setattr(user, field, value)
        user.save()
        return {
            field: value
            for field, value in validated_data.items()
            if field not in self.Meta.user_fields
        }


class PasswordResetSerializer(BasePasswordResetSerializer):  # pylint: disable=abstract-method

    def get_email_options(self):
        return {
            "password_reset_url": settings.DJANGO_FRONTEND_PASSWORD_RESET_URL
        }
