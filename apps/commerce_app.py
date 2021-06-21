# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 16:27:41 2021

"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
import plotly.graph_objs as go
import pandas as pd
import dash_bootstrap_components as dbc


# Gestion des données
echanges = pd.read_csv("data/echanges_internationaux.csv")

echanges = echanges[['SUBJECT','LOCATION','FREQUENCY', 'MEASURE', 'TIME','Value']].\
                    loc[echanges.TIME>='2007',:]

available_countries = echanges['LOCATION'].unique()

# Layout
layout = html.Div([

                html.Div([
                    dcc.Dropdown(
                    id='selection_pays',
                    options=[{'label': i, 'value': i} for i in available_countries],
                    #value=['France', 'United States', 'Japan', 'India'],
                    value=['FRA', 'USA', 'CHN', 'IND'],
                    multi=True,
                    clearable=False
                    )],
                    style={'width': '15%', 'display': 'inline-block', 'margin-right': '20px'}),
                
                html.Div([
                    dcc.Dropdown(
                    id='selection_fond',
                    options=[{'label': i, 'value': i} for i in available_countries],
                    #value=['G7', 'United States', 'OECD - Total', 'Euro area (19 countries)'],
                    value=['G-7', 'G-20', 'OECD', 'EA19'],
                    multi=True
                    )], 
                    style={'width': '15%', 'display': 'inline-block'}),
                
                html.Div([
                    dcc.RadioItems(
                        id='selection_mesure',
                        options=[{'label': 'Variation période précédente', 'value': 'PC_CHGPP'}, 
                                 {'label': 'Milliards de dollars', 'value': 'BLN_USD'}],
                        value='PC_CHGPP',
                        labelStyle={'margin-left':'10px', 'cursor': 'pointer'}
                        ),
                    
                    dcc.RadioItems(
                        id='selection_frequence',
                        options=[{'label': 'Par trimestre', 'value': 'Q'}, 
                                 {'label': 'Par mois', 'value': 'M'}],
                        value='Q',
                        labelStyle={'margin-left':'10px', 'cursor': 'pointer'}
                        ),
                   
                   dcc.RadioItems(
                        id='selection_types_imports',
                        options=[{'label': 'Importations', 'value': 'IMP'}, 
                                 {'label': 'Exportations', 'value': 'EXP'},
                                 {'label': 'Solde commercial', 'value': 'NTRADE'}],
                        value='IMP',
                        labelStyle={'margin-left':'10px', 'cursor': 'pointer'}
                        )
                    ],
                    className = 'block_boutons_radios',
                    style={'width': '30%', 'display': 'inline-block', 'color': 'white', 'margin': '10px'}),
     html.Div([
                dcc.Graph(id='importations_graph1', style={'width': '45%', 'height': '350px', 'display': 'inline-block', 'margin-right': '30px'}),
                dcc.Graph(id='importations_graph2', style={'width': '45%', 'height': '350px', 'display': 'inline-block'}),
                dcc.Graph(id='importations_graph3', style={'width': '45%', 'height': '350px', 'display': 'inline-block', 'margin-right': '30px'}),
                dcc.Graph(id='importations_graph4', style={'width': '45%', 'height': '350px', 'display': 'inline-block'}),
          ], style={'text-align': 'center'},
             className = 'graphs'),
              
        html.Div([
                    dbc.Button(
                        "Interprétation",
                        id="collapse-button_commerce",
                        className="mb-3",
                        color="primary",
                        ),
                    dbc.Collapse(
                        dbc.Card([
                            dbc.CardHeader("Interprétation"),
                            dbc.CardBody([
                                html.P("Ce graphique permet de mettre en évidence l'impact du covid sur les échanges internationnaux."),
                                html.P("On peut remarquer que le premier confinement a entrainé un important déclin du commerce internationnal.\
                                         En effet, les mesures COVID 19 introduites dans la plupart des pays ont fait chuter le commerce des marchandises du G20 au deuxième trimestre 2020 de près de 18% pour les exportations et de 17% pour \
                                         les importations par rapport au premier trimestre 2020. Ceci constitue la plus forte baisse depuis la crise financière des subprimes de 2009. Les données mensuelles montrent que l'effondrement du commerce\
                                         s'est produit en avril 2020, lorsque la plupart des pays ont mis en place des mesures de confinement COVID 19 strictes. La France a vu ses exportations et importations diminuer respectivement de 29% et 20%.\
                                         On remarque également que la Chine a été la seule économie du G20 à enregistrer une croissance des exportations au deuxième trimestre 2020 (en hausse de 9.1%), après une baisse de 9.3% au premier trimestre."),
                                html.P("On observe ensuite un fort rebond du commerce international de marchandises du G20 au troisieme trimestre 2020. En France, les exportations et importations ont respectivement augmentées de 36% et 31% par rapport à la période précédente.\
                                         Parmi les économies du G20, seule la Chine a vu ses échanges commerciaux se redresser au point d’atteindre des niveaux supérieurs à ceux d\'avant la pandémie, le commerce des équipements d\'EPI (équipement de\
                                         protection individuelle), ayant contribué à porter les exportations chinoises à un niveau record au troisième trimestre 2020."),
                                html.P("Ce rebond du commerce international lors du troisième trimestre 2020 est confirmé le trimestre suivant même si ce dernier perd en amplitude par rapport à la periode précédente.")
                                    ]),
                            ]),
                        id="collapse_commerce",
                        ),
                    ], style={'margin-right':'100px', 'margin-left': '100px', 'margin-top': '10px'})
             
        ], className = 'bloc_page')


