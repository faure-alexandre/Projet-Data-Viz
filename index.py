import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import pib_app, travail_app, covid_app, commerce_app, HID_app,\
                petrol_app, actions_app, about_page, home_page

import dash_bootstrap_components as dbc


# Creation de la barre de navigation
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"


liens = dbc.Nav(
            [
                dbc.NavLink("Accueil", href="return", external_link=True),
                dbc.NavLink("Données COVID", href="/apps/covid", external_link=True),
                
                
                dbc.DropdownMenu(
                    children=[
                    dbc.DropdownMenuItem("Echanges commerciaux", href="/apps/commerce", external_link=True),
                    dbc.DropdownMenuItem("PIB", href="/apps/pib", external_link=True),
                    dbc.DropdownMenuItem("Emplois", href="/apps/travail", external_link=True),
                    dbc.DropdownMenuItem("HDI", href="/apps/HID", external_link=True),
                    dbc.DropdownMenuItem("Cours pétrole", href="/apps/petrol", external_link=True),
                    dbc.DropdownMenuItem("Cours actions", href="/apps/actions", external_link=True)
                    ],
                    nav=True,
                    in_navbar=True,
                    label="Données économiques"
                ),
                
                dbc.DropdownMenu(
                    children=[
                    #dbc.DropdownMenuItem("More pages", header=True),
                    dbc.DropdownMenuItem("Sources données", header=True),
                    dbc.DropdownMenuItem("OCDE", href="https://stats.oecd.org/index.aspx?lang=fr", target="_blank"),
                    dbc.DropdownMenuItem("Données Covid", href="https://github.com/owid/covid-19-data/tree/master/public/data", target="_blank"),
                    dbc.DropdownMenuItem("Datasets Kaggle", href="https://www.kaggle.com/datasets", target="_blank"),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("Documentations", header=True),
                    dbc.DropdownMenuItem("Plotly", href="https://plotly.com/", target="_blank"),
                    dbc.DropdownMenuItem("Dash", href="https://dash.plotly.com/", target="_blank"),
                    dbc.DropdownMenuItem("Dash Bootstrap", href="https://dash-bootstrap-components.opensource.faculty.ai/docs/", target="_blank"),
                    
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("A propos", href="/A_propos", external_link=True)
                    ],
                    nav=True,
                    in_navbar=True,
                    label="A propos",
                ),
            ],
            className="ml-auto mr-0 h6 flex-row flex-nowrap justify-content-end mt-0 w-50",
             navbar=False
        )

navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                    dbc.Col(dbc.NavbarBrand(className="ml-2", id='titre_page'))
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://plot.ly",
        ),
        liens,
    ],
    color="dark",
    dark=True,
    sticky='Top',
    className="mt-2 mb-3 text-white w-100, h-0"
)


# Affichage sur l'écran
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])



# Fonction qui gère le passage d'une page à une autre
@app.callback(Output('page-content', 'children'),
              Output('titre_page', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/apps/pib':
        return pib_app.layout, 'Données PIB'
    elif pathname == '/apps/travail':
        return travail_app.layout, 'Marché du travail'
    elif pathname == '/apps/covid':
        return covid_app.layout, 'Chiffres COVID'
    elif pathname == '/apps/commerce':
        return commerce_app.layout, 'Commerce international'
    elif pathname == '/apps/HID':
        return HID_app.layout, 'HDI'
    elif pathname == '/apps/petrol':
        return petrol_app.layout, 'Cours du pétrole'
    elif pathname =='/apps/actions':
        return actions_app.layout, 'Cours des actions'
    elif pathname =='return':
        return home_page.layout, 'Accueil'
    elif pathname =='/A_propos':
        return about_page.layout, 'A propos'
    else:
        return home_page.layout, 'Accueil'
    
    
    
# Lancement de l'application
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False, port=8000, host='127.0.0.1')
    
    
    