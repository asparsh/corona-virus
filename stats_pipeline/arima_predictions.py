import os
import pickle
import numpy as np
from datetime import timedelta
from stats_pipeline import loading_data
from coronavirus.settings import BASE_DIR
from statsmodels.tsa.arima_model import ARIMA

class arima_model():
    def __init__(self, data, stats):
        self.data = data
        self.stats = stats

    def initialise_pred(self, country, state):
        self.pred[country][state]['lower_test'] = []
        self.pred[country][state]['upper_test'] = []
        self.pred[country][state]['error_test'] = []
        self.pred[country][state]['forecast_test'] = []
        self.pred[country][state]['forecast_dates'] = []
        self.pred[country][state]['forecast'] = []
        self.pred[country][state]['lower'] = []
        self.pred[country][state]['upper'] = []
        self.pred[country][state]['state_total_confirmed'] = self.stats[country][state]['state_total_confirmed']
        self.pred[country][state]['state_total_deaths'] = self.stats[country][state]['state_total_deaths']
        self.pred[country][state]['state_total_recover'] = self.stats[country][state]['state_total_recover']
        self.pred[country][state]['total_confirmed'] = self.stats[country][state]['total_confirmed']
        self.pred[country][state]['total_deaths'] = self.stats[country][state]['total_deaths']
        self.pred[country][state]['total_recover'] = self.stats[country][state]['total_recover']
        # self.pred[country][state]['risk_ratio'] = self.stats[country][state]['risk_ratio']
        self.pred[country][state]['fatality_ratio'] = self.stats[country][state]['fatality_ratio']
        self.pred[country][state]['recovery_prof_ratio'] = self.stats[country][state]['recovery_prof_ratio']
        self.pred[country][state]['all_cases'] = self.data[country][state]['cases']
        self.pred[country][state]['all_dates'] = self.data[country][state]['dates']
        self.pred[country][state]['train_cases'] = [x for x in self.data[country][state]['train_cases']]
        self.pred[country][state]['train_dates'] = self.data[country][state]['train_dates']
        self.pred[country][state]['test_dates'] = self.data[country][state]['test_dates']
        self.pred[country][state]['test_cases'] = self.data[country][state]['test_cases']
        self.pred[country][state]['train_original'] = self.data[country][state]['train_cases']

    def check_negative(self, pred, key):
        for country in pred:
            for state in pred[country]:
                for index in range(len(pred[country][state][key])):
                    if pred[country][state][key][index] < 0:
                        pred[country][state][key][index] = 0

        return pred

    def initialise_model(self, value, num, train):
        if value:
            model = ARIMA(train, order=(4, 1, 0))
            model_fit = model.fit(trend='nc', disp=False)
            forecast, stderr, conf = model_fit.forecast(num)
        else:
            model = ARIMA(train, order=(1, 0, 0))

            model_fit = model.fit(trend='nc', disp=False)
            forecast, stderr, conf = model_fit.forecast(num)
        return forecast, stderr, conf

    def generate_dates(self, from_date, days):
        return [from_date + timedelta(days=day) for day in range(1, days + 1)]

    def return_results(self, country, state, pred, forcast_test, lower_test, upper_test, test_case, error):
        pred[country][state]['forecast_test'].append(forcast_test)
        pred[country][state]['lower_test'].append(lower_test)
        pred[country][state]['upper_test'].append(upper_test)
        pred[country][state]['train_cases'].append(test_case)
        pred[country][state]['error_test'].append(str(error))
        return pred

    def model_pediction(self):
        self.pred = {}
        for country in self.data:
            if country not in self.pred:
                self.pred[country] = {}
            for state in self.data[country]:
                if state not in self.pred[country]:
                    self.pred[country][state] = {}
                self.initialise_pred(country, state)
                if (len(self.data[country][state]['train_cases']) > 2):
                    if np.mean(self.data[country][state]['train_cases']) != self.data[country][state]['train_cases'][0]:
                        for test in range(len(self.data[country][state]['test_cases'])):
                            try:
                                forecast, stderr, conf = self.initialise_model(True, 1,
                                                                               self.pred[country][state]['train_cases'])
                                self.pred = self.return_results(country, state, self.pred, forecast, conf[0][0],
                                                                conf[0][1],
                                                                self.data[country][state]['test_cases'][test], stderr)
                            except:
                                forecast, stderr, conf = self.initialise_model(False, 1,
                                                                               self.pred[country][state]['train_cases'])
                                self.pred = self.return_results(country, state, self.pred, forecast, conf[0][0],
                                                                conf[0][1],
                                                                self.data[country][state]['test_cases'][test], stderr)
                        try:
                            forecast, stderr, conf = self.initialise_model(True, 7, self.data[country][state]['cases'])
                            self.pred[country][state]['forecast'] += list(forecast)
                            self.pred[country][state]['lower'] += list(conf[:, 0])
                            self.pred[country][state]['upper'] += list(conf[:, 1])
                            self.pred[country][state]['forecast_dates'] += self.generate_dates(self.data[country][state]['dates'][-1], 7)
                        except:
                            forecast, stderr, conf = self.initialise_model(False, 7, self.data[country][state]['cases'])
                            self.pred[country][state]['forecast'] += list(forecast)
                            self.pred[country][state]['lower'] += list(conf[:, 0])
                            self.pred[country][state]['upper'] += list(conf[:, 1])
                            self.pred[country][state]['forecast_dates'] += self.generate_dates(self.data[country][state]['dates'][-1], 7)
                    else:
                        size = len(self.pred[country][state]['test_cases'])
                        self.pred[country][state]['forecast_test'] += self.pred[country][state]['test_cases']
                        self.pred[country][state]['lower_test'] += [(self.data[country][state]['train_cases'][-1] - 5)] * size
                        self.pred[country][state]['upper_test'] += [(self.data[country][state]['train_cases'][-1] + 5)] * size
                        self.pred[country][state]['train_dates'] += self.pred[country][state]['test_dates']
                        self.pred[country][state]['train_cases'] += self.data[country][state]['test_cases']
                        self.pred[country][state]['error_test'].append(str(0))
                        self.pred[country][state]['forecast'] += [self.pred[country][state]['test_cases'][-1]] * 7
                        self.pred[country][state]['lower'] += [(self.pred[country][state]['test_cases'][-1] - 5)] * 7
                        self.pred[country][state]['upper'] += [(self.pred[country][state]['test_cases'][-1] + 5)] * 7
                        self.pred[country][state]['forecast_dates'] += self.generate_dates(
                            self.data[country][state]['dates'][-1], 7)
        self.pred = self.check_negative(self.pred, 'lower')
        self.pred = self.check_negative(self.pred, 'lower_test')
        return self.pred

    def store_predictions(self, pred):
        with open(os.path.join(BASE_DIR, 'predictions/predictions.pickle'), 'wb') as fp:
            pickle.dump(pred, fp, protocol=pickle.HIGHEST_PROTOCOL)

if __name__=="__main__":
    confirm_dataset, death_dataset, recover_dataset, dataset, stats_dic, sum_stats = loading_data.read_and_clean_data()
    model = arima_model(confirm_dataset, stats_dic)
    pred = model.model_pediction()
    pred['total_stats'] = sum_stats
    model.store_predictions(pred)