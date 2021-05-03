import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import math
import pandas as pd
from plotly.offline import init_notebook_mode, iplot, plot
from plotly import subplots
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output
from app import app


df = pd.read_excel('data/RWTCd.xls',sheet_name=1, header=2)
value=df['Cushing, OK WTI Spot Price FOB (Dollars per Barrel)'].tolist()
date=df.Date


dataFrame=pd.read_csv("data/owid-covid-data.csv")
pays=dataFrame.location.unique().tolist()

dataFram=pd.read_csv("data/Untitled1.csv",decimal=',')
country_petrole=dataFram["Unnamed: 0"].values.tolist()
values=dataFram["pctge"].values.tolist()


layout = html.Div([
            # Div for graph1
            html.Div([
            dcc.Graph(id='g1')
            ],style={'width':'55%','display': 'inline-block'}),

            # Div for graph2
            html.Div([
            dcc.Graph(id='g2')
            ],style={'width':'45%','display': 'inline-block'}),

                        # Div for Dropdown
            html.Div([
            dcc.RadioItems(id='selection_pays',
                        options=[{'label': i, 'value': i} for i in country_petrole],value="United States")
                        ],style={'width':'100%','color': '#FFFFFF'}, className='row'),

])



@app.callback(
    Output('g1', 'figure'),
    [Input('selection_pays', 'value')])


def update_figure(cont):
    index_conf = dataFrame[dataFrame.location == cont].stringency_index
    date_conf=dataFrame[dataFrame.location == "United States"].date
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(go.Scatter(x=date[8400:],
                   y=value[8400:],
                  mode= 'lines',
                name="Prix du baril",line = dict(width=4)))

    fig.add_trace(go.Scatter(x=date_conf,
                   y=index_conf,
                  mode= 'lines',
                name="Confinement",line = dict(width=4)),
             secondary_y=True)

    fig.update_layout(title="Evolution du prix du baril en $ en fonction des confinements", paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',title_font_color="white",font_color='white',legend_title_font_color='white',font=dict(size=14))
    fig.update_yaxes(title_text="Prix du baril en dollars", secondary_y=False)
    fig.update_yaxes(title_text="Indice du confinement", secondary_y=True)
    
    return fig


@app.callback(
    Output('g2', 'figure'),
    [Input('selection_pays', 'value')])

def update_figure(cont):
    pl=np.zeros((len(country_petrole),))
    idx=np.where(cont==np.array(country_petrole))
    pl[idx]=0.1
    fig2 = go.Figure(data=[go.Pie(labels=country_petrole, values=values, textinfo='label+percent',pull=pl)])
    fig2.update_layout(title="Les 10 plus grands pays exportateurs de pétrole", paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',title_font_color="white",font_color='white',legend_title_font_color='white',font=dict(size=14))

    return fig2
