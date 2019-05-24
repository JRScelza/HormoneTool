import dash
import dash_html_components as html
import dash_core_components as dcc
import random

import colorlover as cl

import numpy as np
import pandas as pd


# Create a DataFrame from the .csv file:
df = pd.read_csv("../cycle_viz/mock_hormone_data.csv")
######-------------------------------------------########

transition = {'duration': 2000, 'easing': 'cubic-in-out', 'redraw':True, 'fromcurrent': False}

external_stylesheets =['https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})  # noqa: E501


                        

app.layout = html.Div(
                    style={'backgroundColor':'#F9F0DF',
                           'margin':0

                           },
                    
                    children = [
        
        
        
                    html.Img(src=app.get_asset_url('logo.png'),style = {'width': 150}) ,
                    
                    html.A("About", target="_blank", href="https://www.oova.life", style={"color": "black", "text-decoration": "none", 'padding-left': 20, 'fontSize': 20}),
                
                    
                    html.P('''
                           Let us help you understand
                           ''',
                           style = {
                                 'fontSize' : 30,
                                 'color': 'ff9900',
                                 'font-family':'verdana',
                                 'textAlign': "center",
                                 'width': '100%',
                                 'marginBottom': 30
#                                 'padding-right': '30%',
#                                 'padding-left': '30%'
                                 
                                     }
                           ),
                    
#                    html.P('''
#                           way that I can think
#                           ''',
#                           style = {
#                                 'fontSize' : 20,
#                                 'color': 'ff9900',
#                                 'font-family':'verdana',
#                                 'textAlign': "center",
#                                 'width': '100%',
#                                 'margin': 0
##                                 'padding-right': '30%',
##                                 'padding-left': '30%'
#                                 
#                                     }
#                           ),
#                    
#                    html.P('''
#                           to get this done right now
#                           ''',
#                           style = {
#                                 'fontSize' : 20,
#                                 'color': 'ff9900',
#                                 'font-family':'verdana',
#                                 'textAlign': "center",
#                                 'width': '100%',
#                                 'margin-bottom': 40
##                                 'padding-right': '30%',
##                                 'padding-left': '30%'
#                                 
#                                     }
#                           ),

                    html.Div(
                            className = "row",
                            children = [
                                    
                                    html.Div(
                                            className = "three columns",
                                            style = {
                                                    'marginLeft' : 0,
                                                    'marginRight' : 0,
                                                    'borderTop':'3px solid #d6d6d6',
                                                    'borderBottom':'3px solid #d6d6d6'


                                                    },
                                            children = [
                                                    
                                                    html.H2("Cycle Type",
                                                                 style = {
                                                                         'fontSize' : 20,
                                                                         'color': 'ff9900',
                                                                         'font-family':'verdana',
                                                                         'textAlign': "left",
                                                                         'margin': 10,
                                                                         'padding-left': "20%"

                                                                         }),
    
                                               
                                                    html.Button('Short', 
                                                        id='btn-1',
                                                        className = 'one columns',
                                                        n_clicks_timestamp= 0 ,
                                                        ),
       
                                                   html.Button('Long', 
                                                                 id='btn-2',
                                                                 className = 'one columns',
                                                                 n_clicks_timestamp= 0
                                                                 ),
                                                    
                                                   html.Button('PCOS', 
                                                                 id='btn-3',
                                                                 className = 'one columns',
                                                                 n_clicks_timestamp= 0
                                                                 ),

                                                               
                                                   html.H2("Egg Release",
                                                     style = {
                                                             'fontSize' : 20,
                                                             'color': 'ff9900',
                                                             'font-family':'verdana',
                                                             'textAlign': "left",
                                                             'margin': 10,
                                                             'padding-left': "20%"
                                                            
                                                             }),
    
                                               
                                                    html.Button('Yes', 
                                                        id='btn-4',
                                                        className = 'one columns',
                                                        n_clicks_timestamp= 0 ,
                                                        ),
       
                                                   html.Button('No', 
                                                                 id='btn-5',
                                                                 className = 'one columns',
                                                                 n_clicks_timestamp= 0
                                                                 )
                                                   

                                                   ]),
                                    html.Div(
                                            className = "nine columns",
                                            children = [
                                                    dcc.Graph(id='lh-graph')
                                                    ]
                                            )
                                        ]
                                )
                            ]
                        )


@app.callback([dash.dependencies.Output('lh-graph', 'figure'),
               dash.dependencies.Output('btn-1', 'style'),
               dash.dependencies.Output('btn-2', 'style'),
               dash.dependencies.Output('btn-3', 'style'),
               dash.dependencies.Output('btn-4', 'style'),
               dash.dependencies.Output('btn-5', 'style')],
              [dash.dependencies.Input('btn-1', 'n_clicks_timestamp'),
               dash.dependencies.Input('btn-2', 'n_clicks_timestamp'),
               dash.dependencies.Input('btn-3', 'n_clicks_timestamp'),
               dash.dependencies.Input('btn-4', 'n_clicks_timestamp'),
               dash.dependencies.Input('btn-5', 'n_clicks_timestamp')])

def display(btn1, btn2, btn3, btn4, btn5):
    
    if int(btn1) > int(btn2) and int(btn1) > int(btn3):
        start = 0
        data = df['lh_short'].values
        
        style1 = {
            'backgroundColor': "#A52D04",
            'color': '#FEF9DD',
            'width':'90%',
            'margin': '5%'            }
        
        style2 = {
            'backgroundColor': "#FEF9DD",
            'color': '#A52D04',
            'width':'90%',
            'margin': '5%'            }
                
        style3 = {
            'backgroundColor': "#FEF9DD",
            'color': '#A52D04',
            'width':'90%',
            'margin': '5%'            }
        
        
    elif int(btn2) > int(btn1) and int(btn2) > int(btn3):
        start = 0
        data = df['lh_long'].values
        
        style1 = {
            'backgroundColor': "#FEF9DD",
            'color': '#A52D04',
            'width':'90%',
            'margin': '5%'            }
        
        style2 = {
            'backgroundColor': "#A52D04",
            'color': '#FEF9DD',
            'width':'90%',
            'margin': '5%'            }
                
        style3 = {
            'backgroundColor': "#FEF9DD",
            'color': '#A52D04',
            'width':'90%',
            'margin': '5%'            }
        
    elif int(btn3) > int(btn1) and int(btn3) > int(btn2):
        start = 0
        data = df['lh_pcos'].values
        
        style1 = {
            'backgroundColor': "#FEF9DD",
            'color': '#A52D04',
            'width':'90%',
            'margin': '5%'            }
        
        style2 = {
            'backgroundColor': "#FEF9DD",
            'color': '#A52D04',
            'width':'90%',
            'margin': '5%'            }
                
        style3 = {
            'backgroundColor': "#A52D04",
            'color': '#FEF9DD',
            'width':'90%',
            'margin': '5%'            }
        
    else:
        start = 1
        style1 = {
            'backgroundColor': "#FEF9DD",
            'color': '#A52D04',
             'width':'90%',
             'margin': '5%'
            }
        
        style2 = {
            'backgroundColor': "#FEF9DD",
            'color': '#A52D04',
             'width':'90%',
             'margin': '5%'

            }
                
        style3 = {
            'backgroundColor': "#FEF9DD",
            'color': '#A52D04',
            'width':'90%',
            'margin': '5%'

            }
        
    if int(btn4) > int(btn5):
        start = 0
        pg_data = df['pg_normal'].values

        
        style4 = {
            'backgroundColor': "#4B0082",
            'color': '#FEF9DD',
            'width':'90%',
            'margin': '5%'

            }
        
        style5 = {
            'backgroundColor': "#FEF9DD",
            'color': '#4B0082',
            'width':'90%',
            'margin': '5%'

            }
        
    elif int(btn5) > int(btn4):
        start = 0
        pg_data = df['pg_not'].values

        
        style4 = {
            'backgroundColor': "#FEF9DD",
            'color': '#4B0082',
            'width':'90%',
            'margin': '5%'

            }
        
        style5 = {
            'backgroundColor': "#4B0082",
            'color': '#FEF9DD',
            'width':'90%',
            'margin': '5%'

            }

    else:
        start = 1
        style4 = {
            'backgroundColor': "#FEF9DD",
            'color': '#4B0082',
            'width':'90%',
            'margin': '5%'

            }
        
        style5 = {
            'backgroundColor': "#FEF9DD",
            'color': '#4B0082',
            'width':'90%',
            'margin': '5%'

            }


    if start == 0:
        x = np.array(range(0, len(data)))
        y = data
        
        data2 = df['lh_normal'].values
        x2 = np.array(range(0, len(data2)))
        y2 = data2
        
        
        pg_x = np.array(range(0, len(pg_data)))
        pg_y = pg_data
        
        pg_x_fx = np.array(range(0, len(df['pg_normal'].values)))
        pg_y_fx = df['pg_normal'].values
        
        
        figure = {
                'data': [{
                    'type': 'scatter',
                    'mode': 'lines+markers',
                    'x' : x,
                    'y' : y,
                    'name' : " ",
                    'opacity' : 1.0,
                    
                    'line' : {
                            'width' : 4,
                            'color' : "#A52D04"
                            }
                },
                
                {
                    'type': 'scatter',
                    'mode': 'lines+markers',
                    'x' : x2,
                    'y' : y2,
                    'name' : "Considered Normal LH",
                    'opacity' : 0.2,
                    
                    'line' : {
                            'width' : 4,
                            'color' : "#A52D04"
                            }
                },
                
                    
                {
                    'type': 'scatter',
                    'mode': 'lines+markers',
                    'x' : pg_x,
                    'y' : pg_y,
                    'name' : " ",
                    'opacity' : 1.0,
                    
                    'line' : {
                            'width' : 4,
                            'color' : "#4B0082"
                            }
                },
                    
                {
                    'type': 'scatter',
                    'mode': 'lines+markers',

                    'x' : pg_x_fx,
                    'y' : pg_y_fx,
                    'name' : "Considered Normal PG",
                    'opacity' : 0.2,
                    
                    'line' : {
                            'width' : 4,
                            'color' : "#4B0082"
                            }
                }
            
                ],
        
                'layout': {
                    'paper_bgcolor' : '#FCF1DA',
                    'plot_bgcolor' : '#FCF1DA',
                    'xaxis' : {
                            'title' : 'Cycle',
                            'showticklabels' : False
                            },
                    'yaxis' : {
                        'showticklabels' : False,
                        'range' : [0,26],
                        'autorange' :False
                            },
                    'height': 400,
                    'transition': transition
    
    
                }
        }
    
    else:
        pg_start_x = np.array([random.randint(0,20) for a in range(0,28)])
        pg_start_y = np.array([random.randint(0,4) for a in range(0,20)])
        lh_start_x = np.array([random.randint(0,20) for a in range(0,28)])
        lh_start_y = np.array([random.randint(12,16) for a in range(0,20)])
                
        figure = {
                        
                'data': [{
                    'type': 'scatter',
                    'x' : pg_start_x,
                    'y' : pg_start_y,
                    'name' : " ",
                    'opacity' : 1.0,
                    'mode': 'markers',
                    
                    'line' : {
                            'width' : 4,
                            'color' : "#A52D04"
                            }
                },
                
                {
                    'type': 'scatter',
                    'mode': 'markers',

                    'x' : lh_start_x,
                    'y' : lh_start_y,
                    'name' : "Considered Normal LH",
                    'opacity' : 0.2,
                    
                    'line' : {
                            'width' : 4,
                            'color' : "#A52D04"
                            }
                }
                ],
        
                'layout': {
                    'paper_bgcolor' : '#FCF1DA',
                    'plot_bgcolor' : '#FCF1DA',
                    'xaxis' : {
                            'title' : 'Cycle',
                            'showticklabels' : False
                            },
                    'yaxis' : {
                        'showticklabels' : False,
                        'range' : [0,26],
                        'autorange' :False
                            },
                    'height': 400,
                    'transition': transition
    
    
                }
        }
    
    return figure, style1, style2, style3, style4, style5





if __name__ == '__main__':
    app.run_server( port = 8928, debug=True)




