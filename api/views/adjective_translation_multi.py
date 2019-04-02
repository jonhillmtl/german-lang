from django.http import JsonResponse
from rest_framework.decorators import api_view

from ..serializers import AdjectiveSerializer
from ..models import Adjective, Answer

import json


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
            adjective=AdjectiveSerializer(adjective).data,
            success=True
        ), safe=False)

    except AssertionError as e:
        return JsonResponse(dict(
            success=False,
            error=str(e)
        ))
