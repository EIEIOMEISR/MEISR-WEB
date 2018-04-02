from django import forms

from .models import Question, Answer, Routine

class SurveyForm(forms.Form):
	def __init__(self, *args, **kwargs):
		answers = kwargs.pop('answers')
		
		super(SurveyForm, self).__init__(*args, **kwargs)

		prev = None
		for i,q in enumerate(Question.objects.all()):
			header = ''
			if not prev or q.routine != prev.routine:
				header = q.routine
			self.fields['custom_%s' % i] = forms.ChoiceField(
				required=False,
				label=q.question_text,
				widget=forms.RadioSelect(attrs={'question':q, 'header':header}),
				choices=Answer.CHOICES
				)
			if q.id in answers:
				self.initial['custom_%s' % i] = answers[q.id]
			else:
				self.initial['custom_%s' % i] = 1
			prev = q

	def answers(self):
		for name, value in self.cleaned_data.items():
			if name.startswith('custom_'):
				yield (self.fields[name].widget.attrs['question'], int(value))