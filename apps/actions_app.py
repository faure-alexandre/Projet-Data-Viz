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
import dash_bootstrap_components as dbc

# Gestion des donnees
df_actions = pd.read_csv("data/actions.csv")

df_actions = df_actions.loc[:,['LOCATION', 'TIME', 'FREQUENCY', 'Value']]

available_countries = df_actions['LOCATION'].unique()

bitcoin = pd.read_csv("data/Bitcoin.csv")
bitcoin['Date'] = pd.to_datetime(bitcoin['Date'], format='%d-%m-%Y')

ethereum = pd.read_csv("data/Ethereum.csv")
ethereum['Date'] = pd.to_datetime(ethereum['Date'], format='%d-%m-%Y')

gold = pd.read_csv("data/Gold.csv")
gold['ds'] = pd.to_datetime(gold['ds'], format='%Y-%m-%d')


# Creation des figures pour les cryptos-monnaies
fig_bitcoin = go.Figure()

fig_bitcoin.add_trace(go.Scatter(
                    x=bitcoin.Date,
                    y=bitcoin.Open,
                    text='Cours Bitcoin',
                    mode='lines',
                    fill='tozeroy'
                ) )
fig_bitcoin.update_layout(
                title='Cours Bitcoin',
                xaxis={'title': 'Time'},  
                yaxis={'title': 'Prix (en $)'},
                legend={'x': 0.0, 'y': 1},
                hovermode='closest')
