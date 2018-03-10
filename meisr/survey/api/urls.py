from django.conf.urls import url
from .views import QuestionList, AnswerUpdate, AnswerList

urlpatterns = [
	url(r'^questions/', QuestionList.as_view(), name='question-list'),
	url(r'^answers/', AnswerList.as_view(), name='answer-list'),
	url(r'^u/(?P<user>\d)/q/(?P<question>\d)/', AnswerUpdate.as_view(), name='answer-update'),
]