from django.contrib import admin

from .models import Track, Question, Choice

# Register your models here.
admin.site.register(Track)
admin.site.register(Question)
admin.site.register(Choice)
