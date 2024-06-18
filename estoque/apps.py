from django.apps import AppConfig


class EstoqueConfig(AppConfig):
    name = 'estoque'


    def ready(self):
        from .templatetags import custom_filters
