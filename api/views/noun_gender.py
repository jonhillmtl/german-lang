from django.http import JsonResponse, HttpRequest
from rest_framework.decorators import api_view

from ..serializers import NounSerializer, AppSessionSerializer
from ..models import Noun, Answer, AppSession

import json


def _save_answer_to_session(request: HttpRequest, answer: Answer) -> AppSession:
    session = AppSession.objects.get(pk=request.COOKIES.get('appsession_id'))

    if session:
        session.update(answer)

    return session


@api_view(['POST'])
def check(request: HttpRequest) -> JsonResponse:
    # TODO JHILL: handle 404 gracefuly
    json_data = json.loads(request.body)
    noun = Noun.objects.get(pk=json_data['noun_id'])

    try:
        json_data = json.loads(request.body)
        correct = noun.check_gender(json_data['gender'])

        answer = Answer(
            noun=noun,
            correct=correct,
            user=request.user,
            mode='noun_gender',
            correct_answer=noun.gender,
            answer=json_data,
            correction=False)
        answer.save()

        session = _save_answer_to_session(request, answer)

        return JsonResponse(dict(
            correct=correct,
            correct_answer=noun.gender,
            noun=NounSerializer(noun).data,
            session=AppSessionSerializer(session).data,
            success=True
        ), safe=False)

    except AssertionError as e:
        return JsonResponse(dict(
            success=False,
            error=str(e)
        ))


@api_view(['POST'])
def correction(request: HttpRequest) -> JsonResponse:
    json_data = json.loads(request.body)
    noun = Noun.objects.get(pk=json_data['noun_id'])

    try:
        json_data = json.loads(request.body)
        correct = noun.check_gender_correction(json_data['correction'])

        answer = Answer(
            noun=noun,
            correct=correct,
            user=request.user,
            mode='noun_gender',
            answer=json_data,
            correction=True)
        answer.save()

        return JsonResponse(dict(
            success=correct,
            correct_answer=noun.gender,
            answer=json_data
        ), safe=False)
    except AssertionError as e:
        return JsonResponse(dict(
            success=False,
            error=str(e)
        ))
