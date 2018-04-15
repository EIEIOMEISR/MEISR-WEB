from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('survey.urls'), name='survey'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^', include('allauth.account.urls')),
    url(r'^api/', include('survey.api.urls'), name='api'),
    url(r'^admin/', admin.site.urls),
]
