from django.shortcuts import render, redirect
from api.models import GrammarQueryModel, GrammarQueryStub, Noun
import json
from django.http import HttpResponse

def noun_flash(request):
    return render(request, 'apps/noun_flash.html')

def noun_gender(request):
    return render(request, 'apps/noun_gender.html')

def noun_translation_multi(request):
    return render(request, 'apps/noun_translation_multi.html')

def noun_pluralization(request):
    return render(request, 'apps/noun_pluralization.html')

def noun_translation(request):
    return render(request, 'apps/noun_translation.html')

def noun_article_missing(request):
    return render(request, 'apps/noun_article_missing.html')

def verb_translation_multi(request):
    return render(request, 'apps/verb_translation_multi.html')

def verb_pp_multi(request):
    return render(request, 'apps/verb_pp_multi.html')

def pronouns_missing(request):
    language_code = 'de_DE'
    f = open("./data/{}/pronouns.json".format(language_code))
    pronouns = f.read()

    return render(
        request,
        'apps/pronouns_missing.html',
        dict(
            pronouns=pronouns
        )
    )

def pos_pronouns_missing(request):
    language_code = 'de_DE'
    f = open("./data/{}/pos_pronouns.json".format(language_code))
    pronouns = f.read()
    try:
        jsoned = json.loads(pronouns)
    except ValueError:
        return HttpResponse("nope")

    return render(
        request,
        'apps/pos_pronouns_missing.html',
        dict(
            pronouns=pronouns
        )
    )

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