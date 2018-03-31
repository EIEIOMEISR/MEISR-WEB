import csv
from survey.models import *

def add_record(rec):
	try:
		rec.save()
	except:
		pass

with open('../../meisr.tsv') as tsvfile:
	reader = csv.reader(tsvfile, delimiter='\t')
	for row in reader:
		new_record = Question(question_text=row[1], starting_age=int(row[2]))
		add_record(new_record)
		q = Question.objects.filter(question_text=row[1])[0]
		new_record = Routine(question=q, choice=int(float(row[0])))
		add_record(new_record)
		for x in row[7].split(', '):
			new_record = FunctionalDomain(question=q, choice=x)
			add_record(new_record)
		for x in row[7].split(', '):
			new_record = DevelopmentalDomain(question=q, choice=x)
			add_record(new_record)
		for x in row[7].split(', '):
			new_record = Outcome(question=q, choice=x)
			add_record(new_record)