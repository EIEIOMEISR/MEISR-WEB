from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import api_view
from rest_framework.response import Response

from survey.models import Question, Answer

from .serializers import *

class QuestionList(generics.ListAPIView):
	queryset = Question.objects.all()
	serializer_class = QuestionSerializer
	authentication_classes = ()

class AnswerList(generics.ListCreateAPIView):
	serializer_class = AnswerSerializer
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		return Answer.objects.filter(user=self.request.user)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

class AnswerDetail(generics.RetrieveUpdateAPIView):
	lookup_field = ('question')
	serializer_class = AnswerSerializer
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		return Answer.objects.filter(user=self.request.user)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

class ScoreList(generics.ListCreateAPIView):
	serializer_class = ScoreSerializer
	permissions_classes = (IsAuthenticated,)

	def get_queryset(self):
		return Score.objects.filter(user=self.request.user)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)