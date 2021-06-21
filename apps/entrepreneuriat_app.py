# -*- coding: utf-8 -*-
"""
Created on Sat May  8 17:13:29 2021

"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from app import app
from plotly.subplots import make_subplots
import numpy as np


# Gestion des donnees
creation = pd.read_csv("data/creations_entreprises.csv")
faillites = pd.read_csv("data/faillites_entreprises.csv")

a = creation[creation.ISIC4=='01_99'].Country.unique()
b = creation[creation.ISIC4=='01_99C'].Country.unique()

df_creations = pd.concat([creation[creation.ISIC4=='01_99'],creation[(creation.ISIC4=='01_99C') & (creation.Country.isin(b[~np.isin(b, a)]))]], ignore_index=True)

a = faillites[faillites.ISIC4=='01_99'].Country.unique()
b = faillites[faillites.ISIC4=='01_99C'].Country.unique()

df_faillites = pd.concat([faillites[faillites.ISIC4=='01_99'],faillites[(faillites.ISIC4=='01_99C') & (faillites.Country.isin(b[~np.isin(b, a)]))]], ignore_index=True)

df_creations = df_creations.loc[df_creations.TIME > '2015', ['Country', 'TIME', 'Value']]
df_faillites = df_faillites.loc[df_faillites.TIME > '2015', ['Country', 'TIME', 'Value']]


available_countries = np.unique( 
    np.concatenate((df_faillites['Country'].unique(), df_creations['Country'].unique())) )

# Layout
layout = html.Div([
    
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
                        options=[{'label': 'Par année', 'value': 'A'},
                                 {'label': 'Par trimestre', 'value': 'Q'}, 
                                 {'label': 'Par mois', 'value': 'M'}],
                        value='M',
                        labelStyle={'display': 'inline-block'}
                        )
                    ],
                    className = 'block_boutons_radios',
                    style={'width': '30%', 'display': 'inline-block', 'color': 'white', 'margin': '10px'}),
    
                dcc.Graph(id='entrepreneuriat_graph', style={'width': '90%', 'height': '60%'}),
          
                  dcc.RangeSlider(
                                  min=1950,
                                  max=2022,
                                  value=[2018, 2022],
                                  marks={
                                      1950: {'label': '1950', 'style': {'color': '#77b0b1'}},
                                      2000: {'label': '2000'},
                                      2018: {'label': '2018'},
                                      2022: {'label': '2021', 'style': {'color': '#f50'}}
                                      },
                                  id='selection_date'
                                  ),  
            ], style={'margin-top': '50px', 'margin-left': '10px'},
             className = '1er_graph') 
              
        ], className = 'bloc_page')


# Callback
@app.callback(
    Output('entrepreneuriat_graph', 'figure'),
    [Input('selection_pays', 'value')],
    [Input('selection_frequence', 'value')],
    [Input('selection_date', 'value')])
def update_figure(selected_country, selected_frequency, selected_time):
    
    time_min = str(selected_time[0]) 
    time_max = str(selected_time[1]) 
    
    fig1=go.Figure()
    
    df_filter_creations = df_creations[(df_creations.Country== selected_country)]
    df_filter_faillites = df_faillites[(df_faillites.Country== selected_country)]
            
    fig1.add_trace(go.Scatter(
                    x = df_filter_creations.TIME,
                    y = df_filter_creations.Value,
                    mode = "lines",
                    name = 'creations',
                    line=dict(width=3)))
    
    fig1.add_trace(go.Scatter(
                    x = df_filter_faillites.TIME,
                    y = df_filter_faillites.Value,
                    mode = "lines",
                    name = 'faillites',
                    line=dict(width=3)))


    fig1.update_layout(title = 'Cours des actions',
              xaxis = dict(title = 'Time',ticklen =5,zeroline= False),
              yaxis = dict(title = 'Cours actions',ticklen =5,zeroline= False)
              )

    fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',title_font_color="white",font_color='white',legend_title_font_color='white',font=dict(size=14))
    
    return fig1