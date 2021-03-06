from datetime import datetime

def remove_keys(dic):
    for country in dic:
        for state, value in dic[country].items():
            if country == state:
                dic[country]['All'] = value
                del dic[country][state]
    return dic

def check_len(dic):
    a = {}
    for country in dic:
        for state in dic[country]:
            if len(dic[country][state]['dates']) > 2:
                if country not in a:
                    a[country] = {}
                if state not in a[country]:
                    a[country][state] = {}
                a[country][state]['dates'] = dic[country][state]['dates']
                a[country][state]['cases'] = dic[country][state]['cases']

    return a

def convert_datetime(df):
    df['date1'] = df['ObservationDate'].apply(lambda x: datetime.strptime(x, '%m/%d/%Y'))
    df['date'] = df['date1'].apply(lambda x: x.date())
    df['time'] = df['date1'].apply(lambda x: x.time())
    df = df.drop(['ObservationDate', 'date1'], axis=1)
    df = df.reindex(columns=['SNo', 'Country/Region','Province/State', 'date', 'time','Last Update',
                             'Confirmed', 'Deaths', 'Recovered'])
    return df

def stats_df(df):
    con_sta = df.groupby(["Country/Region", "Province/State"])['Confirmed','Deaths','Recovered', 'date'].last().reset_index()
    con = con_sta.groupby(["Country/Region"]).sum().reset_index()
    return con_sta, con

def provide_general_stats(df):
    output = {'confirmed':'',
              'deaths':'',
              'recovered':''}
    output['confirmed'] = '{:,.0f}'.format(df["Confirmed"].sum())
    output['deaths'] = '{:,.0f}'.format(df["Deaths"].sum())
    output['recovered'] = '{:,.0f}'.format(df["Recovered"].sum())
    return output


def convert_dic(con_sta, con):
    dic = {}
    for (country, state, confirm, death, recover) in zip(con_sta['Country/Region'], con_sta['Province/State'],
                                                         con_sta['Confirmed'], con_sta['Deaths'], con_sta['Recovered']):
        if country not in dic:
                dic[country] = {}
        if state not in dic[country]:
            dic[country][state] = {}
        dic[country][state]['state_total_confirmed'] = confirm
        dic[country][state]['state_total_deaths'] = death
        dic[country][state]['state_total_recover'] = recover
        dic[country][state]['total_confirmed'] = int(con[con["Country/Region"] == country]["Confirmed"].values[0])
        dic[country][state]['total_deaths'] = int(con[con["Country/Region"] == country]["Deaths"].values[0])
        dic[country][state]['total_recover'] = int(con[con["Country/Region"] == country]["Recovered"].values[0])

    # dic = remove_keys(dic)
    return dic

def stats(dic):
    stats_dic = {}
    for country in dic:
        if country not in stats_dic:
            stats_dic[country] = {}
        for state in dic[country]:
            if state not in stats_dic[country]:
                stats_dic[country][state] = {}

            stats_dic[country][state]['state_total_confirmed'] = '{:,.0f}'.format(dic[country][state]['state_total_confirmed'])
            stats_dic[country][state]['state_total_deaths'] = '{:,.0f}'.format(dic[country][state]['state_total_deaths'])
            stats_dic[country][state]['state_total_recover'] = '{:,.0f}'.format(dic[country][state]['state_total_recover'])
            stats_dic[country][state]['total_confirmed'] = '{:,.0f}'.format(dic[country][state]['total_confirmed'])
            stats_dic[country][state]['total_deaths'] = '{:,.0f}'.format(dic[country][state]['total_deaths'])
            stats_dic[country][state]['total_recover'] = '{:,.0f}'.format(dic[country][state]['total_recover'])
            # stats_dic[country][state]['risk_ratio'] = "%.*f" % (
            # 8, dic[country][state]['state_total_confirmed'] / pop[country][state])
            stats_dic[country][state]['fatality_ratio'] = "%.*f" % (
            8, dic[country][state]['state_total_deaths'] / dic[country][state]['total_confirmed'])
            stats_dic[country][state]['recovery_prof_ratio'] = "%.*f" % (
            8, dic[country][state]['state_total_recover'] / dic[country][state]['total_confirmed'])
    return stats_dic

def convert_df_to_dic(df):
    confirmed = {}
    deaths = {}
    recovered = {}
    for country, state, date, confirm, death, recover in zip(df['Country/Region'], df['Province/State'], df['date'],
                                                                  df['Confirmed'],df['Deaths'], df['Recovered']):
        if country not in confirmed:
            confirmed[country] = {}
            deaths[country] = {}
            recovered[country] = {}
        if state not in confirmed[country]:
            confirmed[country][state] = {}
            deaths[country][state] = {}
            recovered[country][state] = {}
            confirmed[country][state]['dates'] = []
            confirmed[country][state]['cases'] = []
            deaths[country][state]['dates'] = []
            deaths[country][state]['cases'] = []
            recovered[country][state]['dates'] = []
            recovered[country][state]['cases'] = []
        confirmed[country][state]['dates'].append(date)
        confirmed[country][state]['cases'].append(confirm)
        deaths[country][state]['dates'].append(date)
        deaths[country][state]['cases'].append(death)
        recovered[country][state]['dates'].append(date)
        recovered[country][state]['cases'].append(recover)

    # confirmed = remove_keys(confirmed)
    # deaths = remove_keys(deaths)
    # recovered = remove_keys(recovered)
    valid_confirmed = check_len(confirmed)
    valid_deaths = check_len(deaths)
    valid_recovered = check_len(recovered)
    return (valid_confirmed, valid_deaths, valid_recovered)

def train_test_split(dic):
    split_dic = {}
    for country in dic:
        if country not in split_dic:
            split_dic[country] = {}
        for state in dic[country]:
            if state not in split_dic[country]:
                split_dic[country][state] = {}
            split_dic[country][state]['dates'] = dic[country][state]['dates']
            split_dic[country][state]['cases'] = dic[country][state]['cases']
            size = len(split_dic[country][state]['dates'])
            split_dic[country][state]['train_dates'] = dic[country][state]['dates'][:int(size*0.8)]
            split_dic[country][state]['train_cases'] = dic[country][state]['cases'][:int(size*0.8)]
            split_dic[country][state]['test_dates'] = dic[country][state]['dates'][int(size*0.8):]
            split_dic[country][state]['test_cases'] = dic[country][state]['cases'][int(size*0.8):]
    return split_dic