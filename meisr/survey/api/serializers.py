from rest_framework import serializers
from rest_auth.serializers import UserDetailsSerializer
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
		fields = ('id', 'user', 'routine', 'score_age', 'score_full', 'timestamp',)
		read_only_fields = ['user']

class UserSerializer(UserDetailsSerializer):
    birth_date = serializers.CharField(source="profile.birth_date")

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('birth_date',)

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('userprofile', {})
        birth_date = profile_data.get('birth_date')

        instance = super(UserSerializer, self).update(instance, validated_data)

        # get and update user profile
        profile = instance.userprofile
        if profile_data and birth_date:
            profile.birth_date = birth_date
            profile.save()
        return instance
