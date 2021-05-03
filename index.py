import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import pib_app, emplois_app, covid_app, importations_app, HID_app


# Affichage sur l'écran
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Affichage de l'index
index_page = html.Div([
    html.H1("Bienvenue !!!"),
    dcc.Link('Voir les stats sur le Pib', href='/apps/pib'),
    html.Br(),
    dcc.Link('Voir les stats sur le COVID', href='/apps/covid'),
    html.Br(),
    dcc.Link('Voir les stats sur les données échanges internationaux', href='/apps/importations'),
    html.Br(),
    dcc.Link('Voir les stats sur l\'emploi', href='/apps/emplois'),
    html.Br(),
    dcc.Link('Voir les stats sur l\'Indice de Développement Humain', href='/apps/HID'),
])


# Fonction qui gère le passage d'une page à une autre
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/apps/pib':
        return pib_app.layout
    elif pathname == '/apps/emplois':
        return emplois_app.layout
    elif pathname == '/apps/covid':
        return covid_app.layout
    elif pathname == '/apps/importations':
        return importations_app.layout
    elif pathname == '/apps/HID':
        return HID_app.layout
    else:
        return index_page


# Lancement de l'application
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
    
    
    