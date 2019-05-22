
import dash
import dash_core_components as dcc
import dash_html_components as html
import colorlover as cl


import plotly.offline as pyo
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import calendar

import plotly
plotly.tools.set_credentials_file(username='jrscelza', api_key='rXxEmpCf6iH93hKgFUON')

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


######-------------------------------------------########
######-------------------------------------------########


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
mu, sigma = np.mean(values) , np.std(values)
s = np.random.normal(mu, sigma, 4000)

######-------------------------------------------########

site_index = df_filtered_year['Site of Attachment'].value_counts().index[:12]

df_cl = df_filtered_year[df_filtered_year['Site of Attachment'].isin(site_index)]
site_index_unid = ["Unidentified" if x== 'None' else x for x in site_index]


body_labels = site_index_unid
body_values = df_cl['Site of Attachment'].value_counts()


######-------------------------------------------########
bupu = cl.scales['4']['seq']['Blues']
pie_colors = cl.interp( bupu, 20 )[8:]

######-------------------------------------------########
######-------------------------------------------########

colors = {
    'background': '#111111',
    'text': '#000000'}

layout =  {
    'plot_bgcolor': colors['background'],
    'paper_bgcolor': colors['background'],
    'font': {
        'color': colors['text']
    },
    'bargap': 0.5
}

app = dash.Dash()

app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})  # noqa: E501


app.layout = html.Div([

    html.Div([

        html.Div([
            dcc.Graph(
                id='histogram',
                figure={
                    'data': [
                        go.Histogram(
                            x = s,
                            name = 'sam'
                        )
                    ],
                'layout': layout} 
            )] , className = 'five columns' ), 
        
        html.Div([
            dcc.Graph(
                id='body-pie',
                figure={
                    'data': [
                        go.Pie(labels=body_labels, 
                        values=body_values,
                        marker=dict(colors=pie_colors, 
                           line=dict(color='#FFFFFF', width=2)))] , 
               'layout' : layout }
            )
        ] , className = 'six columns')
    ], className = 'row'),

    html.Div([

        html.Div([
            dcc.Graph(
                id='histo-2',
                figure={
                    'data': [
                        go.Histogram(
                            x = s,
                            name = 'sam'
                        )
                    ], 'layout' : layout
                }
            ) 
            ] , className = 'twelve columns' )
    ], className = 'row'),
    
    
    html.Div(
        dcc.Slider(
            id='crossfilter-year--slider',
            min= '2012',
            max= '2016',
            value='2016',
            step=None,
    ), style={'width': '49%', 'padding': '0px 20px 20px 20px'} , className = 'row')
 
] , style={'backgroundColor': colors['background']})



if __name__ == '__main__':
    app.run_server()
