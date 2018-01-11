from django.contrib import admin

from .models import Noun, Verb, Translation, Answer, Profile, Phrase

admin.site.register(Noun)
admin.site.register(Translation)
admin.site.register(Answer)
admin.site.register(Verb)
admin.site.register(Profile)
admin.site.register(Phrase)