from django.conf.urls import url

from . import views
from .views import noun_gender, noun_translation_multi, noun_pluralization

urlpatterns = [

    # nouns
    
    # GET
    url(r'^nouns/$', views.random_noun, name='random_noun'),   
    url(r'^nouns/(?P<pk>\d+)/$', views.noun_view, name='noun_view'),   


    # noun_gender mode
    # TODO JHILL: are these regexes right at the beginning?
    # GET
    url(r'nouns/gender/stats/$', views.stats, name='noun_gender_stats'),

    # POST
    url(r'nouns/gender/check/$', noun_gender.check, name='noun_gender_check'),   
    url(r'nouns/gender/correction/$', noun_gender.correction, name='noun_gender_correction'),
    
    # noun_translation_multi mode

    # POST
    url(
        r'nouns/translations/multi/check/$',
        noun_translation_multi.check,
        name='noun_translation_multi_check'
    ),

    url(
        r'nouns/translations/multi/correction/$',
        noun_translation_multi.correction,
        name='noun_translation_multi_correction'
    ),

    # noun_pluralization mode

    # POST
    url(
        r'nouns/pluralization/check/$',
        noun_pluralization.check,
        name='noun_pluralization_check'
    )
]
