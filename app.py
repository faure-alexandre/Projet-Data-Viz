import dash
import dash_bootstrap_components as dbc


app = dash.Dash(__name__, suppress_callback_exceptions=True, 
                external_stylesheets=[dbc.themes.SLATE], update_title='Chargement...',
                title='Covid Dashboard')

server = app.server
