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
            scores.append([total_answers.filter(rating=3).count()/total_answers.count(), total_answers.filter(rating=3).count()/total_questions.count(),i])

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
    add_record(Routine(description='Waking Up', number=1, code='W'))
    add_record(Routine(description='Meal Time', number=2, code='MT'))
    add_record(Routine(description='Getting Dressed', number=3, code='D'))
    add_record(Routine(description='Toileting/Diaper', number=4, code='TD'))
    add_record(Routine(description='Going Out', number=5, code='GO'))
    add_record(Routine(description='Playtime With Others', number=6, code='PTWO'))
    add_record(Routine(description='Play Time by Him or Herself', number=7, code='PTA'))
    add_record(Routine(description='Nap Time', number=8, code='N'))
    add_record(Routine(description='Bath Time', number=9, code='B'))
    add_record(Routine(description='Hanging Out Time (including TV & Books)', number=10, code='HO'))
    add_record(Routine(description='Grocery Shopping', number=11, code='GS'))
    add_record(Routine(description='Outside Time', number=12, code='O'))
    add_record(Routine(description='Bedtime', number=13, code='BT'))
    add_record(Routine(description='Transition Time', number=14, code='TR'))

    with open('meisr.tsv') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            routine = Routine.objects.get(number=int(float(row[0])))
            new_record = Question(question_text=row[1], starting_age=int(row[2]), routine=routine)
            add_record(new_record)

    with open('meisr.tsv') as tsvfile:
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

from allauth.account.models import EmailAddress
from django.contrib.auth.models import User
import random, string, uuid
from datetime import datetime, timedelta, timezone

def prefill():
	username = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(30))
	email = username+'@gmail.com'

	user, created = User.objects.get_or_create(username=username, email=email)
	user.set_password('password123')
	user.save()
	prof = Profile.objects.get(user=user)
	prof.birth_date = datetime.now()
	prof.save()

	EmailAddress(user=user, email=email, verified=True, primary=True).save()

	questions = Question.objects.all()

	for i in range(3):
		date = datetime.now(timezone.utc) - timedelta(days=31*(3-i))
		answers = Answer.objects.filter(user=user).values_list('question', flat=True)
		for q in questions:
			answer = None
			rating = None
			if q.id in answers:
				answer = Answer.objects.get(user=user, question=q)
				if answer.rating < 3:
					answer.rating += 1
					answer.save()
				rating = answer.rating
			else:
				rating = random.randint(1,3)
				answer = Answer(user=user, question=q, rating=rating)
				answer.save()
			sc = Profile.objects.get(user=user).submit_count
			ar = Archive(user=user, question=q, rating=rating, date=date, submit_count=sc)
			ar.save()
		prof.last_submit_date = date
		prof.submit_count += 1
		prof.save()
		score_survey(user)
		for s in Score.objects.filter(user=user):
			diff = datetime.now(timezone.utc) - s.timestamp
			if not diff.days:
				s.timestamp = date
				s.save()
