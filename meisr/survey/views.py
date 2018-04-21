from datetime import datetime
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail, BadHeaderError
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render_to_response, render
from django.template.loader import render_to_string
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from .models import *
from .charts import *
from .helpers import score_survey


from pygal.style import CleanStyle

def index(request):
	is_new_user = not Answer.objects.filter(user=request.user.id).exists()
	return render(request, "survey/index.html", context={'is_new_user': is_new_user})

@login_required
def survey(request):
	answers = {x.question.id: x.rating for x in Answer.objects.filter(user=request.user.id)}
	form = SurveyForm(request.POST or None, answers=answers)
	
	submitting = 'flag' in request.POST and request.POST['flag'] == 'true'
	print('submitting', submitting)

	if form.is_valid():
		if submitting:
			lsd = Profile.objects.get(id=request.user.id).last_submit_date
			if lsd:
				cur = datetime.now()
				diff = (cur.year - lsd.year) * 12 + cur.month - lsd.month
			if lsd and diff < 6:
				submitting = False

		for (question, rating) in form.answers():
			# update
			if question.id in answers and rating != answers[question.id]:
				a = Answer.objects.get(user=request.user, question=question)
				a.rating = rating
				a.save()
			# add
			elif question.id not in answers:
				a = Answer(user=request.user, question=question, rating=rating)
				a.save()
			if submitting:
				sc = Profile.objects.get(id=request.user.id).submit_count
				ar = Archive(user=request.user, question=question, rating=rating, submit_count=sc)
				ar.save()
		if submitting:
			score_survey(request.user)    
			p = Profile.objects.get(id=request.user.id)
			p.last_submit_date = datetime.now()
			p.submit_count += 1
			p.save()

	return render(request, "survey/survey.html", {'form': form})

@login_required
def view_results(request):
        charts = {}
        
        age = "age"
        full = "full"

        for routine in Routine.objects.all():
            charts[routine.description] = {'age':ScoreBarChart(
                    routine,
                    age,
                    range = (0,1),
                    style=CleanStyle
                ).generate(request.user),
                'full':ScoreBarChart(
                    routine, 
                    full,
                    range = (0,1),
                    style=CleanStyle
                ).generate(request.user) 
            }

        return render(request, 'scores/index.html', {'charts':charts})

def emailView(request):
	if request.method == 'GET':
		form = ContactForm()
	else:
		form = ContactForm(request.POST)
		if form.is_valid():
			subject = form.cleaned_data['subject']
			from_email = form.cleaned_data['from_email']
			message = form.cleaned_data['message']
			try:
				send_mail(subject, message, from_email, ['admin@example.com'])
			except BadHeaderError:
				return HttpResponse('Invalid header found.')
			return redirect('/success')
	return render(request, "survey/email.html", {'form': form})

def successView(request):
	return render(request, "survey/success.html")
	
'''
@staff_member_required
def raw_data(request):
	pass
'''
