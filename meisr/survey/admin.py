from django.contrib import admin

from .models import Question
from .models import Answer
from .models import Child
from .models import FunctionalDomain
from .models import DevelopmentalDomain
from .models import Outcome

class QuestionAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Question._meta.fields]

class AnswerAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Answer._meta.fields]

class ChildAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Child._meta.fields]

class FunctionalDomainAdmin(admin.ModelAdmin):
	list_display = [field.name for field in FunctionalDomain._meta.fields]

class DevelopmentalDomainAdmin(admin.ModelAdmin):
	list_display = [field.name for field in DevelopmentalDomain._meta.fields]

class OutcomeAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Outcome._meta.fields]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Child, ChildAdmin)
admin.site.register(FunctionalDomain, FunctionalDomainAdmin)
admin.site.register(DevelopmentalDomain, DevelopmentalDomainAdmin)
admin.site.register(Outcome, OutcomeAdmin)