fig_bitcoin.update_layout(paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',title_font_color="white",font_color='white',legend_title_font_color='white',font=dict(size=14))


fig_ether = go.Figure()

fig_ether.add_trace(go.Scatter(
                    x=ethereum.Date,
                    y=ethereum.Open,
                    text='Cours Ether',
                    mode='lines',
                    fill='tozeroy'
                ) )
fig_ether.update_layout(
                title='Cours Ether',
                xaxis={'title': 'Time'},  
                yaxis={'title': 'Prix (en $)'},
                legend={'x': 0.0, 'y': 1},
                hovermode='closest')
fig_ether.update_layout(paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',title_font_color="white",font_color='white',legend_title_font_color='white',font=dict(size=14))

fig_gold = go.Figure()

fig_gold.add_trace(go.Scatter(
                    x=gold.ds,
                    y=gold.y,
                    text='Cours Or',
                    mode='lines',
                    fill='tozeroy'
                ) )
fig_gold.update_layout(
                title='Cours Or',
                xaxis={'title': 'Time'},  
                yaxis={'title': 'Prix (en $)'},
                legend={'x': 0.0, 'y': 1},
                hovermode='closest')
fig_gold.update_layout(paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',title_font_color="white",font_color='white',legend_title_font_color='white',font=dict(size=14))



# Layout
layout = html.Div([
              html.Div([
                
                    dcc.Dropdown(
                    id='selection_pays',
                    options=[{'label': i, 'value': i} for i in available_countries],
                    value=[],
                    multi=True,
                    placeholder="Selectionnez un pays",
                    )],
                    style={'width': '10%', 'display': 'inline-block'}),
                
                html.Div([
                    dbc.RadioItems(
                        id='selection_frequence',
                        options=[{'label': 'Par année', 'value': 'A'},
                                 {'label': 'Par trimestre', 'value': 'Q'}, 
                                 {'label': 'Par mois', 'value': 'M'}],
                        value='M',
                        labelStyle={'margin-left':'10px', 'cursor': 'pointer'}
                        )
                    ],
                    className = 'block_boutons_radios',
                    style={'margin': '10px', 'display': 'inline-block', 'color': 'white', 
                           }),
                html.Div([
                  dcc.RangeSlider(
                                  min=1950,
                                  max=2022,
                                  value=[2000, 2022],
                                  marks={
                                      1950: {'label': '1950', 'style': {'color': '#77b0b1'}},
                                      2000: {'label': '2000', 'style': {'color': '#f50'}},
                                      2008: {'label': '2008', 'style': {'color': '#f50'}},
                                      2022: {'label': '2021', 'style': {'color': '#f50'}}
                                      },
                                  id='selection_date'
                                  ),  
                  ],
                    className = 'slider',
                    style={'width': '30%', 'display': 'inline-block', 'margin-left': '15px'}),
    html.Div([
                dcc.Graph(id='actions_graph', style={'width': '90%', 'height': '40%', 'display': 'inline-block'}),
             
            ], style={'text-align': 'center'},
             className = '1er_graph'),
    
    html.Div([
        dcc.Graph(figure=fig_bitcoin, id='crypto_graph', style={'width': '30%', 'height': '30%', 'display': 'inline-block'}),
        dcc.Graph(figure=fig_ether, id='crypto_graph2', style={'width': '30%', 'height': '30%', 'display': 'inline-block'}),
        dcc.Graph(figure=fig_gold, id='crypto_graph3', style={'width': '30%', 'height': '30%', 'display': 'inline-block'}),   
        ], style={'text-align': 'center', 'margin-top': '5px'},
             className = 'crypto_graphs'),
    
    
    html.Div([
                    dbc.Button(
                        "Interprétation",
                        id="collapse-button_actions",
                        className="mb-3",
                        color="primary",
                        ),
                    dbc.Collapse(
                        dbc.Card([
                            dbc.CardHeader("Interprétation"),
                            dbc.CardBody([
                                html.P("Ce graphique permet de mettre en évidence l'impact du covid sur le cours des marchés nationaux."),
                                html.P("Le graphique du haut montre l’évolution du prix des actions en se basant sur la moyenne de l’année 2015 ie année 2015 = 100%)"),
                                html.P("On peut observer que durant les mois de mars et avril 2020, la crise sanitaire du coronavirus a déclenché une série de krachs qui ont affecté simultanément toutes les bourses mondiales.\
                                       Les chocs se sont avérés plus ou moins marqués. Moins forts en Chine, ils l'ont été bien davantage dans des pays comme l'Italie ou l'Espagne.\
                                       Pour les principales économies, États-Unis, Japon, Royaume-Uni ou pays de l'Union européenne, la chute des cours au printemps 2020 s'est montrée violente et\
                                       figure même parmi les plus grands évènements boursiers de ce début de XXIe siècle (à savoir l’explosion de la bulle internet en 2001-2002 et les subprimes en 2008-2009)."),
                                html.P("Si on prend le cas des Etats-Unis, l’amplitude de la variation est similaire à celle des crises de 2008 et 2001.\
                                       Deux différences apparaissent cependant: si les courbes ont décru avec un même ordre de grandeur, la baisse est intervenue cette fois avec beaucoup plus de brutalité.\
                                       Elle s'est réalisée en à peine quelques semaines alors que la chute s'était étalée sur plus de 8 mois lors de la grande crise financière et sur plus d'un an pour l'explosion de la bulle Internet.\
                                       Deuxième différence, la remontée des cours a suivi presque aussi brutalement (un peu moins rapidement en Europe). En effet, on remarque que la plupart des bourses nationales sont revenus à l’équilibre\
                                       courant novembre 2020 avant de continuer à  connaitre de fortes hausses probablement dues aux annonces faites sur les vaccins."),
                                html.P("On remarque de plus que le cours des crypto-monnaies, comme la plupart des actions à la mi-mars, a été influencé \
                                         par l'impact de la crise. En effet, le Bitcoin a fortement plongé au début de la crise sanitaire. \
                                         En quelques heures, son cours est passé de 8 000 $ à environ 5 000 $, soit une baisse d'environ 38 %.\
                                         Il est bon de noter que le cours du Bitcoin s’est rapidement relevé. En effet, après ce choc, \
                                         le cours n’a cessé d’augmenter enregistrant ainsi des performances journalières comprises entre 8 et 16 %. Fin juillet, \
                                         le cours du Bitcoin progresse ainsi rapidement dépassant la barre des 9 000 $, longtemps considérée comme une valeur de résistance. \
                                         Le 20 décembre 2020, il atteint les 24 000 $, dépassant largement son précédent record de décembre 2017 avant de s'envoler jusqu'à courant Avril aux alentours de 60 000 $.\
                                         Les performances du Bitcoin pendant la crise pourraient s'expliquer par le spectre du retour de l’inflation (du fait que les banques centrales créent beaucoup de monnaie pour pallier à la crise).\
                                         Face à la dévaluation des monnaies, conséquence directe de l’inflation,\
                                         le Bitcoin s’est affirmé comme une solution pour « protéger son argent »."),
                                html.P("Cependant, le cours des crypto-monnaies et des actions sont influencés par un tas d'autres facteurs externes et on peut se demander si ils constituent un bon indicateur\
                                         au vu de leur volatilité et de l'influence que peuvent avoir certaines personnalités sur leur évolution..."),     
                                         
                                    ]),
                            ]),
                        #is_open = True,
                        id="collapse_actions",
                        ),
                    ], style={'margin-right':'100px', 'margin-left': '100px', 'margin-top': '10px'})
                                         
        ], className = 'bloc_page')


# Callback
@app.callback(
    Output('actions_graph', 'figure'),
    [Input('selection_pays', 'value')],
    [Input('selection_frequence', 'value')],
    [Input('selection_date', 'value')])
def update_figure(selected_country, selected_frequency, selected_time):
    
    time_min = str(selected_time[0]) 
    time_max = str(selected_time[1]) 
    
    fig1=go.Figure()
    
    if selected_country == []:
        for pays in available_countries:
            fig1.add_trace(go.Scatter(
                    x = df_actions.TIME[(df_actions.LOCATION==pays) & (df_actions.FREQUENCY== selected_frequency) & (df_actions.TIME > time_min) & (df_actions.TIME < time_max)],
                    y = df_actions.Value[(df_actions.LOCATION==pays) & (df_actions.FREQUENCY== selected_frequency) & (df_actions.TIME > time_min) & (df_actions.TIME < time_max)],
                    mode = "lines",
                    name = str(pays),
                    line=dict(width=1.5)))
        
    else:
        
        for pays in selected_country:
            df_filter = df_actions[(df_actions.LOCATION== pays) & (df_actions.FREQUENCY== selected_frequency) & (df_actions.TIME > time_min) & (df_actions.TIME < time_max)]
            fig1.add_trace(go.Scatter(
                    x = df_filter.TIME,
                    y = df_filter.Value,
                    mode = "lines",
                    name = str(pays),
                    line=dict(width=3)))


    fig1.update_layout(title = 'Cours des marchés nationaux',
              xaxis = dict(title='Time', ticklen=5, zeroline=False),
              yaxis = dict(title='Evolution du prix des actions',ticklen=5, zeroline=False)
              )

    fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',title_font_color="white",font_color='white',legend_title_font_color='white',font=dict(size=14))
    
    return fig1


@app.callback(
    Output("collapse_actions", "is_open"),
    [Input("collapse-button_actions", "n_clicks")],
    [Input("collapse_actions", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
