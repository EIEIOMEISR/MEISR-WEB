from django.conf.urls import url, include
from .views import *

urlpatterns = [
	url(r'^questions/', QuestionList.as_view(), name='question-list'),
	url(r'^answers/(?P<question>\d+)/', AnswerDetail.as_view(), name='answer-detail'),
	url(r'^answers/', AnswerList.as_view(), name='answer-list'),
	url(r'^scores/', ScoreList.as_view(), name='score-list'),
]