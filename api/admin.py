from django.contrib import admin

from .models import Noun, NounTranslation, Answer

admin.site.register(Noun)
admin.site.register(NounTranslation)
admin.site.register(Answer)