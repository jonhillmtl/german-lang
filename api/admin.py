from django.contrib import admin

from .models import Noun, Verb, Translation, Answer

admin.site.register(Noun)
admin.site.register(Translation)
admin.site.register(Answer)