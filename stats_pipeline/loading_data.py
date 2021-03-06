import pandas as pd
import os
import pickle
from coronavirus.settings import BASE_DIR
from stats_pipeline import helper_functions


def read_and_clean_data():
    # with open(os.path.join(BASE_DIR, 'data/population.p'), 'rb') as fp:
    #     population = pickle.load(fp)
    dataset = pd.read_csv(os.path.join(BASE_DIR, "data/covid_19_data07June.csv"))
    dataset['Country/Region'] = dataset['Country/Region'].apply(lambda x:'China' if x=='Mainland China' else x)
    dataset['Province/State'] = dataset['Province/State'].apply(lambda x:'Chicago' if x=='Chicago, IL' else x)
    dataset['Province/State'].fillna("All", inplace=True)
    dataset.loc[dataset['Province/State'] == 'Taiwan', 'Country/Region'] = "Taiwan"
    dataset.loc[dataset['Province/State'] == 'Macau', 'Country/Region'] = "Macau"
    indexNames = dataset[ (dataset['Confirmed'] == 0) & (dataset['Deaths'] == 0) & (dataset['Recovered'] == 0) ].index
    dataset.drop(indexNames , inplace=True)
    indexNames = dataset[(dataset['Confirmed'] == 0)].index
    dataset.drop(indexNames, inplace=True)

    dataset = helper_functions.convert_datetime(dataset)
    con_sta, con = helper_functions.stats_df(dataset)
    sum_stats = helper_functions.provide_general_stats(con)
    data_dic = helper_functions.convert_dic(con_sta, con)
    stats_dic = helper_functions.stats(data_dic)
    confirmed_dic, death_dic, recover_dic = helper_functions.convert_df_to_dic(dataset)
    confirm_dataset = helper_functions.train_test_split(confirmed_dic)
    death_dataset = helper_functions.train_test_split(death_dic)
    recover_dataset = helper_functions.train_test_split(recover_dic)
    return (confirm_dataset, death_dataset, recover_dataset, dataset, stats_dic, sum_stats)



