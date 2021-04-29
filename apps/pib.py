# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 10:46:47 2021

@author: Arnaud
"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go
import pandas as pd

from app import app

df_pib = pd.read_csv("PIB.csv")
df_pib = df_pib[['LOCATION', 'TIME', 'Value']]
liste_pays = df_pib['LOCATION'].unique()
temps = df_pib['TIME'].unique()


# app = dash.Dash()
# colors = {
#     'background': 'rgba(255, 255, 128, .5)',
#     'text': '#7FDBFF'
# }

# server = app.server

# Reference & Documentation
layout = html.Div(children=[ 
    html.H1(
        children='PIB trimestriel',
        style={
            'textAlign': 'center'
        }
    ),
    html.Div(children='Indice de volume du PIB par trimestre', style={
        'textAlign': 'center'
    }),
    dcc.Graph(id='graph_pib'),
    dcc.Dropdown(
                id='selection_pays',
                options=[{'label': pays, 'value': pays} for pays in liste_pays],
                value='OECD',
                # multi=True
            ),
])

@app.callback(
    Output('graph_pib', 'figure'),
    [Input('selection_pays', 'value')])
def update_figure(choix_pays):
    
    
    df_filter = df_pib[df_pib.LOCATION == choix_pays]
    # Création de la trame 1
    trace1 = go.Scatter(
                    x = df_filter.TIME,
                    y = df_filter.Value,
                    mode = "lines",
                    name = "citations",
                    marker = dict(color = 'rgba(16, 112, 2, 0.8)')) 


    data = [trace1]
    layout = dict(title = 'PIB trimestriel',
              xaxis = dict(title = 'Trimestre',ticklen =5,zeroline= False),
              yaxis = dict(title = 'Indice de volume du PIB',ticklen =5,zeroline= False)
              )
    fig = dict(data = data, layout = layout)

    return fig


# if __name__ == '__main__':
#     app.run_server(debug=True, use_reloader=False)
