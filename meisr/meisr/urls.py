from django.conf.urls import include, url
from django.contrib import admin
from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token
from django.contrib.auth import views as auth_views
from survey.views import account_activation_sent, activate

urlpatterns = [
    url(r'^', include('survey.urls'), name='survey'),
    url(r'^api/', include('survey.api.urls'), name='api-survey'),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/register/', include('rest_auth.registration.urls')),
    url(r'^refresh-token/', refresh_jwt_token),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^account_activation_sent/$', account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate'),
]
