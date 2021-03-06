# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 10:46:47 2021

"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import plotly.graph_objs as go
import pandas as pd

from app import app

df_pib = pd.read_csv("data/PIB.csv")
df_pib = df_pib[['LOCATION', 'TIME', 'Value']]

# temps = df_pib['TIME'].unique()
df = pd.read_csv("data/emploi.csv")
nom_pays = df[['LOCATION', "Pays"]].drop_duplicates()
liste_pays = nom_pays['Pays'].values.tolist()
liste_pays.sort()
df_pib = pd.merge(df_pib, nom_pays, on = "LOCATION", how = "inner")
    
# colors = {
#     'background': 'rgba(255, 255, 128, .5)',
#     'text': '#7FDBFF'
# }


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
                value=['OCDE - Total'], 
                style={'width':'50%'},
                className='row',
                multi=True
            ),
    
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
                                html.P("Ce graphique permet de mettre en évidence l'impact du covid sur le PIB des pays membres de l'OCDE."),
                                html.P("En effet, on voit très nettement une baisse du PIB au deuxième trimestre 2020, et ce pour la totalité des pays de l'OCDE.\
                                        Cette baisse du PIB est la résultante d'une baisse des activités dans de nombreux secteurs (Tourisme, hôtellerie restauration, culture,...) dû aux restrictions sanitaires tel que les confinements.\
                                        Cette baisse du PIB est aussi la conséquence de la chute des échanges commerciaux (cf la page Echanges commerciaux).\
                                        Enfin, cette baisse du PIB est aussi certainement lié à une baisse de la consommation et une réticence à embaucher et investir dans une période compliqué et les perspéctives d'un avenir incertain."),
                                html.P("Cependant, après cette chute record le PIB remonte très nettement au troisième trimestre 2020, probablement dû à une reprise d'activité et de consommation lié à la baisse des restrictions sanitaires pendant l'été,\
                                        à une reprise des échanges commerciaux,\
                                        ainsi qu'aux plans des états et de l'Europe pour relancer l'économie.\
                                        Malgrès cette remontée le PIB n'atteind pas les valeurs d'avant le covid."),
                                html.P("Si l'on compare l'impact économique du covid avec la crise financière de 2008, \
                                        on peut voir que le PIB chute plus brutalement qu'en 2008 mais qu'il remonte aussi plus rapidement.")
                                    ]),
                            ]),
                        id="collapse_actions",
                        ),
                    ], style={'margin-right':'100px', 'margin-left': '100px', 'margin-top': '10px'})
    
], className = 'bloc_page')

@app.callback(
    Output('graph_pib', 'figure'),
    [Input('selection_pays', 'value')])
def update_figure(choix_pays):
    
    fig = go.Figure()
    for pays in choix_pays:
        df_filter = df_pib[df_pib.Pays == pays]
        fig.add_trace(go.Scatter(
                    x = df_filter.TIME,
                    y = df_filter.Value,
                    mode = "lines",
                    name = pays,
                    #marker = dict(color = 'red'),   #rgba(16, 112, 2, 1)
                    line = dict(width=4)))
    



    fig.update_layout(title = 'PIB trimestriel',
              xaxis = dict(title = 'Trimestre',ticklen =5,zeroline= False),
              yaxis = dict(title = 'Indice de volume du PIB',ticklen =5,zeroline= False))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', #'rgba(7,13,64,255)',
        plot_bgcolor='rgba(0,0,0,0)',title_font_color="white",font_color='white',legend_title_font_color='white',font=dict(size=14))
    

    return fig


@app.callback(
    Output("collapse_pib", "is_open"),
    [Input("collapse-button_pib", "n_clicks")],
    [Input("collapse_actions", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open