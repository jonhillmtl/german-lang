from django.http import JsonResponse, HttpRequest
from rest_framework.decorators import api_view
from ..models import Noun, Answer

import json


@api_view(['POST'])
def check(request: HttpRequest) -> JsonResponse:
    # TODO JHILL: handle 404 gracefuly
    # TODO JHILL: also needs to handle modes
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
            correct_answer="TODO JHILL",
            answer=json_data,
            correction=correction)
        answer.save()

        return JsonResponse(dict(
            correct=correct,
            correct_answer="TODO JHILL",
            correction_hint="TODO JHILL",
            success=True
        ), safe=False)
    except AssertionError as e:
        return JsonResponse(dict(
            success=False,
            error=str(e)
        ))
