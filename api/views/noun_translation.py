from django.http import JsonResponse
from rest_framework.decorators import api_view

from ..models import Noun, Answer

import json


@api_view(['POST'])
def check(request):
    # TODO JHILL: handle 404 gracefuly
    json_data = json.loads(request.body)
    noun = Noun.objects.get(pk=json_data['noun_id'])

    try:
        json_data = json.loads(request.body)
        correct = noun.check_translation(json_data['translation'])
        correction = json_data['correction']

        answer = Answer(
            noun=noun,
            correct=correct,
            user=request.user,
            mode='noun_translation',
            correct_answer=noun.translations_text,
            answer=json_data,
            correction=correction)
        answer.save()

        return JsonResponse(dict(
            correct=correct,
            correct_answer=noun.translations_text,
            correction_hint=noun.translations_text,
            success=True
        ), safe=False)
    except AssertionError as e:
        return JsonResponse(dict(
            success=False,
            error=str(e)
        ))
