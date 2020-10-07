from django.contrib import admin
from .models import Question, Choice # current working directory models

# Register your models here.

admin.site.register(Question) # create an admin interface
admin.site.register(Choice)