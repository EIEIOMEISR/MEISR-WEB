from django import forms

from .models import Question, Answer, Routine

class SurveyForm(forms.Form):
	def __init__(self, *args, **kwargs):
		answers = kwargs.pop('answers')
		
		super(SurveyForm, self).__init__(*args, **kwargs)

		#for q in Routine.objects.all().order_by('choice', 'question__starting_age'):
			#print(q.get_choice_display())		
			#print(q.choice, q.question_id, q.question.question_text, q.question.starting_age)
		prev = None
		for i, q in enumerate(Routine.objects.all().order_by('choice', 'question__starting_age')):
			header = ''
			if not prev or q.get_choice_display() != prev.get_choice_display():
				header = q.get_choice_display()
			self.fields['custom_%s' % i] = forms.ChoiceField(required=False,
				label=q.question.question_text,
				widget=forms.RadioSelect(attrs={'qid':q.question_id, 'header':header, 'routine':q.choice}),
				choices=Answer.CHOICES
				)
			if q.question_id in answers:
				self.initial['custom_%s' % i] = answers[q.question_id]
			else:
				self.initial['custom_%s' % i] = 1
			prev = q

	def answers(self):
		for name, value in self.cleaned_data.items():
			if name.startswith('custom_'):
				yield (self.fields[name].widget.attrs['qid'], int(value))