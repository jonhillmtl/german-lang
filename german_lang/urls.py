from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^', include('landing.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('api.urls')),
    url(r'^apps/', include('apps.urls'))
]
