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
from .models import Noun, Answer

import json

@api_view(['GET'])
def random_noun(request):
    # TODO JHILL: need to specify language code, or provide a default
    noun = Noun.random()

    return JsonResponse(dict(
        noun=NounSerializer(noun).data,
        success=True
    ), safe=False)


@api_view(['GET'])
def noun_view(request, pk):
    # TODO JHILL: handle 404 gracefuly
    noun = Noun.objects.get(pk=pk)

    return JsonResponse(dict(
        noun=NounSerializer(noun).data,
        success=True
    ), safe=False)

@api_view(['POST'])
def noun_gender_check(request, pk):
    # TODO JHILL: handle 404 gracefuly
    noun = Noun.objects.get(pk=pk)

    try:
        json_data = json.loads(request.body)
        correct, correct_answer = noun.check_gender(json_data['gender'])

        answer = Answer(
            object_id=noun.id,
            object_type="Noun",
            correct=correct,
            user=request.user,
            mode='noun_gender')
        answer.save()
        
        return JsonResponse(dict(
            correction=correct_answer,
            results=correct,
            noun=NounSerializer(noun).data,
            success=True
        ), safe=False)
    except AssertionError as e:
        return JsonResponse(dict(
            success=False,
            error=str(e)
        ))

@api_view(['POST'])
def noun_gender_check_correction(request, pk):
    # TODO JHILL: handle 404 gracefuly
    noun = Noun.objects.get(pk=pk)

    try:
        return JsonResponse(dict(
            success=True
        ), safe=False)
    except AssertionError as e:
        return JsonResponse(dict(
            success=False,
            error=str(e)
        ))

@api_view(['POST'])
def noun_answer_gender_check(request, pk):
    # TODO JHILL: handle 404 gracefuly
    noun = Noun.objects.get(pk=pk)

    try:
        json_data = json.loads(request.body)

        results, singular_answers, plural_answers = noun.check_answers(json_data)

        return JsonResponse(dict(
            results=results,
            singular_answers=singular_answers,
            plural_answers=plural_answers,
            noun=NounSerializer(noun).data,
            success=True
        ), safe=False)
    except AssertionError as e:
        return JsonResponse(dict(
            success=False,
            error=str(e)
        ))