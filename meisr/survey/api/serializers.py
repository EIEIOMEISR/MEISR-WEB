from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import UserDetailsSerializer
from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from survey.models import *


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
        fields = ('id', 'question_text', 'starting_age',
                  'routine', 'func', 'dev', 'out',)

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


class ScoreSerializer(serializers.ModelSerializer):
    routine = RoutineSerializer(read_only=True)

    class Meta:
        model = Score
        fields = ('id', 'user', 'routine', 'score_age',
                  'score_full', 'timestamp',)
        read_only_fields = ['user']


class UserSerializer(UserDetailsSerializer):
    birth_date = serializers.CharField(source="profile.birth_date")

    class Meta(UserDetailsSerializer.Meta):
        fields = ('username', 'email', 'birth_date',)

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


class CustomRegisterSerializer(RegisterSerializer):
    birth_date = serializers.DateField(required=True, write_only=True)

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
        user.profile.birth_date = self.cleaned_data['birth_date']
        user.save()
        return user
