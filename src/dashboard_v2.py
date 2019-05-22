import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import calendar

import colorlover as cl

import numpy as np
import pandas as pd

mapbox_access_token = 'pk.eyJ1IjoianJzY2VsemEiLCJhIjoiY2prMm5qZTYwMHU0ZTNwcWtndno5ZzR5OCJ9.qLnaoYVwnSe3oVBhSukL6A' 
# import plotly.offline as pyo
# import plotly.graph_objs as go
# import numpy as np
# import pandas as pd
# import calendar

# import plotly
# plotly.tools.set_credentials_file(username='jrscelza', api_key='rXxEmpCf6iH93hKgFUON')

######-------------------------------------------########

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/Nuclear%20Waste%20Sites%20on%20American%20Campuses.csv')
site_lat = df.lat
site_lon = df.lon
locations_name = df.text

######-------------------------------------------########

# Create a DataFrame from the .csv file:
df1 = pd.read_csv('../data/tick_data_1500_22413.csv')
df2 = pd.read_csv('../data/tick_data_22414_54003.csv')
df = pd.concat([df1  ,df2])

bupu = cl.scales['8']['seq']['Blues']
pie_colors = cl.interp( bupu[3:], 20 )[8:]

barColor='rgb(36,219,239)'

month_labels = ['Jan' , 'Feb' , 'Mar' , 'Apr' ,'May' , 'Jun' ,'Jul' ,'Aug' ,'Sep' , 'Oct','Nov' ,'Dec']


######-------------------------------------------########
######-------------------------------------------########


app = dash.Dash()

app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})  # noqa: E501


app.layout = html.Div([

    html.Div([
        
        html.H1(children = "Tick Report Data", style = {
            "color" : '#000000'
        }, className = 'ten columns'),

        html.Img(src = 'http://www.nextgenhealthcare.org/wp-content/themes/4525-ingh/assets/images/logo.svg', height='80', width='160'
        , className = 'two columns')

    ], className = 'row', style={'backgroundColor': '#FFFFFF'}),

    html.Div([

        html.Div(children='An interactive dashboard for exploring the Tick Report Data by year', style={
            'textAlign': 'left',
            'color': '#000000'
        }),
    
    ], className = 'row', style={'backgroundColor': '#FFFFFF'}),


    html.Div([
        html.Div([

            dcc.Slider(
                id='year-slider',
                min=2010,
                max = 2018,
                step = None,
                value=2015,
                marks={
                    2010: {'label': '2010', 'style': {'color': '#000000'}},
                    2011: {'label': '2011', 'style': {'color': '#000000'}},
                    2012: {'label': '2012', 'style': {'color': '#000000'}},
                    2013: {'label': '2013', 'style': {'color': '#000000'}},
                    2014: {'label': '2014', 'style': {'color': '#000000'}},
                    2015: {'label': '2015', 'style': {'color': '#000000'}},
                    2016: {'label': '2016', 'style': {'color': '#000000'}},
                    2017: {'label': '2017', 'style': {'color': '#000000'}},
                    2018: {'label': '2018', 'style': {'color': '#000000'}}
                }
            )
        ], className = 'twelve columns')
    ], className = 'row', style={'margin-left': 60 , 'margin-right': 60, "margin-bottom": 20}),

    html.Div([

        html.Div([dcc.Graph(id='reported-histo')

        ], className = 'eight columns'),

        html.Div([dcc.Graph(id='site-pie')
        ], className = 'four columns')

    ], className = 'row', style={'backgroundColor': '#000000'}),

    html.Div([

        html.Div([dcc.Graph(id='species-bar')

        ], className = 'four columns'),
        
        html.Div([dcc.Graph(id='exposure-histo')

        ], className = 'four columns', style={'backgroundColor': '#000000'}),

        html.Div([dcc.Graph(id='bacteria-bar')

        ], className = 'four columns')
    
    ], className = 'row', style={'backgroundColor': '#FFFFFF', "margin-top": 10}),

    html.Div([

        html.Div([dcc.Graph(id='scatter-map')

        ], className = 'twelve columns', style={'backgroundColor': '#000000'})

        ], className = 'row', style={'backgroundColor': '#000000', "margin-top": 10})

    ], style={'backgroundColor': '#FFFFFF'})




