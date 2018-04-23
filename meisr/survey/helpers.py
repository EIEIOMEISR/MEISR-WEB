from .models import *
import csv

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

def add_record(rec):
    try:
        rec.save()
    except:
        pass

def add_tsv_to_db():
    Routine(description='Waking Up', number=1, code='W').save()
    Routine(description='Meal Time', number=2, code='MT').save()
    Routine(description='Getting Dressed', number=3, code='D').save()
    Routine(description='Toileting/Diaper', number=4, code='TD').save()
    Routine(description='Going Out', number=5, code='GO').save()
    Routine(description='Playtime With Others', number=6, code='PTWO').save()
    Routine(description='Play Time by Him or Herself', number=7, code='PTA').save()
    Routine(description='Nap Time', number=8, code='N').save()
    Routine(description='Bath Time', number=9, code='B').save()
    Routine(description='Hanging Out Time (including TV & Books)', number=10, code='HO').save()
    Routine(description='Grocery Shopping', number=11, code='GS').save()
    Routine(description='Outside Time', number=12, code='O').save()
    Routine(description='Bedtime', number=13, code='BT').save()
    Routine(description='Transition Time', number=14, code='TR').save()

    with open('../meisr.tsv') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            routine = Routine.objects.get(number=int(float(row[0])))
            new_record = Question(question_text=row[1], starting_age=int(row[2]), routine=routine)
            add_record(new_record)

    with open('../meisr.tsv') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            q = Question.objects.get(question_text=row[1])
            for x in row[7].split(', '):
                new_record = FunctionalDomain(question=q, choice=x)
                add_record(new_record)
            for x in row[7].split(', '):
                new_record = DevelopmentalDomain(question=q, choice=x)
                add_record(new_record)
            for x in row[7].split(', '):
                new_record = Outcome(question=q, choice=x)
                add_record(new_record)