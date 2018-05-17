from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Routine(models.Model):
    description = models.CharField(max_length=200, unique=True)
    number = models.PositiveSmallIntegerField(unique=True)
    code = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.description


class Question(models.Model):
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200, unique=True)
    starting_age = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.question_text

    class Meta:
        ordering = ['routine', 'starting_age', 'question_text']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    last_submit_date = models.DateField(null=True, blank=True)
    submit_count = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Answer(models.Model):
    CHOICES = (
        (1, 'Not yet'),
        (2, 'Sometimes'),
        (3, 'Often/Beyond'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True, choices=CHOICES)

    class Meta:
        unique_together = (("question", "user"),)


class FunctionalDomain(models.Model):
    CHOICES = (
        ('E', 'E = engagement'),
        ('I', 'I = independence'),
        ('S', 'S = social relationships'),
    )
    question = models.ForeignKey(
        Question, related_name='func', on_delete=models.CASCADE)
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
    question = models.ForeignKey(
        Question, related_name='dev', on_delete=models.CASCADE)
    choice = models.CharField(max_length=2, choices=CHOICES)

    class Meta:
        unique_together = (("question", "choice"),)


class Outcome(models.Model):
    CHOICES = (
        ('S', 'S = positive social relations'),
        ('K', 'K = acquiring and using knowledge and skills'),
        ('A', 'A = taking action to meet needs'),
    )
    question = models.ForeignKey(
        Question, related_name='out', on_delete=models.CASCADE)
    choice = models.CharField(max_length=1, choices=CHOICES)

    class Meta:
        unique_together = (("question", "choice"),)


class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
    score_full = models.DecimalField(max_digits=4, decimal_places=2)
    score_age = models.DecimalField(max_digits=4, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)


class Archive(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    submit_count = models.PositiveSmallIntegerField()
    rating = models.IntegerField(choices=Answer.CHOICES)
    date = models.DateField()

    class Meta:
        unique_together = (("user", "question", "submit_count"),)
