import csv

from datetime import datetime
from django.contrib.admin.views.decorators import staff_member_required
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
from pygal.style import CleanStyle

from .forms import *
from .models import *
from .charts import *
from .helpers import score_survey

'''
Home page
'''


def index(request):
    is_new_user = not Answer.objects.filter(user=request.user.id).exists()
    return render(request, "survey/index.html", context={'is_new_user': is_new_user})


'''
Survey page
'''


@login_required
def survey(request):
    answers = {x.question.id: x.rating for x in Answer.objects.filter(
        user=request.user.id)}

    form = SurveyForm(request.POST or None, answers=answers)

    submitting = 'flag' in request.POST and request.POST['flag'] == 'true'

    if form.is_valid():
        archive = False
        if submitting:
            lsd = Profile.objects.get(user=request.user).last_submit_date
            if lsd:
                cur = datetime.now()
                diff = (cur.year - lsd.year) * 12 + cur.month - lsd.month
                # it has been 6 months since last submit
                if diff >= 6:
                    archive = True
            # first time submitting
            if not lsd:
                archive = True

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
            if archive:
                sc = Profile.objects.get(user=request.user).submit_count
                ar = Archive(user=request.user, question=question,
                             rating=rating, submit_count=sc, date=datetime.now())
                ar.save()

        if archive:
            p = Profile.objects.get(user=request.user)
            p.last_submit_date = datetime.now()
            p.submit_count += 1
            p.save()

        if submitting:
            score_survey(request.user)

    routines = [x.description for x in Routine.objects.all()]
    return render(request, "survey/survey.html", {'form': form, 'routines': routines})


'''
Viewing scores for each routine
'''


@login_required
def view_results(request):
    charts = {}

    age = "age"
    full = "full"

    for routine in Routine.objects.all().order_by('number'):
        charts[routine.description] = {'age': ScoreBarChart(
            routine,
            age,
            range=(0, 1),
            style=CleanStyle
        ).generate(request.user),
            'full': ScoreBarChart(
                routine,
                full,
                range=(0, 1),
                style=CleanStyle
        ).generate(request.user)
        }
    routines = [x.description for x in Routine.objects.all()]
    return render(request, 'survey/score.html', {'charts': charts, 'routines': routines})


'''
Contact page
'''


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
                send_mail(subject, message, from_email, ['eieio@ua.edu'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('/success')
    return render(request, "survey/email.html", {'form': form})


def successView(request):
    return render(request, "survey/success.html")


'''
Download page for user data
'''


@staff_member_required
def data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="raw_data_{}.csv"'.format(
        datetime.now())

    writer = csv.writer(response)

    questions = Question.objects.order_by('routine__number', 'starting_age')
    question_set = set(questions)

    # generate column headers
    columns = ['Legajo', 'ID', 'Date of Birth']
    for x in range(1, 4):
        columns.append('T{}Date'.format(x))
        for i, y in enumerate(questions):
            columns.append('T{}{}{}'.format(x, y.routine.code, i + 1))
    writer.writerow(columns)

    answers = Archive.objects.order_by(
        'user', 'submit_count', 'question__routine__number', 'question__starting_age')
    users = {}
    ls = []

    # go through all answers build a row for each user
    for x in answers:
        if x.user not in users:
            users[x.user] = {'dates': set()}

            if len(users) > 1:
                writer.writerow(ls)
            ls[:] = []

            bday = Profile.objects.get(user=x.user).birth_date
            ls += ['', 'Child{}'.format(x.user.id), bday]
        if x.date not in users[x.user]['dates']:
            users[x.user]['dates'].add(x.date)
            ls.append(x.date.strftime('%d-%m-%Y'))

        ls.append(x.rating)
    writer.writerow(ls)

    return response
