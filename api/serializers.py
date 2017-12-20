from rest_framework import serializers
from .models import Noun, Verb, Adjective

class NounFlashSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noun
        fields = (
            'id',
            'singular_form',
            'plural_form',
            'gender',
            'translations_text',
            'articled'
        )

class NounSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noun
        fields = (
            'id',
            'singular_form',
            'plural_form',
            'gender',
            'level',
            'chapter',
            'articles',
            'articled',
            'translations_text',
            'possible_translations',
        )
        
class AdjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adjective
        fields = (
            'id',
            'adjective',
            'level',
            'chapter',
            'translations_text',
            'possible_translations',
        )


class VerbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verb
        fields = (
            'id',
            'verb',
            'past_participle',
            'possible_translations',
            'possible_past_participles',
            'translations_text')