@app.callback(
    dash.dependencies.Output('exposure-histo', 'figure'),
    [dash.dependencies.Input('year-slider', 'value')])
def update_histo(selected_year):
    year_index = df['Date tick was removed'].str.startswith(str(selected_year))
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
    
    return {
        'data': [go.Histogram(
            x = values,
            name = 'exposure time'
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'Length of Time in Minutes',
                'showticklabels' : True

            },
            yaxis={
                'title': 'Total Hits',
            },
            hovermode='closest',
            bargap = 0.4,
            plot_bgcolor =  '#000000',
            paper_bgcolor =  '#000000',
            font = dict(
                    color = "#FFFFFF"),
            title = 'Distribution of Attachment Time in Minutes'
            
        )
    }

@app.callback(
    dash.dependencies.Output('site-pie', 'figure'),
    [dash.dependencies.Input('year-slider', 'value')])
def update_pie(selected_year):
    year_index = df['Date tick was removed'].str.startswith(str(selected_year))
    df_filtered_year = df[year_index]
    df_filtered_year['Date tick was removed'] = pd.to_datetime(df_filtered_year['Date tick was removed'] , errors='coerce')
    df_filtered_year = df_filtered_year.dropna(subset=['Date tick was removed'])
    df_filtered_year.index = range(len(df_filtered_year))

    site_index = df_filtered_year['Site of Attachment'].value_counts().index[:12]

    df_cl = df_filtered_year[df_filtered_year['Site of Attachment'].isin(site_index)]
    site_index_unid = ["Unidentified" if x== 'None' else x for x in site_index]


    body_labels = site_index_unid
    body_values = df_cl['Site of Attachment'].value_counts()
    
    return {
      'data': [go.Pie(
            labels=body_labels, 
            values=body_values,
            marker=dict(colors=pie_colors, 
                line=dict(color='#FFFFFF', width=2)),
            textfont = dict( color = '#FFFFFF'),
            outsidetextfont = dict( color = "#FFFFFF")
            )], 
        'layout' : go.Layout(
            plot_bgcolor =  'rgba(0,0,0,0)',
            paper_bgcolor =  'rgba(0,0,0,0)',
            title = 'Attachment Site Locations',
            font = dict(
                color = '#FFFFFF'
            ),


            legend=dict(
                traceorder='normal',
                font=dict(
                    family='sans-serif',
                    size=12,
                    color='#000000'
                ),
                bgcolor='#FFFFFF',
                bordercolor='#FFFFFF',
                borderwidth=2
            ),

        )
    
    }





@app.callback(
    dash.dependencies.Output('reported-histo', 'figure'),
    [dash.dependencies.Input('year-slider', 'value')])
def update_reported(selected_year):
    year_index = df['Date tick was removed'].str.startswith(str(selected_year))
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
        x = df_filtered_year['month'].value_counts().sort_values().index.tolist(),
        y = df_filtered_year['month'].value_counts().sort_values().tolist(),
        name = 'Total Reported',
        marker = dict(color = '#4169E1')
    )

    trace2 = go.Bar(
        x = lst2,
        y = grouped[['1']].tolist(),
        name = 'Borrelia burgdorferi Positive',
        marker = dict(color = '#48D1CC')
    )

    data = [trace1, trace2]

    return {
        'data': data,
        'layout': go.Layout(
            xaxis={
                'title': 'Percentile',
                'ticktext': month_labels,
                'tickvals': [i for i in range(1,13)],
            },
            yaxis={
                'title': 'Total Hits',
            },
            hovermode='closest',
            bargap = 0.4,
            title = 'Monthly Reported Cases',

            legend=dict(
                x=0,
                y=1,
                traceorder='normal',
                font=dict(
                    family='sans-serif',
                    size=12,
                    color='#000000'
                ),
                bgcolor='#FFFFFF',
                bordercolor='#FFFFFF',
                borderwidth=2
            ),
            plot_bgcolor =  'rgba(0,0,0,0)',
            paper_bgcolor =  'rgba(0,0,0,0)',
            font = dict(
                    color = "#FFFFFF")
        )
    }


