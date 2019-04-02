from django.http import JsonResponse, HttpRequest
from rest_framework.decorators import api_view

from ..serializers import PhraseSerializer
from ..models import Phrase, Answer

import json


@api_view(['POST'])
def check(request: HttpRequest) -> JsonResponse:
    # TODO JHILL: handle 404 gracefuly
    json_data = json.loads(request.body)
    phrase = Phrase.objects.get(pk=json_data['phrase_id'])

    try:
        json_data = json.loads(request.body)
        correct = phrase.check_translation_id(json_data['answer'])

        answer = Answer(
            phrase=phrase,
            correct=correct,
            user=request.user,
            mode='phrase_translation_multi',
            correct_answer=[nt.id for nt in phrase.translation_set.all()],
            answer=json_data,
            correction=False)
        answer.save()

        return JsonResponse(dict(
            correct=correct,
            correct_answer=[nt.id for nt in phrase.translation_set.all()],
            correction_hint="",
            phrase=PhraseSerializer(phrase).data,
            success=True
        ), safe=False)
    except AssertionError as e:
        return JsonResponse(dict(
            success=False,
            error=str(e)
        ))
