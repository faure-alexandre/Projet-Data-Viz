import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import pib_app, emplois_app, covid_app, importations_app, HID_app, petrol_app

import dash_bootstrap_components as dbc


# Creation de la barre de navigation
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"


liens = dbc.Row(
            [
                dbc.Col( dbc.NavItem(dbc.NavLink("Accueil", href="return")),width=100),
                dbc.Col( dbc.NavItem(dbc.NavLink("Données COVID", href="/apps/covid")),width=130),
                
                
                dbc.Col(dbc.DropdownMenu(
                    children=[
                    #dbc.DropdownMenuItem("More pages", header=True),
                    dbc.DropdownMenuItem("Echanges commerciaux", href="/apps/importations"),
                    dbc.DropdownMenuItem("PIB", href="/apps/pib"),
                    dbc.DropdownMenuItem("Emplois", href="/apps/emplois"),
                    dbc.DropdownMenuItem("HID", href="/apps/HID"),
                    dbc.DropdownMenuItem("Cours pétrole", href="/apps/petrol")
                    ],
                    nav=True,
                    in_navbar=True,
                    label="Données économiques"
                ),width=100),
                
                dbc.Col(dbc.DropdownMenu(
                    children=[
                    #dbc.DropdownMenuItem("More pages", header=True),
                    dbc.DropdownMenuItem("Sources données", header=True),
                    dbc.DropdownMenuItem("OCDE", href="https://stats.oecd.org/index.aspx?lang=fr"),
                    
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("Documentations", header=True),
                    dbc.DropdownMenuItem("Plotly", href="https://plotly.com/"),
                    dbc.DropdownMenuItem("Dash", href="https://dash.plotly.com/"),
                    
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("A propos", href="/A_propos")
                    ],
                    nav=True,
                    in_navbar=True,
                    label="A propos",
                ),width=100),
            ],
            className="ml-auto mr-0 h6 flex-row flex-nowrap justify-content-end mt-0 w-50",
            style={'width': '20px'},
             align="center",
             no_gutters=True
        )

navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                    dbc.Col(dbc.NavbarBrand(className="ml-2", id='titre_page')),
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://plot.ly",
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
        #dbc.Spinner(color="primary"), 
        liens
    ],
    color="dark",
    dark=True,
    sticky='Top',
    className="mt-2 mb-3 text-white w-100, h-25"
)



# Page a propos
about_page = dbc.Jumbotron(
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
        html.P(dbc.Button("Learn more", color="primary"), className="lead"),
    ],
)



# Affichage sur l'écran
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])

# Affichage de l'index
index_page = html.Div([
    html.H1("Bienvenue !!!"),
    dcc.Link('Les stats sur le PIB', href='/apps/pib', style={'color': '#FFFFFF'}),
    html.Br(),
    dcc.Link('Les stats sur le COVID', href='/apps/covid', style={'color': '#FFFFFF'}),
    html.Br(),
    dcc.Link('Les stats sur les données échanges internationaux', href='/apps/importations', style={'color': '#FFFFFF'}),
    html.Br(),
    dcc.Link('Les stats sur l\'emploi', href='/apps/emplois', style={'color': '#FFFFFF'}),
    html.Br(),
    dcc.Link('Les stats sur l\'Indice de Développement Humain', href='/apps/HID', style={'color': '#FFFFFF'}),
    html.Br(),
    dcc.Link('Les stats sur l\'évolution du prix du pétrole en fonction des confinements', href='/apps/petrol', style={'color': '#FFFFFF'}),
])


# Fonction qui gère le passage d'une page à une autre
@app.callback(Output('page-content', 'children'),
              Output('titre_page', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/apps/pib':
        return pib_app.layout, 'Données PIB'
    elif pathname == '/apps/emplois':
        return emplois_app.layout, 'Marché du travail'
    elif pathname == '/apps/covid':
        return covid_app.layout, 'Chiffres COVID'
    elif pathname == '/apps/importations':
        return importations_app.layout, 'Commerce international'
    elif pathname == '/apps/HID':
        return HID_app.layout, 'HID'
    elif pathname == '/apps/petrol':
        return petrol_app.layout, 'Cours du pétrole'
    elif pathname =='return':
        return index_page, 'Accueil'
    elif pathname =='/A_propos':
        return about_page, 'A propos'
    else:
        return index_page, 'Accueil'
    


# Lancement de l'application
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
    
    
    