from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    CHOICES = (
        (1, 'Waking Up'),
        (2, 'Meals'),
        (3, 'Dressing'),
        (4, 'Toileting/Diaper Change'),
        (5, 'Outings (except grocery shopping'),
        (6, 'Play Time With Others'),
        (7, 'Play Time Alone'),
        (8, 'Nap'),
        (9, 'Bath'),
        (10, 'Hanging Out/Books/TV'),
        (11, 'Grocery Shopping'),
        (12, 'Outdoors'),
        (13, 'Bedtime'),
    )
    question_text = models.CharField(max_length=200)
    starting_age = models.IntegerField(default=0)
    section = models.IntegerField(choices=CHOICES)

    def __str__(self):
        return str(self.id) + ' ' + str(self.question_text)

class Child(models.Model):
    user = models.OneToOneField(User)
    age = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)

class Answer(models.Model):
    CHOICES = (
        (1, 'Not yet'),
        (2, 'Sometimes'),
        (3, 'Often/Beyond This'),
    )

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(Child, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1, choices=CHOICES)
    
    class Meta:
        unique_together = (("question", "user"),)

class FunctionalDomain(models.Model):
    CHOICES = (
            ('E', 'E = engagement'),
            ('I', 'I = independence'),
            ('S', 'S = social relationships'),
        )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.CharField(max_length=1, choices=CHOICES)

class DevelopmentalDomain(models.Model):
    CHOICES = (
            ('A', 'A = adaptive'),
            ('CG', 'CG = cognitive'),
            ('CM', 'CM = communication'),
            ('M', 'M = motor'),
            ('S', 'S = social'),
        )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.CharField(max_length=2, choices=CHOICES)

class Outcome(models.Model):
    CHOICES = (
            ('S', 'S = positive social relations'),
            ('K', 'K = acquiring and using knowledge and skills'),
            ('A', 'A = taking action to meet needs'),
        )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.CharField(max_length=1, choices=CHOICES)