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
from plotly.subplots import make_subplots


# Gestion des donnees
emploi_resume = pd.read_csv("data/emploi_resume.csv")
df_resume = emploi_resume.loc[:,['LOCATION', 'TIME', 'Value']]

emploi = pd.read_csv("data/emploi.csv")
df = emploi.loc[:,['Pays', 'TIME', 'Value']].loc[emploi.SUBJECT == 'LREM64FE']

available_countries = df['Pays'].unique()
available_countries2 = df_resume['LOCATION'].unique()
color=['#fea347','red','green']
fig_c = make_subplots()
for i in range(len(available_countries2)):
    fig_c.add_trace(go.Scatter(
                    x=df_resume[df_resume.LOCATION == available_countries2[i]].TIME,
                    y=df_resume[df_resume.LOCATION == available_countries2[i]].Value,
                    text=df_resume[df_resume.LOCATION == available_countries2[i]]['LOCATION'],
                    mode='markers+lines',
                    marker={
                        'size': 20,
                        'color': color[i],
                        'line': {'width': 2, 'color': 'white'}
                    },
                    name=available_countries2[i]
                ) )
fig_c.update_layout(xaxis={'title': 'Time'},  # 'type':'log'
                yaxis={'title': 'Taux d\'emploi'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0.0, 'y': 1},
                hovermode='closest',
                height=500)
fig_c.update_layout(paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',title_font_color="white",font_color='white',legend_title_font_color='white',font=dict(size=14))


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
    dcc.Graph(id='graph_slider2', style={'width': '75%', 'height': '350px'},
              figure=fig_c)
], style={'text-align': 'center'})


# Callback
@app.callback(
    Output('graph_slider', 'figure'),
    [Input('selection_pays', 'value')])
def update_figure(selected_country):
    
    df_filter = df[df.Pays== selected_country]
    # Création de la trame 1
    fig1=go.Figure()

    fig1.add_trace(go.Scatter(
                    x = df_filter.TIME,
                    y = df_filter.Value,
                    mode = "lines",
                    name = "citations",
                    marker = dict(color = 'red'),
                    line=dict(width=4))) #rgba(16, 112, 2, 0.8)


    fig1.update_layout(title = 'Taux d\'emploi',
              xaxis = dict(title = 'Time',ticklen =5,zeroline= False),
              yaxis = dict(title = 'Taux d\'emploi',ticklen =5,zeroline= False)
              )
    fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',title_font_color="white",font_color='white',legend_title_font_color='white',font=dict(size=14))
    
    return fig1

    
    
    