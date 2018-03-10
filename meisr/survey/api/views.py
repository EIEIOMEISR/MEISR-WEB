from rest_framework import generics, mixins
from django.shortcuts import get_object_or_404
from survey.models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer

'''
python usage example:

import requests

r = requests.get('http://127.0.0.1:8000/api/questions/')
r = requests.post('http://127.0.0.1:8000/api/answers/', auth=('user1','qwerty123'), data={'question':2, 'rating':'3'})
r = requests.get('http://127.0.0.1:8000/api/answers/', auth=('user1','qwerty123'))
r = requests.patch('http://127.0.0.1:8000/api/u/2/q/1/', auth=('user1','qwerty123'), data={'rating':'1'})
'''

class QuestionList(generics.ListAPIView):
	queryset = Question.objects.all()
	serializer_class = QuestionSerializer

class AnswerList(mixins.CreateModelMixin, generics.ListAPIView):
	serializer_class = AnswerSerializer

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

	def get_queryset(self):
		return Answer.objects.filter(user=self.request.user)

class MultipleFieldLookupMixin(object):
	def get_object(self):
		queryset = self.get_queryset()
		queryset = self.filter_queryset(queryset)
		filter = {}
		for field in self.lookup_fields:
			filter[field] = self.kwargs[field]
		return get_object_or_404(queryset, **filter)

class AnswerUpdate(MultipleFieldLookupMixin, generics.RetrieveUpdateAPIView):
	lookup_fields = ('user', 'question')
	queryset = Answer.objects.all()
	serializer_class = AnswerSerializer