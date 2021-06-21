# -*- coding: utf-8 -*-
"""
Created on Sun May  9 14:42:48 2021

"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

# Page a propos
layout = dbc.Jumbotron(
    [
        html.H1("A propos", className="display-3"),
        html.P(
            "Le but de ce dashboard est de mettre en"
             " scène des données permettant d'évaluer l'impact"
             " de la pandémie Covid-19 sur l'économie mondiale.",
            
            className="lead",
        ),
        html.Hr(className="my-2"),
        html.P(
            "Ce projet a été réalisé dans le cadre du cours de"
            " visualisation de données de la"
           " formation centrale digital-lab"
        ),
        html.P(dbc.NavLink( dbc.Button("Page de la formation", color="primary", id='learn_more_button'), 
                           href='https://formation.centrale-marseille.fr/fr/centraledigitallab-laplateforme',
                           target="_blank",
                           style={'display': 'inline-block', 'padding': '0px'}), 
               className="lead"),
    ],
)


    