import plotly.offline as pyo
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import calendar

######-------------------------------------------########
######-------------------------------------------########
######-------------------------------------------########
######-------------------------------------------########
######-------------------------------------------########
filter_year = '2013'

# Create a DataFrame from the .csv file:
df1 = pd.read_csv('../data/tick_data_1500_22413.csv')
df2 = pd.read_csv('../data/tick_data_22414_54003.csv')

df = pd.concat([df1  ,df2])

year_index = df['Date tick was removed'].str.startswith(filter_year)
df_filtered_year = df[year_index]
df_filtered_year['Date tick was removed'] = pd.to_datetime(df_filtered_year['Date tick was removed'] , errors='coerce')
df_filtered_year = df_filtered_year.dropna(subset=['Date tick was removed'])
df_filtered_year.index = range(len(df_filtered_year))








site_index = df_filtered_year['Site of Attachment'].value_counts().index[:12]

df_cl = df_filtered_year[df_filtered_year['Site of Attachment'].isin(site_index)]


site_index_unid = ["Unidentified" if x== 'None' else x for x in site_index]
labels = site_index_unid
values = df_cl['Site of Attachment'].value_counts()

data = [go.Pie(labels=labels, values=values)]

layout = go.Layout(
    title= "Tick Site of Attachment"
)

fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='basic_histogram3.html')