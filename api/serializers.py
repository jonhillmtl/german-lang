from rest_framework import serializers
from .models import Noun

class NounSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noun
        fields = '__all__'