# Callback
@app.callback(
    Output('importations_graph1', 'figure'),
    Output('importations_graph2', 'figure'),
    Output('importations_graph3', 'figure'),
    Output('importations_graph4', 'figure'),
    [Input('selection_pays', 'value')],
    [Input('selection_fond', 'value')],
    [Input('selection_mesure', 'value')],
    [Input('selection_frequence', 'value')],
    [Input('selection_types_imports', 'value')])
def update_figure(selected_country, selected_font, selected_measure, selected_frequency, selected_subject):
    
    # Création de la trame 1
    if selected_subject == 'EXP':
        titlee = "Exportations des biens"
    elif selected_subject == 'IMP':
        titlee = "Importations des biens"
    elif selected_subject == 'NTRADE':
        titlee = "Solde commercial des biens"

    if selected_measure == 'PC_CHGPP':
        legende = 'Variation periode precedente'
    elif selected_measure == 'BLN_USD':
        legende = "Milliards de $"
        
    fig=[go.Figure(), go.Figure(), go.Figure(), go.Figure()]

        
    for i in range(len(selected_country)):
        for pays_font in selected_font:
            fig[i].add_trace(go.Scatter(
                    x = echanges[(echanges.LOCATION==pays_font) & (echanges.FREQUENCY== selected_frequency) & (echanges.SUBJECT== selected_subject) & (echanges.MEASURE==selected_measure)].TIME,
                    y = echanges[(echanges.LOCATION==pays_font) & (echanges.FREQUENCY== selected_frequency) & (echanges.SUBJECT== selected_subject) & (echanges.MEASURE==selected_measure)].Value,
                    mode = "lines",
                    name = pays_font,
                    line=dict(width=1)))
            
        fig[i].add_trace(go.Scatter(
                    x = echanges[(echanges.LOCATION==selected_country[i]) & (echanges.FREQUENCY== selected_frequency) & (echanges.SUBJECT== selected_subject) & (echanges.MEASURE==selected_measure)].TIME,
                    y = echanges[(echanges.LOCATION==selected_country[i]) & (echanges.FREQUENCY== selected_frequency) & (echanges.SUBJECT== selected_subject) & (echanges.MEASURE==selected_measure)].Value,
                    mode = "lines",
                    name = selected_country[i],
                    line=dict(width=2)))


        fig[i].update_layout(title = str(titlee) + ' pour ' + selected_country[i],
              xaxis = dict(title='Time', ticklen=5, zeroline=False),
              yaxis = dict(title=str(legende), ticklen=0.5, zeroline=False)
              )

        fig[i].update_layout(paper_bgcolor='rgba(0,0,0,0)',
                             plot_bgcolor='rgba(0,0,0,0)',title_font_color="white",font_color='white',legend_title_font_color='white',font=dict(size=14))
    
    return fig[0], fig[1], fig[2], fig[3]


@app.callback(
    Output("collapse_commerce", "is_open"),
    [Input("collapse-button_commerce", "n_clicks")],
    [Input("collapse_commerce", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open