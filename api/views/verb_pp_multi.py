from datetime import datetime

from django.db import connection

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from rest_framework.views import APIView

from ..serializers import NounSerializer, VerbSerializer
from ..models import Verb, Answer, UserStats

import json
import random


@api_view(['POST'])
def check(request):
    # TODO JHILL: handle 404 gracefuly
    json_data = json.loads(request.body)
    verb = Verb.objects.get(pk=json_data['verb_id'])

    try:
        json_data = json.loads(request.body)
        correct = verb.check_past_participle(json_data['answer'])

        answer = Answer(
            verb=verb,
            correct=correct,
            user=request.user,
            mode='verb_pp_multi',
            correct_answer=verb.past_participle,
            answer=json_data,
            correction=False)
        answer.save()

        return JsonResponse(dict(
            correct=correct,
            success=True
        ), safe=False)
    except AssertionError as e:
        return JsonResponse(dict(
            success=False,
            error=str(e)
        ))