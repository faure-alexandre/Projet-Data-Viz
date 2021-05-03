import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objects as go
import math
import pandas as pd
from plotly import subplots
from dash.dependencies import Input, Output
from app import app
from plotly.subplots import make_subplots


dataFrame=pd.read_csv("data/owid-covid-data.csv")

continent=dataFrame.continent.unique().tolist()
continent=np.delete(continent, 1)


layout = html.Div([

            # Div for graph1
            html.Div([
            dcc.Graph(id='graph_1')
            ],style={'width':'49%','display': 'inline-block'}),

            # Div for graph2
            html.Div([
            dcc.Graph(id='graph_2')
            ],style={'width':'49%','display': 'inline-block'}),

            # Div for Dropdown
            html.Div([
            dcc.Dropdown(id='selection_pays', 
                        options=[{'label': i, 'value': i} for i in continent],value="Asia")
                        ],style={'width':'10%','color':'blue'}),

])



@app.callback(
    Output('graph_1', 'figure'),
    Output('graph_2', 'figure'),
    [Input('selection_pays', 'value')])
def update_figure(cont):
    data = dataFrame[dataFrame.continent == cont]
    data_sorted=data.groupby(['location']).human_development_index.mean()
    HDI_per_country=pd.to_numeric(data_sorted.values,errors="coerce")

 # On prend l'age median pour chaque pays
    data_age_median = data[['iso_code', 'median_age','location']].groupby(by='location', as_index=False).agg(np.max)
    
    
    deaths_permillions=pd.to_numeric(data.groupby(['location']).total_deaths_per_million.last().values,errors="coerce")
    extreme_poverty=pd.to_numeric(data.groupby(['location']).extreme_poverty.last().values,errors="coerce")

    age_median=pd.to_numeric(data.groupby(['location']).median_age.last().values,errors="coerce")

    country=data_sorted.index.values.tolist()

    idx=[]
    for x in range(len(HDI_per_country)):
        if pd.isnull(HDI_per_country[x]) == True or pd.isnull(age_median[x]) or pd.isnull(extreme_poverty[x]):
            idx.append(x)


    HDI_per_country=np.delete(HDI_per_country, idx)
    country=np.delete(country, idx)
    deaths_permillions=np.delete(deaths_permillions, idx)
    age_median=np.delete(age_median, idx)
    extreme_poverty=np.delete(extreme_poverty,idx)
    fig1 = make_subplots()
    fig1.add_trace(go.Scatter(x=country,
                   y=deaths_permillions,
                  mode= 'markers',
                  marker= dict(
                    color = HDI_per_country,
                    size = age_median,
                  showscale = True,
                  colorbar=dict(
                  title ="HDI"),
                  colorscale="Bluered_r")))

    fig1.update_layout(title = 'HDI', yaxis = dict(title = "Décès par millions d'habitants"),paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',title_font_color="white",font_color='white',legend_title_font_color='white',font=dict(size=14))
    
    
    
    fig2 = go.Figure(data=go.Choropleth(
        locations=data_age_median['iso_code'], # Spatial coordinates
        z = data_age_median['median_age'].astype(float), # Data to be color-coded
        colorscale = 'Bluered_r',
        colorbar_title = "Age Médian",
        ))

    if cont != "Oceania":
        fig2.update_layout(
            title_text = 'Age médian de la population',
            geo_scope="world"#cont.lower(), # limite map scope to USA
             )

    fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',title_font_color="white",font_color='white',legend_title_font_color='white',font=dict(size=14))
    fig2.update_geos(visible=False,showocean=True, oceancolor='lightblue')

    return fig1, fig2


