from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^stats/$', views.stats, name='stats'),
    url(r'^prefs/$', views.prefs, name='prefs'),

    url(r'^nouns/gender/$', views.noun_gender, name='noun_gender'),
    url(r'^nouns/translation/multi/$', views.noun_translation_multi, name='noun_translation_multi'),
    url(r'^nouns/pluralization/$', views.noun_pluralization, name='noun_pluralization'),
    url(r'^nouns/translation/$', views.noun_translation, name='noun_translation'),
    url(r'^nouns/article/missing/$', views.noun_article_missing, name='noun_article_missing'),

    url(r'^verbs/translation/multi/$', views.verb_translation_multi, name='verb_translation_multi'),
    url(r'^verbs/pastparticiple/multi/$', views.verb_pp_multi, name='verb_pp_multi'),

    url(r'^pronouns/missing/$', views.pronouns_missing, name='pronouns_missing'),
    url(r'^pronouns/possesive/missing/$', views.pos_pronouns_missing, name='pos_pronouns_missing'),
]
