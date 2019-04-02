from django.http import JsonResponse, HttpRequest
from rest_framework.decorators import api_view

from ..serializers import NounSerializer
from ..models import Noun, Answer

import json


@api_view(['POST'])
def check(request: HttpRequest) -> JsonResponse:
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

