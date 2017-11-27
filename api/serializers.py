from rest_framework import serializers
from .models import Noun, Verb

class NounSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noun
        fields = ('id', 'singular_form', 'plural_form', 'gender', 'level',
                  'chapter', 'gendered_singular', 'gendered_plural', 'translations_text',
                  'possible_translations')

class VerbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verb
        fields = ('id', 'verb', 'past_participle', 'possible_translations', )