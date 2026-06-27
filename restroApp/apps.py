from django.apps import AppConfig


class RestroappConfig(AppConfig):
    name = 'restroApp'

    def ready(self):
        from . import signals
