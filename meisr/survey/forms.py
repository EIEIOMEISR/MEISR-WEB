from django import forms


from .models import Question, Answer, Routine

class SurveyForm(forms.Form):
	def __init__(self, *args, **kwargs):
		answers = kwargs.pop('answers')
		
		super(SurveyForm, self).__init__(*args, **kwargs)

		total_routines = Routine.objects.all().order_by("-number")[0].number

		prev = None
		for i,q in enumerate(Question.objects.all()):
			header = ''
			if not prev or q.routine != prev.routine:
				header = "{}/{} {}".format(q.routine.number , total_routines, q.routine)
			self.fields['custom_%s' % i] = forms.ChoiceField(
				required=False,
				label=q.question_text,
				widget=forms.RadioSelect(attrs={'question':q, 'header':header, 'class':'inline'}),
				choices=Answer.CHOICES
				)
			if q.id in answers:
				self.initial['custom_%s' % i] = answers[q.id]
			else:
				pass
				#not defaulting to 1 anymore should be NULL
				#self.initial['custom_%s' % i] = 1
			prev = q

	def answers(self):
		for name, value in self.cleaned_data.items():
			if name.startswith('custom_'):
				yield (self.fields[name].widget.attrs['question'], int(value))