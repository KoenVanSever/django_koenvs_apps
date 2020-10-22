from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# /i you can make custom (sub)classes


class OneByteField(models.PositiveSmallIntegerField):
    def __init__(self, default=255, validators=[
            MinValueValidator(0), MaxValueValidator(255)], *args, **kwargs):
        super().__init__(default=default, validators=validators, *args, **kwargs)


class TwoByteField(models.PositiveIntegerField):
    def __init__(self, default=65535, validators=[
            MinValueValidator(0), MaxValueValidator(65535)], *args, **kwargs):
        super().__init__(default=default, validators=validators, *args, **kwargs)


class CustomPositiveSmallIntegerField(models.PositiveSmallIntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        super().__init__(self, verbose_name, name, **kwargs)
