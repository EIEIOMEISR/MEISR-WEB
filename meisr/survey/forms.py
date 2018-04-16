from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class SurveyForm(forms.Form):
	def __init__(self, *args, **kwargs):
		answers = kwargs.pop('answers')
		super(SurveyForm, self).__init__(*args, **kwargs)

		print('remaking form')
		prev = None
		for i,q in enumerate(Question.objects.all()):
			# add a header before question if new routine
			header = ''
			if not prev or q.routine != prev.routine:
				header = q.routine
			self.fields['custom_%s' % i] = forms.ChoiceField(
				required=False,
				label=q.question_text,
				widget=forms.RadioSelect(attrs={'question':q, 'header':header, 'class':'inline', 'qid':q.id}),
				choices=Answer.CHOICES
				)
			if q.id in answers:
				self.initial['custom_%s' % i] = answers[q.id]
			prev = q

	def answers(self):
		for name, value in self.cleaned_data.items():
			if name.startswith('custom_') and value:
				yield (self.fields[name].widget.attrs['question'], int(value))

class DateInput(forms.DateInput):
	input_type = 'date'

class SignupForm(forms.Form):
	birth_date = forms.DateField(required=True, label="Your child's date of birth", widget=DateInput())

	def signup(self, request, user):
		user.profile.birth_date = self.cleaned_data['birth_date']
		user.save()

class ContactForm(forms.Form):
	from_email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Your e-mail address'}))
	subject = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Subject'}))
	message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter your message'}), required=True)