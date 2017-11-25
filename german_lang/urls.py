from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/nouns/', include('api.urls')),
    url(r'^apps/', include('apps.urls'))
]
