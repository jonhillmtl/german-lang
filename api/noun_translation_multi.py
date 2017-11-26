from datetime import datetime

from django.db import connection

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer    

from rest_framework.views import APIView

from .serializers import NounSerializer
from .models import Noun, Answer, UserStats

import json
import random


@api_view(['POST'])
def check(request):
    # TODO JHILL: handle 404 gracefuly
    json_data = json.loads(request.body)
    noun = Noun.objects.get(pk=json_data['noun_id'])

    try:
        json_data = json.loads(request.body)
        correct = noun.check_translation(json_data['translation_id'])

        answer = Answer(
            noun=noun,
            correct=correct,
            user=request.user,
            mode='noun_translation_multi',
            correct_answer=[nt.id for nt in noun.nountranslation_set.all()],
            answer=json_data,
            correction=False)
        answer.save()
        print(answer.id)
        return JsonResponse(dict(
            correct=correct,
            correct_answer=noun.gender,
            correction_hint=noun.gender_correction,
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
            correct_answer=noun.gender,
            answer=json_data
        ), safe=False)
    except AssertionError as e:
        return JsonResponse(dict(
            success=False,
            error=str(e)
        ))

@api_view(['GET'])
def gender_stats(request):
    # TODO JHILL: Move this onto the user object, make it queryable like crazy
    us = UserStats(request.user)

    return JsonResponse(dict(
        mode_percentage=us.all_time_percentage('noun_gender'),
        all_time_percentage=us.all_time_percentage(),

        mode_last_24h_percentage=us.last_24h_percentage('noun_gender'),
        last_24h_percentage=us.last_24h_percentage(),
        
        succces=True
    ))