import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import pib, emplois, HID


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/apps/pib':
        return pib.layout
    elif pathname == '/apps/emplois':
        return emplois.layout
    elif pathname == '/apps/HID':
        return HID.layout

    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)