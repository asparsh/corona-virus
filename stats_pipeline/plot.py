import os

import plotly.graph_objs as go#visualization
from plotly.offline import plot
from coronavirus.settings import BASE_DIR

class plot_results():
    def __init__(self, pred):
        self.pred = pred

    def plot(self, country, state):
        print(country, state)

        trace1 = {
            "fill": None,
            "mode": "markers",
            "name": "Confirmed cases",
            "type": "scatter",
            "x": self.pred[country][state]['all_dates'] + self.pred[country][state]['forecast_dates'],
            "y": self.pred[country][state]['all_cases'],
        }
        trace2 = {
            "fill": "tonexty",
            #           "line": {"color": "#1efded"},
            "mode": "lines",
            "name": "upper bound",
            "type": "scatter",
            "x": self.pred[country][state]['test_dates'] + self.pred[country][state]['forecast_dates'],
            "y": self.pred[country][state]['upper_test'] + self.pred[country][state]['upper'],

        }

        trace3 = {
            "fill": "tonexty",
            #           "line": {"color": "#57b8ff"},
            "mode": "lines",
            "name": "lower bound",
            "type": "scatter",
            "x": self.pred[country][state]['test_dates'] + self.pred[country][state]['forecast_dates'],
            "y": self.pred[country][state]['lower_test'] + self.pred[country][state]['lower'],

        }
        trace4 = {
            #           "fill": "tonexty",
            #           "line": {"color": "#a6e22e"},
            "mode": "lines",
            "name": "Model predictions",
            "type": "scatter",
            "x": self.pred[country][state]['all_dates'] + self.pred[country][state]['forecast_dates'],
            "y": self.pred[country][state]['train_original'] + self.pred[country][state]['forecast_test'] +
                 self.pred[country][state]['forecast'],

        }

        data = go.Data([trace1, trace2, trace3, trace4])
        layout = {
            "title": "Cases in " + country + " for " + state,
            "xaxis": {
                "title": "Dates",
                "ticklen": 5,
                "gridcolor": "rgb(255, 255, 255)",
                "gridwidth": 2,
                "zerolinewidth": 1
            },
            "yaxis": {
                "title": 'Cases',
                "ticklen": 5,
                "gridcolor": "rgb(255, 255, 255)",
                "gridwidth": 2,
                "zerolinewidth": 1
            },

            "plot_bgcolor": "rgb(243, 243, 243)",
            "paper_bgcolor": "rgb(243, 243, 243)"
        }
        config = {"responsive" : True}

        fig = go.Figure(data=data, layout=layout)
        plot(fig, filename=os.path.join(BASE_DIR, 'templates/fig.html'), auto_open=False, config=config)

