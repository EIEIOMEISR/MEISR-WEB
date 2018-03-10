from django.views import generic

from .models import Question


class IndexView(generic.ListView):
    template_name = 'survey/index.html'

    def get_queryset(self):
        return Question.objects.order_by('section')