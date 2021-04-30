# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 16:27:41 2021

@author: Alexandre
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
from app import app
import plotly.graph_objs as go
import pandas as pd


# Gestion des données
donnees_covid = pd.read_csv("data/donnees_covid.csv")

stats_pays = donnees_covid[['location','human_development_index', 'gdp_per_capita', 
                            'population','life_expectancy','stringency_index']].groupby(by='location', as_index=False).agg(np.max)

donnees_covid = donnees_covid[['total_cases','total_deaths','location',
                               'date','continent','total_vaccinations','total_tests']]
df = donnees_covid.groupby(by='continent', as_index=False).agg(np.max)

available_countries = donnees_covid['location'].unique()


# Layout
layout = html.Div([
                html.H2(
                        children="Le COVID en chiffres",
                        style={
                            'textAlign': 'center',
                            }
                    ),
    
              html.Div([
                html.Div([
                    html.H5(['Sélectionnez un pays: '], style={'width': '40%'}),
                    dcc.Dropdown(
                    id='selection_pays',
                    options=[{'label': i, 'value': i} for i in available_countries],
                    value='France',
                    style={'width': '75%'},
                    )],
                    style={'display': 'flex','width': '50%', 'margin': '15px'}),
    
                   dcc.Graph(id='covid_death_graph', style={'width': '1000px', 'height': '350px','display': 'inline-block', 'opacity': '0.9'}),
                   ], style={'width': '45%','margin-top': '40px', 'margin-left': '10px','display': 'inline-block'},
                   className = '1er_graph'), 
              
              html.Div([
                  dcc.Graph(id='pie', style={'width': '500px', 'height': '350px', 'opacity': '0.9'}, figure=
                       {'data': [
                           go.Pie(
                               values = df.total_deaths,
                               labels = df.continent,
                               name = "camembert",
                               direction = 'clockwise')  
                           ],
                       'layout' : dict(title = 'Nombre de morts du COVID par continent')
                       }
                            ),
                  ], style={'width': '35%','margin-top': '50px', 'margin-left': '300px','display': 'inline-block'},
                   className = '2eme_graph'),
              
              html.Div([
              html.Div([
                   dcc.Graph(id='vaccination_graph', style={'width': '1000px', 'height': '350px','display': 'inline-block', 'opacity': '0.9'}),
                   ], style={'width': '45%','margin-top': '25px', 'margin-left': '10px','display': 'inline-block'},
                   className = '3eme_graph'), 
              
              html.Div([
                  html.Table([
                      html.Tr([html.Td('Indice de developpement'), html.Td(id='HDI')]),
                      html.Tr([html.Td('PIB'), html.Td(id='gdp')]),
                      html.Tr([html.Td('Population'), html.Td(id='pop')]),
                      html.Tr([html.Td('Espérance de vie'), html.Td(id='life_exp')]),
                      html.Tr([html.Td('Indice de confinement'), html.Td(id='ind_conf')]),
                     ]),
                  ], style={'width': '20%','height': '50%','margin': 'auto', 'margin-left': '400px','display': 'inline-block',
                            'background-color':'white', 'textAlign': 'center','font-size':'170%',
                            'vertical-align': 'bottom', 'color': 'red', 'opacity': '0.9'},
                   className = 'stats_pays'),
              ], className = 'bloc_bas', style={'display': 'flex'})  ,            
        ], className = 'bloc_page')


                            
# Callbacks
@app.callback(
    Output('covid_death_graph', 'figure'),
    Output('vaccination_graph', 'figure'),
    [Input('selection_pays', 'value')])
def update_figure(selected_country):
    
    donnees_covid_filter = donnees_covid[donnees_covid.location == selected_country]
    # Création de la trame 1
    trace1 = go.Scatter(
                    x = donnees_covid_filter.date,
                    y = donnees_covid_filter.total_deaths,
                    mode = "lines",
                    name = "citations",
                    marker = dict(color = 'rgba(16, 112, 2, 0.8)')) 


    data = [trace1]
    layout = dict(title = 'Nombre de morts du COVID par pays',
              xaxis = dict(title = 'Time',ticklen =5,zeroline= False),
              yaxis = dict(title = 'Morts',ticklen =5,zeroline= False)
              )
    fig1 = dict(data = data, layout = layout)
    
    trace2 = go.Bar(
                    x = donnees_covid_filter.date,
                    y = donnees_covid_filter.total_vaccinations,
                    name = "citations",
                    marker = dict(color = 'rgba(16, 112, 2, 0.8)')) 


    data2 = [trace2]
    layout2 = dict(title = 'Nombre de vaccinations',
              xaxis = dict(title = 'Time',ticklen =5,zeroline= False),
              yaxis = dict(title = 'Nb personnes vaccinées',ticklen =5,zeroline= False)
              )
    fig2 = dict(data = data2, layout = layout2)

    return fig1, fig2

@app.callback(
    Output('HDI', 'children'),
    Output('gdp', 'children'),
    Output('pop', 'children'),
    Output('life_exp', 'children'),
    Output('ind_conf', 'children'),
    [Input('selection_pays', 'value')])
def callback_tableau(x):
    hdi = stats_pays.human_development_index[stats_pays.location == x]
    gdp = stats_pays.gdp_per_capita[stats_pays.location == x]
    pop = stats_pays.population[stats_pays.location == x]
    life_exp = stats_pays.life_expectancy[stats_pays.location == x]
    ind_conf = stats_pays.stringency_index[stats_pays.location == x]
    
    return float(hdi), float(gdp), float(pop), float(life_exp), float(ind_conf)


