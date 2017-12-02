from django.shortcuts import render, redirect
from api.models import GrammarQueryModel, GrammarQueryStub, Noun
import json

def noun_gender(request):
    return render(request, 'apps/noun_gender.html')

def noun_translation_multi(request):
    return render(request, 'apps/noun_translation_multi.html')

def noun_pluralization(request):
    return render(request, 'apps/noun_pluralization.html')

def noun_translation(request):
    return render(request, 'apps/noun_translation.html')

def verb_translation_multi(request):
    return render(request, 'apps/verb_translation_multi.html')

def verb_pp_multi(request):
    return render(request, 'apps/verb_pp_multi.html')

def stats(request):
    grammar_query_stub = GrammarQueryStub(user=request.user)
    weak_nouns = Noun.weak(grammar_query_stub)

    return render(request, 'apps/misc/stats.html', dict(
        weak_nouns=weak_nouns
    ))

def prefs(request):
    if request.method == 'GET':
        levels = GrammarQueryModel.levels()
        tags = GrammarQueryModel.all_tags()

        return render(request, 'apps/misc/prefs.html', dict(levels=levels, tags=tags))
    else:
        # TODO JHILL: could be prettier
        request.user.profile.levels = [json.loads(l.replace('\'', '"')) for l in request.POST.getlist('level')]
        request.user.profile.tags = request.POST.getlist('tag')
        request.user.profile.save()

        return redirect('prefs')