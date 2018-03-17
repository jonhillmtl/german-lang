from django.shortcuts import render, redirect
from api.models import GrammarQueryModel, GrammarQueryStub, Noun, AppSession
import json
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
import datetime

def _render_app_session(request, app_name, template, context=dict()):
    current_appsession_id = request.COOKIES.get('appsession_id')
    if current_appsession_id is not None:
        current_session = AppSession.objects.get(pk=current_appsession_id)
        if current_session:
            # TODO JHILL: a function instead? maybe delete it if it has
            # no answers?
            current_session.finished_at = datetime.datetime.now()
            current_session.save()

    session = AppSession()
    session.app_name = app_name
    session.user = request.user
    session.save()

    context['session_id'] = session.id

    response = render(request, template, context)
    response.set_cookie('appsession_id', session.id)
    return response

@login_required
def noun_list(request):
    nouns = Noun.objects.order_by('level', 'chapter', 'singular_form').all()

    return render(request, 'apps/noun_list.html', dict(
        nouns=nouns
    ))

@login_required
def noun_random_feed(request):
    query_stub = GrammarQueryStub(mode='random', user=request.user)
    nouns = [Noun.random(query_stub)[0] for i in range(0, 100)]

    return render(request, 'apps/noun_random_feed.html', dict(
        nouns=nouns
    ))

@login_required
def noun_flash(request):
    return render(request, 'apps/noun_flash.html')

@login_required
def noun_gender(request):
    return _render_app_session(request, 'noun_gender', 'apps/noun_gender.html')

@login_required
def noun_translation_multi(request):
    return render(request, 'apps/noun_translation_multi.html')

@login_required
def noun_pluralization(request):
    return render(request, 'apps/noun_pluralization.html')

@login_required
def noun_translation(request):
    return render(request, 'apps/noun_translation.html')

@login_required
def noun_article_missing(request):
    return render(request, 'apps/noun_article_missing.html')

@login_required
def verb_translation_multi(request):
    return render(request, 'apps/verb_translation_multi.html')

@login_required
def verb_pp_multi(request):
    return render(request, 'apps/verb_pp_multi.html')

@login_required
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

@login_required
def pos_pronouns_missing(request):
    # TODO JHILL: get language code from cookie
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

def adjective_translation_multi(request):
    return render(request, 'apps/adjective_translation_multi.html')

def phrase_translation_multi(request):
    return render(request, 'apps/phrase_translation_multi.html')

def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            
            return redirect('index')
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def stats(request):
    grammar_query_stub = GrammarQueryStub(user=request.user)
    weak_nouns = Noun.weak(grammar_query_stub)

    return render(request, 'apps/misc/stats.html', dict(
        weak_nouns=weak_nouns
    ))

@login_required
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