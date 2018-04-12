from django.shortcuts import redirect, render_to_response, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from .models import *

def index(request):
    is_new_user = not Answer.objects.filter(user=request.user.id).exists()
    return render(request, "survey/index.html", context={'is_new_user': is_new_user})

def survey(request):
    answers = {x.question.id: x.rating for x in Answer.objects.filter(user=request.user.id)}

    form = SurveyForm(request.POST or None, answers=answers)
    
    if form.is_valid():
        for (question, rating) in form.answers():
            if question.id in answers:
                if rating != answers[question.id]:
                    print('UPDATING answer to question {}'.format(question.id))
                    a = Answer.objects.get(user=request.user, question=question)
                    a.rating = rating
                    a.save()
            else:
                print('ADDING answer to question {}'.format(question.id))
                a = Answer(user=request.user, question=question, rating=rating)
                a.save()
            pass
        pass

    return render(request, "survey/survey.html", {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})