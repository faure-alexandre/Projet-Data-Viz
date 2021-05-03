# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 16:27:41 2021

@author: Alexandre
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
import plotly.graph_objs as go
import pandas as pd


# Gestion des données
echanges = pd.read_csv("data/echanges_internationaux_ocde.csv")

echanges = echanges[['SUBJECT','Country','FREQUENCY', 'TIME','Value']].loc[echanges.MEASURE=='CXMLSA',:]

available_countries = echanges['Country'].unique()


# Layout
layout = html.Div([
                html.H2(
                        children="Echanges internationaux",
                        style={
                            'textAlign': 'center',
                            }
                    ),
    
              html.Div([
                html.Div([
                    dcc.Dropdown(
                    id='selection_pays',
                    options=[{'label': i, 'value': i} for i in available_countries],
                    value='France'
                    )],
                    style={'width': '20%', 'display': 'inline-block'}),
                
                html.Div([
                    dcc.RadioItems(
                        id='selection_frequence',
                        options=[{'label': 'Par trimestre', 'value': 'Q'}, 
                                 {'label': 'Par mois', 'value': 'M'}],
                        value='Q',
                        labelStyle={'display': 'inline-block'}
                        ),
                    
                    dcc.RadioItems(
                        id='selection_types_imports',
                        options=[{'label': 'Importations', 'value': 'XTIMVA01'}, 
                                 {'label': 'Exportations', 'value': 'XTEXVA01'},
                                 {'label': 'Echanges nets', 'value': 'XTNTVA01'}],
                        value='XTIMVA01',
                        labelStyle={'display': 'inline-block'}
                        )
                    ],
                    className = 'block_boutons_radios',
                    style={'width': '20%', 'display': 'inline-block', 'color': 'white', 'margin': '10px'}),
    
                dcc.Graph(id='importations_graph', style={'width': '1000px', 'height': '350px'}),
          ], style={'margin-top': '50px', 'margin-left': '10px'},
             className = '1er_graph') 
              
        ], className = 'bloc_page')


# Callback
@app.callback(
    Output('importations_graph', 'figure'),
    [Input('selection_pays', 'value')],
    [Input('selection_frequence', 'value')],
    [Input('selection_types_imports', 'value')])
def update_figure(selected_country, selected_frequency, selected_subject):
    
    echanges_filter = echanges[echanges.Country== selected_country][echanges.FREQUENCY== selected_frequency][echanges.SUBJECT== selected_subject]
    # Création de la trame 1
    if selected_subject=='XTEXVA01':
        titlee="Exportations en billion de dollars"
    elif selected_subject=='XTIMVA01':
        titlee="Importations en billion de dollars"
    elif selected_subject=='XTNTVA01':
        titlee="Echanges nets en billion de dollars"


    fig1=go.Figure()
    fig1.add_trace(go.Scatter(
                    x = echanges_filter.TIME,
                    y = echanges_filter.Value,
                    mode = "lines",
                    name = "citations",
                    marker = dict(color = 'red'),
                    line=dict(width=4)))#rgba(16, 112, 2, 0.8)


    fig1.update_layout(title = 'Echanges internationaux',
              xaxis = dict(title = 'Time',ticklen =5,zeroline= False),
              yaxis = dict(title = str(titlee),ticklen =5,zeroline= False)
              )

    fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',title_font_color="white",font_color='white',legend_title_font_color='white',font=dict(size=14))
    
    return fig1
