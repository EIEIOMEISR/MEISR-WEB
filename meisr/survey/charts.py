import pygal

from .models import *


class ScoreBarChart():

    def __init__(self, **kwargs):
        self.chart = pygal.Bar(**kwargs)
        self.chart.title = 'MEISR Results' 
        self.chart.x_labels = map(str, range(1, 10))

    def get_data(self,user,score_type):
        '''
        Query the db for chart data, pack them into a dict and return it.
        '''
        data = {}
        for score in Score.objects.filter(user=user):
            if score_type == 0:
                if score.routine.description in data:
                    data[score.routine.description].append(score.score_age)
                else:
                    data[score.routine.description] = [score.score_age]
            elif score_type == 1:
                if score.routine.description in data:
                    data[score.routine.description].append(score.score_full)
                else:
                    data[score.routine.description] = [score.score_full]
        return data

    def generate(self,user,score_type):
        # Get chart data
        chart_data = self.get_data(user,score_type)

        # Add data to chart
        for key, value in chart_data.items():
            self.chart.add(key, value)

        # Return the rendered SVG
        return self.chart.render(is_unicode=True)
