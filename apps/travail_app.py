# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 16:27:41 2021

"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from app import app
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc


# Gestion des donnees
chomage = pd.read_csv("data/chomage.csv")

chomage = chomage.loc[:,['LOCATION', 'TIME', 'SUBJECT', 'FREQUENCY', 'Value']].loc[chomage.TIME>='2007',:]

available_countries = chomage['LOCATION'].unique()


inputs =  dbc.Card([
            dbc.CardHeader('Gestion des paramètres'),
            dbc.CardBody([
                html.H6("Selection d'un pays:"),
                html.Div([
                    dcc.Dropdown(
                    id='selection_pays',
                    options=[{'label': i, 'value': i} for i in available_countries],
                    #value=['France', 'United States', 'Japan', 'India'],
                    value='FRA',
                    clearable=False
                    )],
                    style={'width': '100%'}),
                
                html.Br(),
                html.H6("Selection des pays en fond:"),
                html.Div([
                    dcc.Dropdown(
                    id='selection_fond',
                    options=[{'label': i, 'value': i} for i in available_countries],
                    #value=['G7', 'United States', 'OECD - Total', 'Euro area (19 countries)'],
                    value=['G-7', 'USA', 'OECD', 'EA19'],
                    multi=True
                    )], 
                    style={'width': '100%'}),
                
                html.Br(),
                html.H6("Selection fréquence:"),
                dcc.RadioItems(
                        id='selection_frequence',
                        options=[{'label': 'Par année', 'value': 'A'}, 
                                 {'label': 'Par trimestre', 'value': 'Q'}, 
                                 {'label': 'Par mois', 'value': 'M'}],
                        value='Q',
                        labelStyle={'margin-left':'10px', 'cursor': 'pointer'}
                        )
                ]),
            #dbc.CardHeader('A propos des données'),
            ], color="light", outline=True, style={'width': '15%', 'display': 'inline-block', 'height': '400px', 'margin-left': '25px', 'vertical-align': 'top'})


# Layout
layout = html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(id='graph_chomage', style={'width': '45%', 'height': '350px', 'display': 'inline-block', 'margin-right': '30px'}),
                    dcc.Graph(id='graph_chomage_sexe', style={'width': '45%', 'height': '350px', 'display': 'inline-block'}),
                    ], style={'text-align': 'center'}),
                
                html.Div([
                    dbc.Button(
                        "Interprétation",
                        id="collapse-button",
                        className="mb-3",
                        color="primary",
                        ),
                    dbc.Collapse(
                        dbc.Card([
                            dbc.CardHeader("Interprétation"),
                            dbc.CardBody([
                                html.P("Ce graphique permet de mettre en évidence l'impact de la crise du covid sur le marché de l'emploi."),
                                html.P("Le taux de chômage, au sens du Bureau international du Travail (BIT), qui définit un chômeur comme une personne ayant recherché \
                                        activement un emploi dans le mois précédent, a diminué juqu'au mois de mai 2020 avant de progressé pour atteindre en moyenne 9 % de la population active durant l'été 2020\
                                        en France, de juillet à septembre. Ce qui représente 628.000 personnes de plus sur la période, ou 2,7 millions au total."),
                                html.P("Cette baisse en trompe-l'oeil du chômage au deuxième trimestre peut être expliquée par le 1er confinement:\
                                        en effet, des centaines de milliers de chômeurs n'avaient pu effectuer leurs démarches et n'avaient donc pas été comptabilisés,\
                                        Plus généralement, il convient de noter que les statistiques du chômage ne rendent pas compte de la totalité du sous-emploi causé par la COVID-19, \
                                        étant donné que certaines personnes « pas en emploi » peuvent être comptées comme étant « hors de la population active » parce qu’en raison de la pandémie, \
                                        elles n’étaient pas en mesure de chercher un emploi activement ou bien n’étaient pas disponibles pour travailler (garde des enfants...)."),
                                html.P("De plus, Les mesures mises en place par les administrations nationales pour réduire la propagation du Coronavirus peuvent avoir\
                                        un impact sur la capacité à conduire des enquêtes sur le terrain, et donc, sur la qualité des statistiques produites généralement."),
                                    ]),
                            ]),
                        id="collapse",
                        ),
                    ], style={'margin-right':'100px', 'margin-left': '100px', 'margin-top': '10px'})
                ], style={'display': 'inline-block', 'width': '83%'}), 
            inputs  
            ], className = 'bloc_page')


# Callback
@app.callback(
    Output('graph_chomage', 'figure'),
    Output('graph_chomage_sexe', 'figure'),
    [Input('selection_pays', 'value')],
    [Input('selection_fond', 'value')],
    [Input('selection_frequence', 'value')])
def update_figure(selected_country, selected_font, selected_frequency):
    
    # Création de la figure 1
    fig1 = go.Figure()

    for country_font in selected_font:
        fig1.add_trace(go.Scatter(
                    x = chomage[(chomage.LOCATION==country_font) & (chomage.FREQUENCY== selected_frequency) & (chomage.SUBJECT== 'TOT')].TIME,
                    y = chomage[(chomage.LOCATION==country_font) & (chomage.FREQUENCY== selected_frequency) & (chomage.SUBJECT== 'TOT')].Value,
                    mode = "lines",
                    name = country_font,
                    line=dict(width=1))) 

    fig1.add_trace(go.Scatter(
                    x = chomage[(chomage.LOCATION==selected_country) & (chomage.FREQUENCY== selected_frequency) & (chomage.SUBJECT== 'TOT')].TIME,
                    y = chomage[(chomage.LOCATION==selected_country) & (chomage.FREQUENCY== selected_frequency) & (chomage.SUBJECT== 'TOT')].Value,
                    mode = "lines",
                    name = selected_country,
                    line=dict(width=3))) 

    fig1.update_layout(title = 'Taux de chômage',
              xaxis = dict(title = 'Time', ticklen=5, zeroline=False),
              yaxis = dict(title = 'Taux de chômage', ticklen=5, zeroline=False)
              )
    fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',title_font_color="white",font_color='white',legend_title_font_color='white',font=dict(size=14))
    
    
    
    
    # Création de la figure 2
    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
                    x = chomage[(chomage.LOCATION==selected_country) & (chomage.FREQUENCY== selected_frequency) & (chomage.SUBJECT== 'MEN')].TIME,
                    y = chomage[(chomage.LOCATION==selected_country) & (chomage.FREQUENCY== selected_frequency) & (chomage.SUBJECT== 'MEN')].Value,
                    mode = "lines",
                    name = 'Femmes',
                    line=dict(width=3))) 
    fig2.add_trace(go.Scatter(
                    x = chomage[(chomage.LOCATION==selected_country) & (chomage.FREQUENCY== selected_frequency) & (chomage.SUBJECT== 'WOMEN')].TIME,
                    y = chomage[(chomage.LOCATION==selected_country) & (chomage.FREQUENCY== selected_frequency) & (chomage.SUBJECT== 'WOMEN')].Value,
                    mode = "lines",
                    name = 'Hommes',
                    line=dict(width=3))) 

    fig2.update_layout(title = 'Taux de chômage par sexe',
              xaxis = dict(title = 'Time', ticklen=5, zeroline=False),
              yaxis = dict(title = 'Taux de chômage', ticklen=5, zeroline=False)
              )
    fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',title_font_color="white",font_color='white',legend_title_font_color='white',font=dict(size=14))
    
    
    return fig1, fig2


@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [Input("collapse", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open



