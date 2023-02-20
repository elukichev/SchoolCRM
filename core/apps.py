from django.apps import AppConfig
from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

class CoreConfig(AppConfig):
    name = 'core'
