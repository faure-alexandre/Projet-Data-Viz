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
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc

# Gestion des données
donnees_covid = pd.read_csv("data/donnees_covid.csv")

stats_pays = donnees_covid[['location','human_development_index', 'gdp_per_capita', 
                            'population','life_expectancy','stringency_index', 'continent']].groupby(by='location', as_index=False).agg(np.max)

donnees_covid = donnees_covid[['total_cases','total_deaths','location',
                               'date','continent','total_vaccinations','total_tests']]
df = donnees_covid.groupby(by='continent', as_index=False).agg(np.max)

available_countries = donnees_covid['location'].unique()



# Layout
layout = html.Div([
              html.Div([
                html.Div([
                    #html.H5(['Sélectionnez un pays: '], style={'width': '70%'}),
                    dcc.Dropdown(
                    id='selection_pays',
                    options=[{'label': i, 'value': i} for i in available_countries],
                    value='France',
                    style={'width': '75%'},
                    placeholder="Sélectionnez un pays:")],
                    style={'display': 'flex','width': '65%', 'margin': '15px'}
                    ),
    
                   dcc.Graph(id='covid_death_graph', style={'width': '800px', 'height': '400px','display': 'inline-block'}),  #, 'opacity': '0.9'
                   ], style={'width': '40%','margin-top': '40px', 'margin-left': '10px','display': 'inline-block'},
                   className = '1er_graph'), 
              
              html.Div([
                  dcc.Graph(id='pie', style={'width': '550px', 'height': '400px', 'opacity': '0.9'}),
                  ], style={'width': '30%','margin-top': '50px', 'margin-left': '300px','display': 'inline-block'},
                   className = '2eme_graph'),
              
              html.Div([
              html.Div([
                   dcc.Graph(id='vaccination_graph', style={'width': '1000px', 'height': '350px','display': 'inline-block', 'opacity': '0.9'}),
                   ], style={'width': '45%','margin-top': '25px', 'margin-left': '10px','display': 'inline-block'},
                   className = '3eme_graph'), 
              
              html.Div([
                  dbc.Table([
                      html.Tbody([html.Tr([html.Td('Indice de developpement'), html.Td(id='HDI')]),
                      html.Tr([html.Td('PIB'), html.Td(id='gdp')]),
                      html.Tr([html.Td('Population'), html.Td(id='pop')]),
                      html.Tr([html.Td('Espérance de vie'), html.Td(id='life_exp')]),
                      html.Tr([html.Td('Indice de confinement'), html.Td(id='ind_conf')])]),
                     ],bordered=True,
                      dark=True,
                      hover=True,
                      responsive=True,
                      striped=True),
                  ], style={'width': '30%','height': '30%','margin': 'auto', 'margin-left': '300px','display': 'inline-block',
                             'textAlign': 'center','font-size':'150%',
                            'vertical-align': 'bottom'},
                   className = 'stats_pays'),
              ], className = 'bloc_bas', style={'display': 'flex'})  ,            
        ], className = 'bloc_page')


                            
# Callbacks
@app.callback(
    Output('covid_death_graph', 'figure'),
    Output('pie', 'figure'),
    Output('vaccination_graph', 'figure'),
    [Input('selection_pays', 'value')])
def update_figure(selected_country):
    
    donnees_covid_filter = donnees_covid[donnees_covid.location == selected_country]
    # Création de la trame 1
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
                    x = donnees_covid_filter.date,
                    y = donnees_covid_filter.total_deaths,
                    mode = "lines",
                    name = "citations",
                    marker = dict(color = 'red'),
                    line = dict(width=4))) #rgba(16, 112, 2, 0.8)


    
    fig1.update_layout(title = 'Nombre de morts du COVID par pays',
              xaxis = dict(title = 'Time',ticklen =5,zeroline= False),
              yaxis = dict(title = 'Morts',ticklen =5,zeroline= False))

    fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',title_font_color="white",font_color='white',legend_title_font_color='white',font=dict(size=14))
    
    
    fig2 = go.Figure()
    fig2.add_trace( go.Bar(
                    x = donnees_covid_filter.date,
                    y = donnees_covid_filter.total_vaccinations,
                    name = "citations",
                    marker = dict(color = 'red'))) #'rgba(16, 112, 2, 0.8)'

    fig2.update_layout(title = 'Nombre de vaccinations',
              xaxis = dict(title = 'Time',ticklen =5,zeroline= False),
              yaxis = dict(title = 'Nb personnes vaccinées',ticklen =5,zeroline= False)
              )

    fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',title_font_color="white",font_color='white',legend_title_font_color='white',font=dict(size=14))
    
    
    cont = str(stats_pays.continent[stats_pays.location == selected_country].values[0])
    pl = np.zeros((df.shape[0],))
    idx = np.where(df.continent==cont)
    pl[idx]=0.15
    
    fig_chart=go.Figure()
    fig_chart.add_trace(go.Pie(
                               values = df.total_deaths,
                               labels = df.continent,
                               name = "camembert",
                               direction = 'clockwise',
                               pull = pl))

    fig_chart.update_layout(title = 'Nombre de morts du COVID par continent',paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',title_font_color="white",font_color='white',legend_title_font_color='white',font=dict(size=14))
    
    return fig1, fig_chart, fig2

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


