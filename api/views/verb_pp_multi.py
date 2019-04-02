from django.http import JsonResponse
from rest_framework.decorators import api_view

from ..models import Verb, Answer

import json


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
            correction=False
        )
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