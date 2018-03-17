from datetime import datetime

from django.db import connection

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer    

from rest_framework.views import APIView

from ..serializers import NounSerializer, AppSessionSerializer
from ..models import Noun, Answer, UserStats, AppSession

import json
import random

def _save_answer_to_session(request, answer):
    session = AppSession.objects.get(pk=request.COOKIES.get('appsession_id'))

    if session:
        session.update(answer)

    return session

@api_view(['POST'])
def check(request):
    # TODO JHILL: handle 404 gracefuly
    json_data = json.loads(request.body)
    noun = Noun.objects.get(pk=json_data['noun_id'])

    try:
        json_data = json.loads(request.body)
        correct = noun.check_gender(json_data['gender'])

        answer = Answer(
            noun=noun,
            correct=correct,
            user=request.user,
            mode='noun_gender',
            correct_answer=noun.gender,
            answer=json_data,
            correction=False)
        answer.save()
        
        session = _save_answer_to_session(request, answer)

        return JsonResponse(dict(
            correct=correct,
            correct_answer=noun.gender,
            noun=NounSerializer(noun).data,
            session=AppSessionSerializer(session).data,
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
