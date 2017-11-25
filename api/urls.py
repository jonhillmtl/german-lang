from django.conf.urls import url

from . import views

urlpatterns = [
    # GET
    url(r'^$', views.random_noun, name='random_noun'),   
    url(r'^(?P<pk>\d+)/$', views.noun_view, name='noun_view'),   
    
    # POST
    url(r'^(?P<pk>\d+)/gender/$', views.noun_gender_check, name='noun_gender_check'),   
    url(r'^(?P<pk>\d+)/gender/correction/$', views.noun_gender_check_correction, name='noun_gender_check_correction'),
    url(r'gender/stats/$', views.noun_gender_stats, name='noun_gender_stats'),
]
