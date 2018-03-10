from rest_framework import serializers
from survey.models import Question
from survey.models import Answer

class QuestionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Question
		fields = ('id','question_text', 'starting_age', 'section')

class AnswerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Answer
		fields = ('id', 'question', 'user', 'rating')
		read_only_fields = ['user']