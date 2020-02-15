import os
import pickle
from coronavirus.settings import BASE_DIR
from stats_pipeline.plot import plot_results
from django.shortcuts import render
from django.http import JsonResponse


def get_country_state(request, *args, **kwargs):
    country_state = {}
    country_state['country'] = {}
    with open(os.path.join(BASE_DIR, 'predictions/predictions.pickle'), 'rb') as handle:
        predictions = pickle.load(handle)
    country_state['total_stats'] = predictions['total_stats']
    for country in predictions:
        country_state['country'][country] = [state for state in predictions[country]]
    return render(request, 'corona_dash.html', {'country_state': country_state})



def getTimeSeriesGraph(request, *args, **kwargs):
    with open(os.path.join(BASE_DIR, 'predictions/predictions.pickle'), 'rb') as handle:
        predictions = pickle.load(handle)
    country = request.GET.get('country')
    state = request.GET.get('state')
    plotResults = plot_results(predictions)
    plotResults.plot(country, state)
    with open(os.path.join(BASE_DIR, 'templates/fig.html')) as f:
        fileContent = f.read()
    ratios = {}
    ratios['risk_ratio'] = predictions[country][state]['risk_ratio']
    ratios['fatality_ratio'] = predictions[country][state]['fatality_ratio']
    ratios['recovery_prof_ratio'] = predictions[country][state]['recovery_prof_ratio']
    ratios['cases_till_date'] = predictions[country][state]['all_cases'][-1]
    ratios['cases_predicted'] = int(predictions[country][state]['forecast'][-1])

    return JsonResponse({'fileContent': fileContent, 'ratios': ratios}, status=200, content_type='application/json')