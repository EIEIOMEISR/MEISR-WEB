from rest_framework import serializers
from survey.models import *

class QuestionSerializer(serializers.ModelSerializer):
	section = serializers.SerializerMethodField()
	func = serializers.SerializerMethodField()
	dev = serializers.SerializerMethodField()
	out = serializers.SerializerMethodField()

	class Meta:
		model = Question
		fields = ('id','question_text', 'starting_age', 'section', 'func', 'dev', 'out')
	
	def get_section(self, obj):
		return obj.get_section_display()
	def get_func(self, obj):
		return(FunctionalDomain.objects.filter(question=obj.id).values_list('choice', flat=True))
	def get_dev(self, obj):
		return(DevelopmentalDomain.objects.filter(question=obj.id).values_list('choice', flat=True))
	def get_out(self, obj):
		return(Outcome.objects.filter(question=obj.id).values_list('choice', flat=True))

class AnswerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Answer
		fields = ('id', 'user', 'question', 'rating')

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

	#TODO: add validation