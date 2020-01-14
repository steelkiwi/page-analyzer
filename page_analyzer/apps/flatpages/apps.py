from contextlib import suppress

from django.apps import AppConfig


class FlatpagesConfig(AppConfig):
    name = 'flatpages'

    def ready(self):
        with suppress(ImportError):
            from flatpages import signals  # noqa: F401
