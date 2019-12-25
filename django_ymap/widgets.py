from django.forms.widgets import TextInput
from django.conf import settings


class YmapCoordFieldWidget(TextInput):
    attrs = None

    def __init__(self, attrs=None):
        default = {'class': 'ymap_field', 'style': 'display:none'}
        if attrs:
            default.update(attrs)
        super(YmapCoordFieldWidget, self).__init__(default)

    class Media:
        js = ('//api-maps.yandex.ru/2.1/?apikey={}&lang=ru-RU'.format(getattr(settings, 'YANDEX_MAP_API_KEY', '')), 'django_ymap/init.js')
