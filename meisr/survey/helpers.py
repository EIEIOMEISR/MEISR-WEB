from .models import *

def score_survey(user):
    answers = Answer.objects.filter(user=user)
    routines = Routine.objects.all()

    scores = []

    for i in range(1,routines.count()+1):
        total_answers = answers.filter(question__routine__number=i)
        total_questions = Question.objects.filter(routine__number=i)
        if total_answers.count() != 0 and total_questions.count() != 0:
            scores.append([total_answers.filter(rating=3).count()/total_answers.count(),
                           total_answers.filter(rating=3).count()/total_questions.count(),i])

    for x in scores:
        routine = Routine.objects.get(number=x[2]) 
        age = x[0]
        full = x[1]
        new_score = Score(user=user, routine=routine, score_full=full, score_age=age)
        new_score.save()