@app.callback(
    dash.dependencies.Output('species-bar', 'figure'),
    [dash.dependencies.Input('year-slider', 'value')])
def update_species(selected_year):
    year_index = df['Date tick was removed'].str.startswith(str(selected_year))
    df_filtered_year = df[year_index]
    df_filtered_year['Date tick was removed'] = pd.to_datetime(df_filtered_year['Date tick was removed'] , errors='coerce')
    df_filtered_year = df_filtered_year.dropna(subset=['Date tick was removed'])
    df_filtered_year.index = range(len(df_filtered_year))

    
    
    return {
        'data': [go.Bar(
            x = df_filtered_year['Species'].value_counts().tolist()[::-1],
            y = df_filtered_year['Species'].value_counts().index.tolist()[::-1],
            orientation = 'h',
            marker=dict(
                color= barColor)
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'Count'},
            hovermode='closest',
            bargap = 0.4,
            title = 'Tick Species Quantities',
            margin=go.Margin(
                l=200,
                r=0,
                b=100,
                t=100,
                pad=4
                ),
            plot_bgcolor =  '#000000',
            paper_bgcolor =  '#000000',
            font = dict(
                    color = "#FFFFFF")
        )
    }


@app.callback(
    dash.dependencies.Output('bacteria-bar', 'figure'),
    [dash.dependencies.Input('year-slider', 'value')])
def update_bacteria(selected_year):
    year_index = df['Date tick was removed'].str.startswith(str(selected_year))
    df_filtered_year = df[year_index]
    df_filtered_year['Date tick was removed'] = pd.to_datetime(df_filtered_year['Date tick was removed'] , errors='coerce')
    df_filtered_year = df_filtered_year.dropna(subset=['Date tick was removed'])
    df_filtered_year.index = range(len(df_filtered_year))

    df_bacteria = df_filtered_year[df_filtered_year.columns[17:]]
    df_bacteria.replace('None', 0, inplace=True)
    df_bacteria = df_bacteria.apply(pd.to_numeric)
    
    bacteria_values = df_bacteria.sum(axis = 0).sort_values()[1:18]
    bacteria_index = df_bacteria.sum(axis = 0).sort_values()[1:18].index

    return {
        'data': [go.Bar(
            x = bacteria_values,
            y = bacteria_index,
            orientation = 'h',
            marker=dict(
                color= barColor)
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'Count'},
            yaxis=dict(
                ticktext =  bacteria_index,
                tickvals = [i for i in range(len(bacteria_index))]),
            hovermode='closest',
            bargap = 0.4,
            title = 'Bacteria Species Quantities',
            margin=go.Margin(
                l=200,
                r=0,
                b=100,
                t=100,
                pad=4
                ),
            plot_bgcolor =  '#000000',
            paper_bgcolor =  '#000000',
            font = dict(
                    color = "#FFFFFF")
        )
    }





### TEMP MAP#####


@app.callback(
    dash.dependencies.Output('scatter-map', 'figure'),
    [dash.dependencies.Input('year-slider', 'value')])
def update_map(selected_year):
    bob = selected_year
    return {

        "data" : [
            go.Scattermapbox(
                lat=['45.5017'],
                lon=['-73.5673'],
                mode='markers',
                marker=dict(
                    size=14
                ),
                text=['Montreal'],
            )
        ],

        "layout" : go.Layout(
            height = 800,
            autosize=False,
            hovermode='closest',
            plot_bgcolor =  '#000000',
            paper_bgcolor =  '#000000',
            mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=0,
                center=dict(
                    lat=45,
                    lon=-73
                ),
                pitch=0,
                zoom=5
            ),
        )
    }



# Add the server clause:
if __name__ == '__main__':
    app.run_server()