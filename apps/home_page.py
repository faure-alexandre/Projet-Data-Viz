# -*- coding: utf-8 -*-
"""
Created on Fri May 14 12:01:41 2021

"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


layout = html.Div([
    
    html.Div([
        
        html.H1('Bienvenue !!!'),
        html.P('Le but de ce dashboard est de mettre en'\
             ' scène des données permettant d\'évaluer l\'impact'\
             ' de la pandémie Covid-19 sur l\'économie mondiale.')
    
    ], className='abstract'),
        
    html.Div([
        html.Div([
            html.H2('Déroulement du projet'),
            html.P(['Nous avons dans un premier temps essayé de faire une première '\
                   'analyse sur le jeu de données fournit avec le sujet (disponible ',
                   html.A('ici', href='https://data.mendeley.com/datasets/b2wvnbnpj9/1', target='_blank'),
                   '). Il s\'est cependant avéré que ce dataset était assez limité de' \
                   ' part le fait qu\'il ne disposait que d\'un seul indicateur'\
                   ' économique (le PIB) et que ce dernier était fixe pour chaque'\
                   ' pays car il n\'est mis à jour qu\'une fois par an.'\
                   ' La fenêtre d\'observation était également trop courte (du 31/12/2019 au 19/10/2020) pour pouvoir appréhender à long terme les effets de la crise.']),
            html.P(['Nous avons donc décidé de rechercher d\'autres sources de données'\
                    ' et nous avons trouvé un dataset (disponible ',
                    html.A('ici', href='https://github.com/owid/covid-19-data/tree/master/public/data', target='_blank'),
                    ') mis à jour quotidiennement et contenant de nombreuses informations'\
                    ' relatives à la progression de la pandémie ainsi que des données'\
                    ' démographiques et de développement relatives à chaque pays (tableau récapitulatif'\
                    ' de toutes les variables disponible ',
                    html.A('ici', href='https://github.com/owid/covid-19-data/blob/master/public/data/owid-covid-codebook.csv', target='_blank'),
                    ').']),
            html.P(['Il nous a fallu dans un second temps trouver des données permettant'\
                    ' de mesurer l\'impact économique de la crise. Nous nous sommes pour'\
                    ' cela appuyé sur les nombreux datasets disponibles sur le site de'\
                    ' l\'OCDE (voir ',
                    html.A('ici', href='https://stats.oecd.org/index.aspx?lang=fr', target='_blank'),
                    ') en choisissant différents indicateurs ainsi que certains datasets disponibles sur Kaggle.'])

           ], className='deroulement_projet'),  
            
        html.Div([ 
            html.H2('Plan du dashboard'),
            html.Ul([
                html.Li([dcc.Link('Données covid', href='/apps/covid', style={'color': '#FFFFFF'}),
                        ': page contenant quelques graphiques relatifs à'\
                        ' l\'évolution de l\'épidemie.']),
                html.Li([dcc.Link('PIB', href='/apps/pib', style={'color': '#FFFFFF'}),
                         ': page permettant de mesurer l\'impact de la crise sur l\'évolution du PIB.']), 
                html.Li([dcc.Link('Commerce', href='/apps/commerce', style={'color': '#FFFFFF'}),
                         ': page permettant de mesurer l\'impact de la crise sur les échanges internationaux (exportations, importations).']), 
                html.Li([dcc.Link('HDI', href='/apps/HID', style={'color': '#FFFFFF'}),
                         ': page permettant de mesurer l\'impact de la crise en fonction du développement des pays.']), 
                html.Li([dcc.Link('Cours actions', href='/apps/actions', style={'color': '#FFFFFF'}),
                         ': page permettant de mesurer l\'impact de la crise sur le cours des actions.']), 
                html.Li([dcc.Link('Cours pétrole', href='/apps/petrol', style={'color': '#FFFFFF'}),
                         ': page permettant de mesurer l\'impact de la crise sur l\'évolution des prix du pétrole.']),
                html.Li([dcc.Link('Emplois', href='/apps/travail', style={'color': '#FFFFFF'}),
                         ': page permettant de mesurer l\'impact de la crise sur la situation du marché de l\'emploi.']), 
            
                ]),
             html.P(['Chaque page du Dashboard contient tout en bas un bouton \'Interprétation\' permettant de faire une analyse synthétique des graphiques présentés',
                     html.Br(), 'afin de mettre en avant leur pertinence vis-à-vis de la problématique ainsi que leurs limitations.'])
            ], className='plan_dashboard'),
    ], className='conteneur_flex'),    
 ], className='accueil'
)


 