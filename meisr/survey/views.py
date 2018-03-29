from django.views import generic
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView

from .forms import NameForm, SurveyForm, AnswerForm

from .models import Question


class IndexView(generic.ListView):
    template_name = 'survey/index.html'

    def get_queryset(self):
        return Question.objects.order_by('section')

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'survey/name.html', {'form': form})

class SurveyView(TemplateView):
	template_name = 'survey/name.html'

	def get(self, request):
		form = SurveyForm()
		return render(request, self.template_name, {'form': form})

def index(request):
	questions = Question.objects.all()
	if request.method == 'POST':
		print(request.POST)
		for q in questions:
			try:
				data ={ u'%s-answer'%q.id: request.POST[u'%s-answer'%q.id]}
			except:
				data = { u'%s-answer'%q.id: None}
	else:
		pass
	return render_to_response('survey/survey.html', {'questions': questions,})