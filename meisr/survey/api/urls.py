from django.conf.urls import url
from .views import QuestionList, AnswerUpdate, AnswerCreate

urlpatterns = [
	url(r'^questions/', QuestionList.as_view(), name='question-list'),
	url(r'^update/(?P<question>\d)/(?P<user>\d)/$', AnswerUpdate.as_view(), name='answer-update'),
	url(r'^create/$', AnswerCreate.as_view(), name='answer-create')
]