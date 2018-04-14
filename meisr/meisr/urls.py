from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from survey.views import account_activation_sent, activate

urlpatterns = [
    url(r'^', include('survey.urls'), name='survey'),
    url(r'^api/', include('survey.api.urls'), name='api'),

    url(r'^', include('django.contrib.auth.urls')),
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, name='logout'),
    url(r'^account_activation_sent/$', account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate'),

    url(r'^admin/', admin.site.urls),
]
