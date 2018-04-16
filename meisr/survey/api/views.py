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

class ScoreList(generics.CreateAPIView):
        serializer_class = ScoreSerializer
        permissions_classes = (IsAuthenticated,)

        def get_queryset(self):
            return Score.objects.filter(user=self.request.user)

        def perform_create(self, serializer):
            serializer.save(user=self.request.user)

@api_view(['GET'])
def score_survey(request):
    answers = Answer.objects.filter(user=request.user.id)
    routines = Routine.objects.all()

    scores = []

    for i in range(1,routines.count()+1):
        total_answers = answers.filter(question__routine__number=i)
        total_questions = Question.objects.filter(routine__number=i)
        if total_answers.count() != 0 and total_questions.count() != 0:
            scores.append([total_answers.filter(rating=3).count()/total_answers.count(),
                           total_answers.filter(rating=3).count()/total_questions.count(),i])

    for x in scores:
        routine = Routine.objects.get(number=x[2]) 
        age = x[0]
        full = x[1]
        new_score = Score(user=request.user, routine=routine, score_full=full, score_age=age)
        new_score.save()

    return Response(None)

