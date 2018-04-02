from django.shortcuts import redirect, render_to_response, render

from django.views.decorators.csrf import csrf_exempt

from .forms import SurveyForm

from .models import Answer

def survey(request):
    answers = {x.question.id: x.rating for x in Answer.objects.filter(user=request.user.id)}

    form = SurveyForm(request.POST or None, answers=answers)
    
    if form.is_valid():
        for (question, answer) in form.answers():
            if question in answers:
                if answer != answers[question]:
                    print('UPDATING answer to question {}'.format(question))
            else:
                print('ADDING answer to question {}'.format(question))
                Answer(user=request.user, question=question)
            pass
        pass

    return render(request, "survey/survey.html", {'form': form})