from django.conf.urls import url

from django.views.generic import TemplateView, RedirectView

from . import views

app_name = 'survey'
urlpatterns = [
    url(r'^$', views.survey, name='survey'),
    url(r'^signup/$', views.signup, name='signup'),
]