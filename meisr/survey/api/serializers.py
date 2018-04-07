from rest_framework import serializers
from survey.models import *

class QuestionSerializer(serializers.ModelSerializer):
	routine = serializers.SerializerMethodField()
	func = serializers.SerializerMethodField()
	dev = serializers.SerializerMethodField()
	out = serializers.SerializerMethodField()

	class Meta:
		model = Question
		fields = ('id','question_text', 'starting_age', 'routine', 'func', 'dev', 'out',)

	def get_routine(self, obj):
		return obj.routine.description

	def get_func(self, obj):
		return(FunctionalDomain.objects.filter(question=obj.id).values_list('choice', flat=True))
	
	def get_dev(self, obj):
		return(DevelopmentalDomain.objects.filter(question=obj.id).values_list('choice', flat=True))
	
	def get_out(self, obj):
		return(Outcome.objects.filter(question=obj.id).values_list('choice', flat=True))

class AnswerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Answer
		fields = ('id', 'user', 'question', 'rating',)
		read_only_fields = ['user']

	#TODO: validate()

class ScoreSerializer(serializers.ModelSerializer):
	class Meta:
		model = Score
		fields = ('id', 'user', 'raw', 'dev', 'func', 'out', 'timestamp',)
		read_only_fields = ['user']

