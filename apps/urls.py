from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^nouns/gender/$', views.noun_gender, name='noun_gender'),
    url(r'^nouns/translation/multi/$', views.noun_translation_multi, name='noun_translation_multi'),   
    url(r'^nouns/pluralization/$', views.noun_pluralization, name='noun_pluralization'),   

]
