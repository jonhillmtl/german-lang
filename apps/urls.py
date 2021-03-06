from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),

    url(r'^signup/$', views.signup, name='signup'),

    url(r'^stats/$', views.stats, name='stats'),
    url(r'^prefs/$', views.prefs, name='prefs'),

    url(r'^nouns/list/$', views.noun_list, name='noun_list'),
    url(r'^nouns/random/$', views.noun_random_feed, name='noun_random_feed'),

    url(r'^nouns/flash/$', views.noun_flash, name='noun_flash'),
    url(r'^nouns/gender/$', views.noun_gender, name='noun_gender'),
    url(r'^nouns/translation/multi/$', views.noun_translation_multi, name='noun_translation_multi'),
    url(r'^nouns/pluralization/$', views.noun_pluralization, name='noun_pluralization'),
    url(r'^nouns/translation/$', views.noun_translation, name='noun_translation'),
    url(r'^nouns/article/missing/$', views.noun_article_missing, name='noun_article_missing'),

    url(r'^verbs/translation/multi/$', views.verb_translation_multi, name='verb_translation_multi'),
    url(r'^verbs/pastparticiple/multi/$', views.verb_pp_multi, name='verb_pp_multi'),

    url(r'^pronouns/missing/$', views.pronouns_missing, name='pronouns_missing'),
    url(r'^pronouns/possesive/missing/$', views.pos_pronouns_missing, name='pos_pronouns_missing'),

    url(r'^adjective/translation/multi/$', views.adjective_translation_multi, name='adjective_translation_multi'),

    url(r'^phrase/translation/multi/$', views.phrase_translation_multi, name='phrase_translation_multi'),

    url(r'^prep/cases/multi/$', views.prep_cases_multi, name='prep_cases_multi')
]
