from django.conf.urls import url, include
from . import views

from allauth.account.views import confirm_email as allauthemailconfirmation

urlpatterns = [
    url(r'^rest-auth/registration/account-confirm-email/(?P<key>[\s\d\w().+-_\',:&]+)/$', allauthemailconfirmation, name="account_confirm_email"),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/', include('allauth.account.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),

	url(r'^questions/$', views.QuestionList.as_view(), name='question-list'),
	url(r'^answers/(?P<question>\d+)/$', views.AnswerDetail.as_view(), name='answer-detail'),
	url(r'^answers/$', views.AnswerList.as_view(), name='answer-list'),
	url(r'^scores/', views.ScoreList.as_view(), name='score-list'),
]