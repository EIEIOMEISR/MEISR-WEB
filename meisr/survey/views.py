import requests

from django.shortcuts import redirect, render_to_response, render

from django.views.decorators.csrf import csrf_exempt

from .forms import SurveyForm

def survey(request):
    result = requests.get('http://127.0.0.1:8000/api/questions/')
    questions = [(x['id'], x['question_text']) for x in result.json()]

    result = requests.post('http://127.0.0.1:8000/rest-auth/login/', data={'username':'bds','password':'one12345'})
    result = requests.get('http://127.0.0.1:8000/api/answers/', headers={'Authorization': 'JWT '+result.json()['token']})
    answers = {}
    for x in result.json():
        answers[x['question']] = x['rating']

    form = SurveyForm(request.POST or None, questions=questions)
    if form.is_valid():
        for (question, answer) in form.answers():
            if question in answers:
                if answer != answers[question]:
                    print('UPDATING answer to question {}'.format(question))
            else:
                print('ADDING answer to question {}'.format(question))
            pass
        pass

    return render(request, "survey/survey.html", {'form': form})