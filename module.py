import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def format_full(df, code_df):
    
    df['code'] = None
    df.columns = ['date', 'country', 'state', 'lat', 'long', 'confirmed', 'recovered', 'deaths', 'code']
    df.drop(['lat', 'long'], axis = 1, inplace = True)
    
    codes = code_df.drop(['Alpha-2 code', 'Numeric code', 'Latitude (average)', 'Longitude (average)'], axis = 1)
    codes.columns = ['country', 'code']
    
    rename_dict = codes.set_index('country').to_dict()['code']
    
    df.date = pd.to_datetime(df.date)
    df.sort_values('date', ascending = True, inplace = True)
    df.recovered = df.recovered.fillna(0)
    df['code'] = df.country
    df.code = df.code.replace(rename_dict)
    df.recovered = df.recovered.fillna(0)

    
    df = df.sort_values(['country', 'date'])
    df.set_index('date', inplace = True)
    
    df = df[['country', 'code', 'state', 'confirmed', 'recovered', 'deaths']]
    
    df = df.groupby(['country', 'date', 'code']).sum().reset_index()
    df = df.set_index('date')

    
    return df

def create_country_dict(df):
    country_df_names = []
    for country in df.country.unique().tolist():
        df_name = f"{country}"
        country_df_names.append(df_name)
        
    country_df_dict = {}
    
    for name in country_df_names:
     
        country_df_dict[name] = df[df.country == name]
    
    return country_df_dict


def plot_time_series(df_dict):
    for key in df_dict.keys():
        
        t = df_dict[key].plot(figsize = (30, 10), color = ['blue', 'green', 'red'], lw = 2)
        t.set_xlabel('Date', fontweight = 'bold', fontsize = 25)
        t.set_ylabel('Number of Cases', fontweight = 'bold', fontsize = 25)
        t.set_title(f'{key} COVID-19 Progression', fontsize = 35, fontweight = 'bold')
        t.tick_params(axis = 'both', which = 'both', labelsize = 20)
        t.legend(loc = 'best', prop = {'size': 20}, frameon = True, edgecolor = 'black', fancybox = True, facecolor = 'white', framealpha = .9)
        
    return t
        
        
        