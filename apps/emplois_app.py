# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 16:27:41 2021

@author: Alexandre
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from app import app


# Gestion des donnees
emploi_resume = pd.read_csv("data/emploi_resume.csv")
df_resume = emploi_resume.loc[:,['LOCATION', 'TIME', 'Value']]

emploi = pd.read_csv("data/emploi.csv")
df = emploi.loc[:,['Pays', 'TIME', 'Value']].loc[emploi.SUBJECT == 'LREM64FE']

available_countries = df['Pays'].unique()
available_countries2 = df_resume['LOCATION'].unique()


# Layout
layout = html.Div([
    html.H2(
            children="Taux d'emploi",
            style={
            'textAlign': 'center',
            }),
    dcc.Graph(id='graph_slider', style={'width': '75%', 'height': '350px', 'opacity': '0.8'}),
    dcc.Dropdown(
                id='selection_pays',
                options=[{'label': i, 'value': i} for i in available_countries],
                value='France',
                style={'width': '40%', 'textAlign': 'center'}
            ),
    html.H2(
            children="Stats agrégées",
            style={
            'textAlign': 'center',
            }),
    dcc.Graph(id='graph_slider2', style={'width': '75%', 'height': '350px', 'opacity': '0.8'},
              figure={
            'data': [
                go.Scatter(
                    x=df_resume[df_resume.LOCATION == i].TIME,
                    y=df_resume[df_resume.LOCATION == i].Value,
                    text=df_resume[df_resume.LOCATION == i]['LOCATION'],
                    mode='markers+lines',
                    opacity=0.8,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in available_countries2 
            ],
            'layout': go.Layout(
                xaxis={'title': 'Time'},  # 'type':'log'
                yaxis={'title': 'Taux d\'emploi'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0.0, 'y': 1},
                hovermode='closest',
                height=500
            )
        }
              ),
    
], style={'text-align': 'center'})


# Callback
@app.callback(
    Output('graph_slider', 'figure'),
    [Input('selection_pays', 'value')])
def update_figure(selected_country):
    
    df_filter = df[df.Pays== selected_country]
    # Création de la trame 1
    trace1 = go.Scatter(
                    x = df_filter.TIME,
                    y = df_filter.Value,
                    mode = "lines",
                    name = "citations",
                    marker = dict(color = 'rgba(16, 112, 2, 0.8)')) 


    data = [trace1]
    layout = dict(title = 'Taux d\'emploi',
              xaxis = dict(title = 'Time',ticklen =5,zeroline= False),
              yaxis = dict(title = 'Taux d\'emploi',ticklen =5,zeroline= False)
              )
    fig = dict(data = data, layout = layout)

    return fig

    
    
    