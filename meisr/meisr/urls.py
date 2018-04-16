from django.conf.urls import include, url
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^', include('survey.urls'), name='survey'),
    url(r'^(accounts/)?', include('allauth.account.urls')),
    url(r'^api/', include('survey.api.urls'), name='api'),
    url(r'^admin/', admin.site.urls),
    url(r'^api-token-auth/', obtain_jwt_token),
]
