import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
        df_dict[key].sort_values('date', ascending = [True], inplace = True)
        df_dict[key].drop(columns = ['lat', 'long'], inplace = True)
        df_dict[key].set_index('date', inplace = True)
        df_dict[key] = df_dict[key].groupby(['date', 'country']).sum().reset_index()
        df_dict[key].set_index('date', inplace = True)
        
        df_dict[key]['recovered'] = df_dict[key]['recovered'].fillna(0)
        
        df_dict[key]['conf_pct_change'] = df_dict[key]['confirmed'].pct_change(periods = 1).fillna(0)
        df_dict[key]['rec_pct_change'] = df_dict[key]['recovered'].pct_change(periods = 1).fillna(0)
        df_dict[key]['death_pct_change'] = df_dict[key]['deaths'].pct_change(periods = 1).fillna(0)
        
    return df_dict

def plot_time_series(df_dict):
    for key in df_dict.keys():
        fig, (ax1, ax2, ax3) = plt.subplots(nrows = 1, ncols = 3, figsize = (30,5))
        
        ax1.plot(df_dict[key]['confirmed'], color = 'blue', lw = 3, label = 'Confirmed')
        ax2.plot(df_dict[key]['recovered'], color = 'green', lw = 3, label = 'Recovered')
        ax3.plot(df_dict[key]['deaths'], color = 'red', lw = 3, label = 'Deaths')
        
        ax1.set_ylabel('Number of People', fontsize = 14, fontweight = 'bold')
        
        ax1.set_title('Confirmed')
        ax2.set_title('Recovered')
        ax3.set_title('Deaths')
        
        plt.suptitle(f"{key[:-3]}", fontsize = 25, fontweight = 'bold', y = 1.08)
        
        plt.tight_layout()
        
        