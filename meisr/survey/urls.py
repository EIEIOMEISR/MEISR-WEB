from django.conf.urls import url
from . import views

app_name = 'survey'
urlpatterns = [
	url(r'^$', views.index, name='home'),
    url(r'^survey/$', views.survey, name='survey'),
    url(r'^view_results/$', views.view_results, name='view_results'),
    url(r'^email/$', views.emailView, name='email'),
    url(r'^success$', views.successView, name='success'),
    url(r'^data/$', views.data, name='success'),
]
