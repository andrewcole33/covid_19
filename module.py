import pandas as pd
import numpy as np
import os

def gather_data():
    confirmed_df = pd.read_csv('data/time_series_covid19_confirmed_global.csv')
    deaths_df = pd.read_csv('data/time_series_covid19_deaths_global.csv')
    recovered_df = pd.read_csv('data/time_series_covid19_deaths_global.csv')
    
    df_list = [confirmed_df, deaths_df, recovered_df]
    for df in df_list:
        df['total'] = df.iloc[:,4:].sum(axis = 1)
        
    return confirmed_df, deaths_df, recovered_df


def create_country_dict(df):
    country_df_names = []
    for country in df.country.unique().tolist():
        df_name = f"{country}_df"
        country_df_names.append(df_name)
        
    country_df_dict = {}
    for name in country_df_names:
        country_df_dict[name] = df[df.country == name[:-3]]
    
    return country_df_dict

def format_time_series(df_dict):
    for key in df_dict.keys():
        df_dict[key].date = pd.to_datetime(df_dict[key].date)
        df_dict[key].set_index('date', inplace = True)
        df_dict[key].drop('country', axis = 1, inplace = True)
    return df_dict