from django import forms
from django.forms import ModelForm

from .models import Question, Answer

class NameForm(forms.Form):
	your_name = forms.CharField(label='Your name', max_length=100)

class SurveyForm(forms.Form):
	CHOICES = [('select1', 'select 1'), ('select2', 'select 2')]
	ratings = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

class AnswerForm(forms.ModelForm):
	class Meta:
		model = Answer
		exclude = ("user", "question",)
Answer.form = AnswerForm