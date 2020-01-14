from django.urls import path, include

from rest_auth.registration.views import RegisterView
from rest_auth.views import LogoutView, LoginView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from rest_framework.routers import SimpleRouter, Route

from users.views import ProfileAPIViewSet, ResendVerificationEmailView, VerifyEmailView


class ProfileRouter(SimpleRouter):
    routes = [
        Route(
            url=r"^{prefix}{trailing_slash}$",
            mapping={"get": "retrieve",
                     "put": "update",
                     "patch": "partial_update"},
            name="{basename}-detail",
            detail=False,
            initkwargs={"suffix": "instance"},
        )
    ]


profile_router = ProfileRouter()
profile_router.register("my", ProfileAPIViewSet, "my")

register_urls = [
    path("resend-email/", ResendVerificationEmailView.as_view(), name="resend-email"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path("", RegisterView.as_view(), name="register"),
]

auth_urls = [
    path("logout/", LogoutView.as_view(), name="logout"),
    path("login/", LoginView.as_view(), name="login"),
    path("password/reset/", PasswordResetView.as_view(), name="password-reset"),
    path("password/reset/confirm/", PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
    path("password/change/", PasswordChangeView.as_view(), name="password-change"),
    path("register/", include(register_urls)),
]

urlpatterns = [
    path("profiles/", include((profile_router.urls, "profiles"))),
    path("auth/", include((auth_urls, "auth"))),
]
