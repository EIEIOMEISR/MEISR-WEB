import pygal

from .models import *


class ScoreBarChart():

    def __init__(self, routine,score_type,**kwargs):
        self.score_type = score_type
        self.routine = routine
        self.routine.description = routine.description
        self.chart = pygal.Bar(**kwargs)
        self.chart.title = 'MEISR Results: ' + routine.description 
        if self.score_type == "age":
            self.chart.title += " to Age Score"
        elif self.score_type == "full":
            self.chart.title += " Full Routine Score"
        #self.chart.x_labels = map(str, range(1, 10))

    def get_data(self,user,routine,score_type):
        '''
        Query the db for chart data, pack them into a dict and return it.
        '''
        data = {}
        for score in Score.objects.filter(user=user).filter(routine=routine).order_by('timestamp'):
            if score_type == "age":
                data[str(score.timestamp)] = score.score_age
            elif score_type == "full":
                data[str(score.timestamp)] = score.score_full
        return data

    def generate(self,user):
        # Get chart data
        chart_data = self.get_data(user,self.routine,self.score_type)

        # Add data to chart
        for key, value in chart_data.items():
            self.chart.add(key, value)

        # Return the rendered SVG
        return self.chart.render(is_unicode=True)
