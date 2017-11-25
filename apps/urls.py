from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^nouns/gender/$', views.noun_gender, name='noun_gender'),   
]
