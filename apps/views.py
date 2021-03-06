from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from api.models import GrammarQueryModel, GrammarQueryStub, Noun, AppSession

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
import datetime
import json

from typing import Dict


def _render_app_session_view(
    request: HttpRequest,
    app_name: str,
    template: str,
    context: Dict = dict()
) -> HttpResponse:
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

    response = render(request, template, context)
    response.set_cookie('appsession_id', session.id)
    return response


@login_required
def noun_list(request: HttpRequest) -> HttpResponse:
    """
    Render the noun_list app.

    Parameters
    ----------
    request: HttpRequest
        the HttpRequest

    Response
    --------
    HttpResponse
        the HttpResponse with rendered html

    """

    nouns = Noun.objects.order_by('level', 'chapter', 'singular_form').all()

    return _render_app_session_view(request, 'noun_list', 'apps/noun_list.html', dict(
        nouns=nouns
    ))


@login_required
def noun_random_feed(request: HttpRequest) -> HttpResponse:
    """
    Render the noun_random_feed app.

    Parameters
    ----------
    request: HttpRequest
        the HttpRequest

    Response
    --------
    HttpResponse
        the HttpResponse with rendered html

    """

    query_stub = GrammarQueryStub(mode='random', user=request.user)
    nouns = [Noun.random(query_stub)[0] for i in range(0, 100)]

    return _render_app_session_view(request, 'noun_random_feed', 'apps/noun_random_feed.html', dict(
        nouns=nouns
    ))


@login_required
def noun_flash(request: HttpRequest) -> HttpResponse:
    """
    Render the noun_flash app.

    Parameters
    ----------
    request: HttpRequest
        the HttpRequest

    Response
    --------
    HttpResponse
        the HttpResponse with rendered html

    """

    return _render_app_session_view(request, 'noun_flash', 'apps/noun_flash.html')


@login_required
def noun_gender(request: HttpRequest) -> HttpResponse:
    """
    Render the noun_gender app.

    Parameters
    ----------
    request: HttpRequest
        the HttpRequest

    Response
    --------
    HttpResponse
        the HttpResponse with rendered html

    """

    return _render_app_session_view(request, 'noun_gender', 'apps/noun_gender.html')


@login_required
def noun_translation_multi(request: HttpRequest) -> HttpResponse:
    """
    Render the noun_translation_multi app.

    Parameters
    ----------
    request: HttpRequest
        the HttpRequest

    Response
    --------
    HttpResponse
        the HttpResponse with rendered html

    """

    return _render_app_session_view(request, 'noun_translation_multi', 'apps/noun_translation_multi.html')


@login_required
def noun_pluralization(request: HttpRequest) -> HttpResponse:
    """
    Render the noun_pluralization app.

    Parameters
    ----------
    request: HttpRequest
        the HttpRequest

    Response
    --------
    HttpResponse
        the HttpResponse with rendered html

    """

    return _render_app_session_view(request, 'noun_pluralization', 'apps/noun_pluralization.html')


@login_required
def noun_translation(request: HttpRequest) -> HttpResponse:
    """
    Render the noun_translation app.

    Parameters
    ----------
    request: HttpRequest
        the HttpRequest

    Response
    --------
    HttpResponse
        the HttpResponse with rendered html

    """

    return _render_app_session_view(request, 'noun_translation', 'apps/noun_translation.html')


@login_required
def noun_article_missing(request: HttpRequest) -> HttpResponse:
    """
    Render the noun_article_missing app.

    Parameters
    ----------
    request: HttpRequest
        the HttpRequest

    Response
    --------
    HttpResponse
        the HttpResponse with rendered html

    """

    return _render_app_session_view(request, 'noun_article_missing', 'apps/noun_article_missing.html')


@login_required
def verb_translation_multi(request: HttpRequest) -> HttpResponse:
    """
    Render the verb_translation_multi app.

    Parameters
    ----------
    request: HttpRequest
        the HttpRequest

    Response
    --------
    HttpResponse
        the HttpResponse with rendered html

    """

    return _render_app_session_view(request, 'verb_translation_multi', 'apps/verb_translation_multi.html')


