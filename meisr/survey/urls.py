from django.conf.urls import url
from . import views

app_name = 'survey'
urlpatterns = [
	url(r'^$', views.index, name='home'),
    url(r'^survey/$', views.survey, name='survey'),
    url(r'^score_survey/$', views.score_survey, name='score_survey'),
    url(r'^view_results/$', views.view_results, name='view_results'),
]
