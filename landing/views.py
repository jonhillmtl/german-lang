from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse


@login_required
def index(request: HttpRequest) -> JsonResponse:
    return render(request, 'landing/index.html')