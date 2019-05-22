import plotly.offline as pyo
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import calendar

import plotly
plotly.tools.set_credentials_file(username='jrscelza', api_key='rXxEmpCf6iH93hKgFUON')



import random

######-------------------------------------------########
######-------------------------------------------########
######-------------------------------------------########
######-------------------------------------------########
######-------------------------------------------########
filter_year = '2015'

# Create a DataFrame from the .csv file:
df1 = pd.read_csv('../data/tick_data_1500_22413.csv')
df2 = pd.read_csv('../data/tick_data_22414_54003.csv')

df = pd.concat([df1  ,df2])

year_index = df['Date tick was removed'].str.startswith(filter_year)
df_filtered_year = df[year_index]
df_filtered_year['Date tick was removed'] = pd.to_datetime(df_filtered_year['Date tick was removed'] , errors='coerce')
df_filtered_year = df_filtered_year.dropna(subset=['Date tick was removed'])
df_filtered_year.index = range(len(df_filtered_year))


index_of_hours = np.where(df_filtered_year['Time Attached'].str.contains("Hours"))
index_of_minutes = np.where(df_filtered_year['Time Attached'].str.contains("Minutes"))

df_filtered_year['exposure'] = ['None']*len(df_filtered_year)
df_filtered_year['exposure'][index_of_hours[0]] = df_filtered_year['Time Attached'][index_of_hours[0]].str.split(' ').str[0]
df_filtered_year['exposure'][index_of_minutes[0]] = df_filtered_year['Time Attached'][index_of_minutes[0]].str.split(' ').str[0]

histo_data = df_filtered_year[df_filtered_year['exposure'] != 'None']
histo_data['exposure'] = histo_data['exposure'].astype(float)
histo_data['exposure'][index_of_hours[0]] = histo_data['exposure'][index_of_hours[0]]*60

histo_data['exposure'] = histo_data['exposure'] / 60

values = histo_data['exposure']


# mu, sigma = np.mean(values) , np.std(values)
# s = np.random.normal(mu, sigma, 4000)



######-------------------------------------------########
######-------------------------------------------########
######-------------------------------------------########
######-------------------------------------------########

data = [go.Histogram(
    x=values,
    name = 'sam'
)]


layout = {
    'shapes': [
        # Line Horizontal
        {
            'type': 'line',
            'x0': 0,
            'y0': np.mean(values),
            'x1': 100,
            'y1': np.mean(values),
            'line': {
                'color': 'rgb(50, 171, 96)',
                'width': 4
            },
        }
    ],
    'showlegend': True
}



fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='wide_histogram.html')
