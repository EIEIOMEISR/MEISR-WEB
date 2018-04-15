from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render_to_response, render
from django.template.loader import render_to_string
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt

from .tokens import account_activation_token
from .forms import *
from .models import *
from .charts import *


from pygal.style import CleanStyle

def index(request):
    is_new_user = not Answer.objects.filter(user=request.user.id).exists()
    return render(request, "survey/index.html", context={'is_new_user': is_new_user})

@login_required
def survey(request):
    answers = {x.question.id: x.rating for x in Answer.objects.filter(user=request.user.id)}
    form = SurveyForm(request.POST or None, answers=answers)
    
    if form.is_valid():
        #'submit' in request.POST)
        #Profile.objects.filter(user=request.user.id)[0].birth_date
        for (question, rating) in form.answers():
            # update an answer
            if question.id in answers and rating != answers[question.id]:
                a = Answer.objects.get(user=request.user, question=question)
                a.rating = rating
                a.save()
            # add a new answer
            elif question.id not in answers:
                a = Answer(user=request.user, question=question, rating=rating)
                a.save()

    return render(request, "survey/survey.html", {'form': form})

def score_survey(request):
        answers = Answer.objects.filter(user=request.user.id)
        routines = Routine.objects.all()

        scores = []

        for i in range(1,routines.count()+1):
            temp = answers.filter(question__routine__number=i)
            if temp.count() != 0 and temp.exclude(rating__isnull=True) != 0:
                scores.append([temp.filter(rating=3).count()/temp.exclude(rating__isnull=True).count(),temp.filter(rating=3).count()/temp.count(),i])

        for x in scores:
            routine = Routine.objects.get(number=x[2]) 
            full = x[1]
            age = x[0]
            new_score = Score(user=request.user, routine=routine, score_full=full, score_age=age)
            new_score.save()

        return redirect('/view_results')


def view_results(request):
        charts = {}
        
        age_bar_chart = ScoreBarChart(
        height=600,
        width=800,
        explicit_size=True,
        style=CleanStyle
        )

        full_bar_chart = ScoreBarChart(
        height=600,
        width=800,
        explicit_size=True,
        style=CleanStyle
        )

        charts['score_age'] = age_bar_chart.generate(request.user, 0)
        charts['score_full'] = full_bar_chart.generate(request.user, 1)

        return render(request, 'scores/index.html', charts)

'''
@staff_member_required
def raw_data(request):
    pass
'''
