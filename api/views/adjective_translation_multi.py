from datetime import datetime

from django.db import connection

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from rest_framework.views import APIView

from ..serializers import AdjectiveSerializer
from ..models import Adjective, Answer, UserStats

import json
import random


@api_view(['POST'])
def check(request):
    # TODO JHILL: handle 404 gracefuly
    json_data = json.loads(request.body)
    adjective = Adjective.objects.get(pk=json_data['adjective_id'])

    try:
        json_data = json.loads(request.body)
        correct = adjective.check_translation_id(json_data['answer'])

        answer = Answer(
            adjective=adjective,
            correct=correct,
            user=request.user,
            mode='adjective_translation_multi',
            correct_answer=[nt.id for nt in adjective.translation_set.all()],
            answer=json_data,
            correction=False)
        answer.save()
        
        return JsonResponse(dict(
            correct=correct,
            correct_answer=[nt.id for nt in adjective.translation_set.all()],
            correction_hint="",
            noun=AdjectiveSerializer(adjective).data,
            success=True
        ), safe=False)
    
    except AssertionError as e:
        return JsonResponse(dict(
            success=False,
            error=str(e)
        ))
