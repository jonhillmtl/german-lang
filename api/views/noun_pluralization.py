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
        correct = noun.check_plural(json_data['plural'])
        correction = json_data['correction']

        answer = Answer(
            noun=noun,
            correct=correct,
            user=request.user,
            mode='noun_pluralization',
            correct_answer=noun.gendered_plural,
            answer=json_data,
            correction=correction)
        answer.save()

        return JsonResponse(dict(
            correct=correct,
            correct_answer=noun.gendered_plural,
            correction_hint=noun.gendered_plural,
            success=True
        ), safe=False)
    except AssertionError as e:
        return JsonResponse(dict(
            success=False,
            error=str(e)
        ))
