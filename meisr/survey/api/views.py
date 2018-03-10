from rest_framework import generics
from django.shortcuts import get_object_or_404
from survey.models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer

class QuestionList(generics.ListAPIView):
	queryset = Question.objects.all()
	serializer_class = QuestionSerializer

#answer list


class MultipleFieldLookupMixin(object):
	def get_object(self):
		queryset = self.get_queryset()
		queryset = self.filter_queryset(queryset)
		filter = {}
		for field in self.lookup_fields:
			filter[field] = self.kwargs[field]
		return get_object_or_404(queryset, **filter)

class AnswerUpdate(MultipleFieldLookupMixin, generics.RetrieveUpdateAPIView):
	lookup_fields = ('question', 'user')
	queryset = Answer.objects.all()
	serializer_class = AnswerSerializer

class AnswerCreate(MultipleFieldLookupMixin, generics.CreateAPIView):
	queryset = Answer.objects.all()
	serializer_class = AnswerSerializer

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)