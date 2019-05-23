import dash
import dash_html_components as html
import dash_core_components as dcc

import colorlover as cl

import numpy as np
import pandas as pd



# Create a DataFrame from the .csv file:
df = pd.read_csv("../cycle_viz/mock_hormone_data.csv")
######-------------------------------------------########
######-------------------------------------------########

external_stylesheets =['https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#
app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})  # noqa: E501
#
#
app.layout = html.Div([
        
    html.Button('Short', 
                id='btn-1',
                className = 'one columns',
                n_clicks_timestamp= 0 ,
                style = {
                        'backgroundColor' :  '#4CAF50'
                        }
                ),
                
     html.Button('Long', 
                 id='btn-2',
                 className = 'one columns',
                 n_clicks_timestamp= 0 ,
                 style = {
                        'backgroundColor' :  '#4CAF50'
                        }
                 ),
    
    html.Button('PCOS', 
                 id='btn-3',
                 className = 'one columns',
                 n_clicks_timestamp= 0,
                 style = {
                        'backgroundColor' :  '#4CAF50'
                        }
                 ),
    
    html.Div([dcc.Graph(id='lh-graph')],
              className = 'nine columns')
    ]
)

@app.callback([dash.dependencies.Output('lh-graph', 'figure'),
               dash.dependencies.Output('btn-1', 'style'),
               dash.dependencies.Output('btn-2', 'style'),
               dash.dependencies.Output('btn-3', 'style')],
              [dash.dependencies.Input('btn-1', 'n_clicks_timestamp'),
               dash.dependencies.Input('btn-2', 'n_clicks_timestamp'),
               dash.dependencies.Input('btn-3', 'n_clicks_timestamp')])

def display(btn1, btn2, btn3):
    
    if int(btn1) > int(btn2) and int(btn1) > int(btn3):
        data = df['lh_short'].values
        
        style1 = {
            'backgroundColor': "#C13605"
            }
        
        style2 = {
            'backgroundColor': "#FEF9DD"
            }
                
        style3 = {
            'backgroundColor': "#FEF9DD"
            }
        
        
    elif int(btn2) > int(btn1) and int(btn2) > int(btn3):
        data = df['lh_long'].values
        
        style1 = {
            'backgroundColor': "#FEF9DD"
            }
        
        style2 = {
            'backgroundColor': "#C13605"
            }
                
        style3 = {
            'backgroundColor': "#FEF9DD"
            }
        
    elif int(btn3) > int(btn1) and int(btn3) > int(btn2):
        data = df['lh_pcos'].values
        
        style1 = {
            'backgroundColor': "#FEF9DD"
            }
        
        style2 = {
            'backgroundColor': "#FEF9DD"
            }
                
        style3 = {
            'backgroundColor': "#C13605"
            }
        
    else:
        data = df['lh_normal'].values
        
        style1 = {
            'backgroundColor': "#FEF9DD"
            }
        
        style2 = {
            'backgroundColor': "#FEF9DD"
            }
                
        style3 = {
            'backgroundColor': "#FEF9DD"
            }
        
    x = np.array(range(0, len(data)))
    y = data
        
    figure = {
            'data': [{
                'type': 'scatter',
                'x' : x,
                'y' : y,
                'name' : "Normal LH",
                'opacity' : 0.2,
                
                'line' : {
                        'width' : 4,
                        'color' : "#A52D04"
                        }

            }],
    
            'layout': {
                'paper_bgcolor' : '#FCF1DA',
                'plot_bgcolor' : '#FCF1DA',
                'xaxis' : {
                        'title' : 'Cycle',
                        'showticklabels' : False
                        },
                'yaxis' : {
                'showticklabels' : False
                        }
            }
    }
    
    return figure, style1, style2, style3


if __name__ == '__main__':
    app.run_server( port = 8921, debug=True)




