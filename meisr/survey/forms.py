from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

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

class SignUpForm(UserCreationForm):
    email = email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class': 'validate form-control',}))
    birth_date = forms.DateField(label="Your child's date of birth", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'MM/DD/YYYY'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'birth_date', 'password1', 'password2', )

    def __init__(self, *args, **kwargs):
	    super(SignUpForm, self).__init__(*args, **kwargs)

	    self.fields['username'].widget.attrs['class'] = 'form-control'
	    self.fields['password1'].widget.attrs['class'] = 'form-control'
	    self.fields['password2'].widget.attrs['class'] = 'form-control'