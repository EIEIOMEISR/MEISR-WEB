from django.shortcuts import redirect, render_to_response, render

from django.views.decorators.csrf import csrf_exempt

from .forms import SurveyForm

from .models import Answer

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