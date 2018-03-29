from django.conf.urls import url

from . import views

app_name = 'survey'
urlpatterns = [
    #url(r'^$', views.IndexView.as_view(), name='index'),
    #url(r'^$', views.SurveyView.as_view())
    url(r'^$', views.index)
]