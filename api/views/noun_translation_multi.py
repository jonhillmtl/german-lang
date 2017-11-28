from datetime import datetime

from django.db import connection

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from rest_framework.views import APIView

from ..serializers import NounSerializer
from ..models import Noun, Answer, UserStats

import json
import random


@api_view(['POST'])
def check(request):
    # TODO JHILL: handle 404 gracefuly
    json_data = json.loads(request.body)
    noun = Noun.objects.get(pk=json_data['noun_id'])

    try:
        json_data = json.loads(request.body)
        correct = noun.check_translation_id(json_data['answer'])

        answer = Answer(
            noun=noun,
            correct=correct,
            user=request.user,
            mode='noun_translation_multi',
            correct_answer=[nt.id for nt in noun.translation_set.all()],
            answer=json_data,
            correction=False)
        answer.save()

        return JsonResponse(dict(
            correct=correct,
            correct_answer=[nt.id for nt in noun.translation_set.all()],
            correction_hint="",
            noun=NounSerializer(noun).data,
            success=True
        ), safe=False)
    except AssertionError as e:
        return JsonResponse(dict(
            success=False,
            error=str(e)
        ))

@api_view(['POST'])
def correction(request):
    json_data = json.loads(request.body)
    noun = Noun.objects.get(pk=json_data['noun_id'])

    try:
        json_data = json.loads(request.body)
        correct = noun.check_gender_correction(json_data['correction'])

        answer = Answer(
            noun=noun,
            correct=correct,
            user=request.user,
            mode='noun_gender',
            correct_answer=noun.gender_correction,
            answer=json_data,
            correction=True)
        answer.save()

        return JsonResponse(dict(
            success=correct,
            answer=json_data
        ), safe=False)
    except AssertionError as e:
        return JsonResponse(dict(
            success=False,
            error=str(e)
        ))
