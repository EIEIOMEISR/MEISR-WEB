from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    question_text = models.CharField(max_length=200, unique=True)
    starting_age = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id) + ': ' + str(self.question_text)

    class Meta:
        ordering = ['starting_age', 'question_text']


class Routine(models.Model):
    CHOICES = (
        (1, 'Waking Up'),
        (2, 'Meal Times'),
        (3, 'Getting Dressed'),
        (4, 'Toileting/Diaper'),
        (5, 'Outings (Going Out)'),
        (6, 'Play Time With Others'),
        (7, 'Play Time by Him or Herself'),
        (8, 'Nap Time'),
        (9, 'Bath Time'),
        (10, 'Hanging Out Time (including TV & Books)'),
        (11, 'Grocery Shopping'),
        (12, 'Outside Time'),
        (13, 'Bedtime'),
        (14, 'Transition Time')
    )
    question = models.ForeignKey(Question,related_name='routine', on_delete=models.CASCADE)
    choice = models.IntegerField(choices=CHOICES)

    class Meta:
        unique_together = (("question", "choice"),)

class Child(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)

class Answer(models.Model):
    CHOICES = (
        (1, 'Not yet'),
        (2, 'Sometimes'),
        (3, 'Often'),
        (4, 'Beyond This')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1, choices=CHOICES)
    
    class Meta:
        unique_together = (("question", "routine", "user"),)

class FunctionalDomain(models.Model):
    CHOICES = (
            ('E', 'E = engagement'),
            ('I', 'I = independence'),
            ('S', 'S = social relationships'),
        )
    question = models.ForeignKey(Question,related_name='func', on_delete=models.CASCADE)
    choice = models.CharField(max_length=1, choices=CHOICES)

    class Meta:
        unique_together = (("question", "choice"),)

class DevelopmentalDomain(models.Model):
    CHOICES = (
            ('A', 'A = adaptive'),
            ('CG', 'CG = cognitive'),
            ('CM', 'CM = communication'),
            ('M', 'M = motor'),
            ('S', 'S = social'),
        )
    question = models.ForeignKey(Question,related_name='dev', on_delete=models.CASCADE)
    choice = models.CharField(max_length=2, choices=CHOICES)

    class Meta:
        unique_together = (("question", "choice"),)

class Outcome(models.Model):
    CHOICES = (
            ('S', 'S = positive social relations'),
            ('K', 'K = acquiring and using knowledge and skills'),
            ('A', 'A = taking action to meet needs'),
        )
    question = models.ForeignKey(Question, related_name='out', on_delete=models.CASCADE)
    choice = models.CharField(max_length=1, choices=CHOICES)

    class Meta:
        unique_together = (("question", "choice"),)

class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    raw = models.DecimalField(max_digits=4, decimal_places=2)
    dev = models.DecimalField(max_digits=4, decimal_places=2)
    func = models.DecimalField(max_digits=4, decimal_places=2)
    out = models.DecimalField(max_digits=4, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)