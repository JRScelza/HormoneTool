import plotly.offline as pyo
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import calendar

# Create a DataFrame from the .csv file:
df1 = pd.read_csv('../data/tick_data_1500_22413.csv')
df2 = pd.read_csv('../data/tick_data_22414_54003.csv')

df = pd.concat([df1  ,df2])

filter_year = '2015'

year_index = df['Date tick was removed'].str.startswith(filter_year)
df_filtered_year = df[year_index]
df_filtered_year['Date tick was removed'] = pd.to_datetime(df_filtered_year['Date tick was removed'] , errors='coerce')
df_filtered_year = df_filtered_year.dropna(subset=['Date tick was removed'])
df_filtered_year.index = range(len(df_filtered_year))



df_filtered_year['month'] = df_filtered_year['Date tick was removed'].dt.month
di = dict((v,k) for k,v in enumerate(calendar.month_abbr))
labels = list(di.keys())[1:]

df_new = pd.DataFrame({
    "month" : df_filtered_year['month'],
    "Borrelia" : df_filtered_year['Borrelia burgdorferi sensu lato'],
    "Moyonii" : df_filtered_year['Borrelia mayonii']
})

grouped = df_new.groupby(["Borrelia" , "month"]).size()
grouped.reset_index

lst = list(grouped[['1']].index)
lst2 = [item[1] for item in lst]


trace1 = go.Bar(
    x = df_filtered_year['month'].value_counts().index.tolist(),
    y = df_filtered_year['month'].value_counts().tolist(),
    name = 'Total Reported',
    marker = dict(color = '#9EA0A1')
)

trace2 = go.Bar(
    x = lst2,
    y = grouped[['1']].tolist(),
    name = 'Borrelia burgdorferi Positive',
    marker = dict(color = '#CD7F32')
)


data = [trace2 , trace1 ] 

layout = go.Layout(
    title = 'Total Tick Reports %s' % filter_year, # Graph title
    xaxis = dict(title = 'Some random x-values' , 
                range=[1, 12],
                tickvals = list(range(1,13)),
                ticktext = labels), # x-axis label
    yaxis = dict(title = 'Some random y-values'), # y-axis label
    hovermode ='closest', # handles multiple points landing on the same vertical,
    barmode = 'stack'
)

fig = go.Figure(data = data, layout = layout)
pyo.plot(fig, filename='scatter3.html')




