import requests

from django import forms

from .models import Question, Answer

class SurveyForm(forms.Form):
	CHOICES = ((1,'a'),(2,'b'),(3,'c'))

	def __init__(self, *args, **kwargs):
		questions = kwargs.pop('questions')
		super(SurveyForm, self).__init__(*args, **kwargs)

		result = requests.post('http://127.0.0.1:8000/rest-auth/login/', data={'username':'bds','password':'one12345'})
		result = requests.get('http://127.0.0.1:8000/api/answers/', headers={'Authorization': 'JWT '+result.json()['token']})
		answers = {}
		for x in result.json():
			answers[x['question']] = x['rating']

		for i, q in enumerate(questions):
			self.fields['custom_%s' % i] = forms.ChoiceField(required=False,
				label=q[1],
				widget=forms.RadioSelect(attrs={'qid':q[0]}),
				choices=self.CHOICES
				)
			if q[0] in answers:
				self.initial['custom_%s' % i] = answers[q[0]]
			else:
				self.initial['custom_%s' % i] = 1

	def answers(self):
		for name, value in self.cleaned_data.items():
			if name.startswith('custom_'):
				yield (self.fields[name].widget.attrs['qid'], int(value))