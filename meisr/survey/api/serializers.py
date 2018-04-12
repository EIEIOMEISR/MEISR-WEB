from rest_framework import serializers
from rest_auth.serializers import UserDetailsSerializer
from survey.models import *

from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

class RoutineSerializer(serializers.ModelSerializer):
	class Meta:
		model = Routine
		fields = ('id', 'description', 'number')

class QuestionSerializer(serializers.ModelSerializer):
	routine = RoutineSerializer(read_only=True)
	func = serializers.SerializerMethodField()
	dev = serializers.SerializerMethodField()
	out = serializers.SerializerMethodField()

	class Meta:
		model = Question
		fields = ('id','question_text', 'starting_age', 'routine', 'func', 'dev', 'out',)

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

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    username = serializers.CharField(required=True)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)
    birth_date = serializers.DateField(required=True)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                _("The two password fields didn't match."))
        return data

    def get_cleaned_data(self):
        return {
            'birth_date': self.validated_data.get('birth_date', ''),
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.profile.save()
        return user