@login_required
def verb_pp_multi(request: HttpRequest) -> HttpResponse:
    """
    Render the verb_pp_multi app.

    Parameters
    ----------
    request: HttpRequest
        the HttpRequest

    Response
    --------
    HttpResponse
        the HttpResponse with rendered html

    """

    return _render_app_session_view(request, 'verb_pp_multi', 'apps/verb_pp_multi.html')


@login_required
def pronouns_missing(request: HttpRequest) -> HttpResponse:
    """
    Render the pronouns_missing app.

    Parameters
    ----------
    request: HttpRequest
        the HttpRequest

    Response
    --------
    HttpResponse
        the HttpResponse with rendered html

    """
    language_code = 'de_DE'
    f = open("./data/{}/pronouns.json".format(language_code))
    pronouns = f.read()

    return _render_app_session_view(
        request,
        'pronouns_missing',
        'apps/pronouns_missing.html',
        dict(
            pronouns=pronouns
        )
    )


@login_required
def pos_pronouns_missing(request: HttpRequest) -> HttpResponse:
    """
    Render the pos_pronouns_missing app.

    Parameters
    ----------
    request: HttpRequest
        the HttpRequest

    Response
    --------
    HttpResponse
        the HttpResponse with rendered html

    """

    # TODO JHILL: get language code from cookie
    language_code = 'de_DE'

    f = open("./data/{}/pos_pronouns.json".format(language_code))
    pronouns = f.read()

    return _render_app_session_view(
        request,
        'pos_pronouns_missing',
        'apps/pos_pronouns_missing.html',
        dict(
            pronouns=pronouns
        )
    )


@login_required
def prep_cases_multi(request: HttpRequest) -> HttpResponse:
    """
    Render the prep_cases_multi app.

    Parameters
    ----------
    request: HttpRequest
        the HttpRequest

    Response
    --------
    HttpResponse
        the HttpResponse with rendered html

    """

    # TODO JHILL: get language code from cookie
    language_code = 'de_DE'

    f = open("./data/{}/prep_cases.json".format(language_code))
    prep_cases = f.read()

    return _render_app_session_view(
        request,
        'prep_cases_multi',
        'apps/prep_cases_multi.html',
        dict(
            prep_cases=prep_cases
        )
    )


def adjective_translation_multi(request: HttpRequest) -> HttpResponse:
    """
    Render the adjective_translation_multi app.

    Parameters
    ----------
    request: HttpRequest
        the HttpRequest

    Response
    --------
    HttpResponse
        the HttpResponse with rendered html

    """
    return _render_app_session_view(
        request,
        'adjective_translation_multi',
        'apps/adjective_translation_multi.html'
    )


def phrase_translation_multi(request: HttpRequest) -> HttpResponse:
    """
    Render the phrase_translation_multi app.

    Parameters
    ----------
    request: HttpRequest
        the HttpRequest

    Response
    --------
    HttpResponse
        the HttpResponse with rendered html

    """
    return _render_app_session_view(
        request,
        'phrase_translation_multi',
        'apps/phrase_translation_multi.html'
    )


def signup(request: HttpRequest) -> HttpResponse:
    """
    Render the signup page or process a signup.

    Parameters
    ----------
    request: HttpRequest
        the HttpRequest

    Response
    --------
    HttpResponse
        the HttpResponse with rendered html

    """
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
def stats(request: HttpRequest) -> HttpResponse:
    """
    Render the stats page.

    Parameters
    ----------
    request: HttpRequest
        the HttpRequest

    Response
    --------
    HttpResponse
        the HttpResponse with rendered html

    """

    grammar_query_stub = GrammarQueryStub(user=request.user)
    weak_nouns = Noun.weak(grammar_query_stub)

    return render(request, 'apps/misc/stats.html', dict(
        weak_nouns=weak_nouns
    ))


@login_required
def prefs(request: HttpRequest) -> HttpResponse:
    """
    Render the stats page.

    Parameters
    ----------
    request: HttpRequest
        the HttpRequest

    Response
    --------
    HttpResponse
        the HttpResponse with rendered html

    """

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
