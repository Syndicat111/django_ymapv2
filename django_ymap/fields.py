# * coding: utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.db import models
from django.contrib.postgres.fields import JSONField
from django_ymap.widgets import YmapCoordFieldWidget
from django.core.exceptions import ValidationError
from six import string_types
import json


class YmapCoord(JSONField):
    def __init__(self, start_query=u'Россия', size_width=500, size_height=500, **kwargs):
        init = {'default': {'coordinates': [], 'address': None}}
        init.update(**kwargs)
        self.start_query, self.size_width, self.size_height = start_query, size_width, size_height
        super(YmapCoord, self).__init__(**init)

    def formfield(self, **kwargs):
        defaults = {'widget': YmapCoordFieldWidget(attrs={
            "data-start_query": self.start_query,
            "data-size_width": self.size_width,
            "data-size_height": self.size_height,
        })}
        defaults.update(kwargs)
        return super(YmapCoord, self).formfield(**defaults)

    def validate(self, value, model_instance):
        super(YmapCoord, self).validate(value, model_instance)
        coordinates = value.get('coordinates')
        address = value.get('address')
        if len(value.keys()) != 2:
            raise ValidationError(_('Invalid format[2]'))

        if address and not isinstance(address, string_types):
            raise ValidationError(_('Invalid format[3]'))
        if not isinstance(coordinates, list):
            raise ValidationError(_('Invalid format[4]'))
        try:
            map(float, coordinates[:2])
        except (ValueError, IndexError, TypeError):
            raise ValidationError(_('Invalid format[4]'))
