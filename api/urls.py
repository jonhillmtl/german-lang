from django.conf.urls import url

from . import views
from .views import noun_gender, noun_translation_multi, noun_pluralization, \
                   noun_translation, verb_translation_multi, verb_pp_multi, \
                   adjective_translation_multi

urlpatterns = [
    # stats
    url(r'stats/$', views.stats, name='noun_gender_stats'),

    # adjectives

    # GET
    url(r'^adjective/$', views.adjective_random, name='adjective_random'),   

    # POST
    url(
        r'adjectives/translation/multi/check/$',
        adjective_translation_multi.check,
        name='adjective_translation_multi_check'
    ),
    
    # nouns
    
    # GET
    url(r'^nouns/$', views.nouns, name='nouns'),
    url(r'^noun/$', views.noun_random, name='noun_random'),   
    url(r'^nouns/(?P<pk>\d+)/$', views.noun_view, name='noun_view'),   

    # noun_gender mode

    # POST
    url(r'nouns/gender/check/$', noun_gender.check, name='noun_gender_check'),   
    url(r'nouns/gender/correction/$', noun_gender.correction, name='noun_gender_correction'),
    
    # noun_translation_multi mode

    # POST
    url(
        r'nouns/translation/multi/check/$',
        noun_translation_multi.check,
        name='noun_translation_multi_check'
    ),

    url(
        r'nouns/translation/multi/correction/$',
        noun_translation_multi.correction,
        name='noun_translation_multi_correction'
    ),

    # noun_pluralization mode

    # POST
    url(
        r'nouns/pluralization/check/$',
        noun_pluralization.check,
        name='noun_pluralization_check'
    ),
    
    # noun_translation mode

    # POST
    url(
        r'nouns/translation/check/$',
        noun_translation.check,
        name='noun_translation_check'
    ),

    # verbs

    # GET
    url(r'^verbs/$', views.verb_random, name='verb_random'),

    # POST

    # verb_translation_multi
    url(
        r'verbs/translation/multi/check/$',
        verb_translation_multi.check,
        name='verb_translation_multi_check'
    ),

    # verb_pp_multi
    url(
        r'verbs/pp/multi/check/$',
        verb_pp_multi.check,
        name='verb_pp_multi_check'
    )
]
