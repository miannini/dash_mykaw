# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 11:01:48 2020

@author: ANGEL_MARTINEZ
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
import os
import json
import dash_table
from datetime import timedelta
from datetime import date

import datetime
import dash_bootstrap_components as dbc

#LEE ARCHIVO BASE
def data_in():
    df = pd.read_csv(os.path.join("data/Data_lotes.csv"))
    df['KEY'] = df['Lat'].round(decimals=5).map(str) +"_"+ df['Lon'].round(decimals=5).map(str)
    
    df_1 = pd.read_csv(os.path.join("data/resumen_lotes_medidas.csv"))
    df_1['KEY'] = df_1['y'].round(decimals=5).map(str) +"_"+ df_1['x'].round(decimals=5).map(str)
    
    df_merge = pd.merge(df_1,df,on='KEY',how='left')
    df_merge['Fecha']= pd.to_datetime(df_merge['date'], format='%Y%m%d').dt.date
    
    df = df_merge[df_merge['Fecha']==max(df_merge['Fecha'])]
    
    return df_1, df_merge, df

def table_DB():
    df_DB = pd.read_csv(os.path.join("data/db_potreros.csv"))
    df_DB["NAME"] = df_DB["FINCA"]+ df_DB["POTRERO"].astype(str)
    df_DB["NAME"] = df_DB["NAME"].str.replace("LA ISLA", "La_Isla-Lote_", case = False) 
    df_DB["NAME"] = df_DB["NAME"].str.replace("PARAISO", "Paraiso-Lote_", case = False) 
    df_DB["NAME"] = df_DB["NAME"].str.replace("JUNCAL", "Juncalito-Lote_", case = False) 
    df_DB["NAME"] = df_DB["NAME"].str.replace("EL RECODO", "RC", case = False)
    df_DB["NAME"] = df_DB["NAME"].str.replace("MANGA LARGA", "La_Isla-Lote_ML_", case = False)
    df_DB["NAME"] = df_DB["NAME"].str.replace('RC([0-9]{1,2})T',r'T\1',case = False)
    df_DB["FECHA ACTIVIDAD"] = pd.to_datetime(df_DB["FECHA ACTIVIDAD"],format='%d/%m/%Y').dt.date
                                                    
    df_DB=df_DB.loc[:,['NAME','ACTIVIDAD','FECHA ACTIVIDAD','PRODUCTO','HATO','TIPO DE FORRAJE','NUMERO ANIMALES','LECHE TOTAL']].sort_values('FECHA ACTIVIDAD',ascending=False)
    df_DB=df_DB[df_DB['FECHA ACTIVIDAD'] > (date.today() - timedelta(days=360))]

    return df_DB

def lotes_cercanos():
    df, df_merge = graficas_all()
    DB_lotes_cercanos = pd.read_csv(os.path.join("data/lotes_cercanos.csv"))
    DB_lotes_cercanos = DB_lotes_cercanos.transpose().reset_index()
    DB_lotes_cercanos.columns = DB_lotes_cercanos.iloc[0]
    DB_lotes_cercanos = DB_lotes_cercanos.iloc[1:]
    DB_lotes_cercanos = DB_lotes_cercanos[:-1]
    
    return DB_lotes_cercanos, df, df_merge

def df_vacas():
    df_todos_los_datos = pd.read_csv(os.path.join("data/Todos_los_datos.csv"))
    df_sub = df_todos_los_datos['Numero'].unique()
    df_eventos_reg = pd.read_csv(os.path.join("data/Eventos_registrados.csv"))
    df_mastitis_vacas = pd.read_csv(os.path.join("data/Historico_Mastitis_Inversiones_Camacho-Vacas.csv"))
    
    return df_sub, df_todos_los_datos, df_eventos_reg, df_mastitis_vacas

def df_lotes():
    df_seguimiento_hatos = pd.read_csv(os.path.join("data/seguimiento_hatos(Test).csv"))
    #df_seguimiento_hatos[(df_seguimiento_hatos['date'] > '2020-03-01')]
    #df_seguimiento_hatos = df_seguimiento_hatos[df_seguimiento_hatos['date']==max(df_seguimiento_hatos['date'])]
    return df_seguimiento_hatos

#LEE GEOJSON
with open('data/Finca.geojson') as geofile:
    j_file_complete = json.load(geofile)
    
with open('data/La_Isla-polygon.geojson') as geofile:
    j_file = json.load(geofile)
    
with open('data/Juncalito-polygon.geojson') as geofile:
    j_file1 = json.load(geofile)
    
with open('data/Paraiso-polygon.geojson') as geofile:
    j_file2 = json.load(geofile)
    
with open('data/Recodo.geojson') as geofile:
    j_file3 = json.load(geofile)
    
with open('data/Recodo01-72.geojson') as geofile:
    j_file4 = json.load(geofile)
    
with open('data/RecodoT1-T9.geojson') as geofile:
    j_file5 = json.load(geofile)
    

#ESTILOS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server
app.config["suppress_callback_exceptions"] = True

#COLORES
colors = {
    'background': '#f7f7f7',
    'text': '#00a99e',
    'title': '#99b9b7',
    'subtitle': '#99b9b7',
    'Graph': '#d4d4d4',
    'text1' : '#080909',
    'GraphLine' : '#f4d44d',
    'Alto' : '#99e699',
    'Medio' : '#aae2fb',
    'Bajo' : '#ff9999'
}

#DEFINICION FUNCIONES 
def elaboracion_encabezado():
    return [
    html.Div(
        [
        html.H1(
            children='DASHBOARD FINCA LOS CAMACHO',
            style={
                'margin-left': '20px',
                'margin-top': '50px',
                'textAlign': 'Left',
                'color': colors['text']
            },className="nine columns"
        ),
        html.Img(
            src= app.get_asset_url('logo.png'),
            style={
                'height': '15%',
                'width': '15%',
                'float': 'right',
                'margin-top': '0px'
            },className="three columns"
        ),
        ],className="row flex-display"
    ),
    ]
def elaboracion_tabs():
    return [
    html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="tab1",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="TAB1",
                        label="La Isla, Juncalito y Paraiso",
                        value="tab1",
                        className="custom-tab",
                        selected_className="custom-tab--selected"
                    ),
                    dcc.Tab(
                        id="TAB2",
                        label="Recodo",
                        value="tab2",
                        className="custom-tab",
                        selected_className="custom-tab--selected"
                    ),
                    dcc.Tab(
                        id="TAB3",
                        label="Recodo - Control Lotes/Hatos",
                        value="tab3",
                        className="custom-tab",
                        selected_className="custom-tab--selected"
                    ),
                    dcc.Tab(
                        id="TAB4",
                        label="Monitoreo de mi ganado",
                        value="tab4",
                        className="custom-tab",
                        selected_className="custom-tab--selected"
                    )
                ],style={'textAlign': 'center','color': colors['title'], 'font-size': '25px'}
            )
        ]
    )
    ]

#ELABORACION MAPA La Isla, Juncalito y Paraiso

mapbox_access_token = "pk.eyJ1IjoiYmxhY2thbmdlbGl0byIsImEiOiJja2NlN2Rhc2YwMmU5MnFtZ25rMDBwcWZoIn0.s3voGZglWzPU5OOZHYWjHw"

#Variables necesarias para hover_data
def graficas_all():
    df_1, df_merge, df = data_in()
    df=df.copy()
    df.loc[:,"Lote"] = df.loc[:,"name"]
    df.loc[:,"Área"] = df.loc[:,"Area"] + " m^2"
    df.loc[:,"Índice de Vegetación"] = round(df.loc[:,"mean_value._NDVI"],4)
    df.loc[:,"Biomasa"] = round(df.loc[:,"biomass_corrected"],2)
    df.loc[:,"Índice de Hoja"] = round(df.loc[:,"mean_value._LAI"],2)
    df.loc[:,"Humedad"] = round(df.loc[:,"mean_value._MOIST"],2)
    return df, df_merge

#Mapa de la pestaña Juncalito, la isla
def fig_tab1():
    df, df_merge = graficas_all()
    
    mapa_tab1 = px.choropleth_mapbox(
        df,
        geojson=j_file_complete,
        color="Índice de Vegetación",
        locations="Lote", 
        featureidkey="properties.name",
        center={"lat": 5.534985, "lon": -73.796751},
        mapbox_style="satellite", 
        zoom=14.2,
        #animation_frame="Fecha",
        color_continuous_scale=["red", "yellow", "green"],
        hover_data={"Lote": True, "Área": True, "Índice de Vegetación": True, "Biomasa": True, "Índice de Hoja": True, "Humedad": True, "mean_value._NDVI": False}
    )
    
    mapa_tab1.update_geos(fitbounds="locations", visible=True)
    
    mapa_tab1.update_layout(
        margin=dict(t=10, r=10, b=10, l=10), 
        clickmode = 'event+select',
        mapbox_accesstoken=mapbox_access_token,
        mapbox=dict(
            layers=[
                dict(
                    sourcetype = 'geojson',
                    source = j_file, 
                    below="water",
                    type = 'line',
                    color = '#fb8aff',
                    opacity= 0.5
                ),
                dict(
                    sourcetype = 'geojson',
                    source = j_file1, 
                    below="water",
                    type = 'line',
                    color = '#ffffff',
                    opacity= 0.5
                ),
                dict(
                    sourcetype = 'geojson',
                    source = j_file2, 
                    below="water",
                    type = 'line',
                    color = '#3399ff',
                    opacity= 0.5
                )
            ]
        )
    )
    return mapa_tab1

#Gráfico de la pestaña mapa recodo
def fig_tab2():
    df, df_merge = graficas_all()
    mapa_tab2 = px.choropleth_mapbox(
        df,
        geojson=j_file3, 
        color="Índice de Vegetación",
        locations="Lote", 
        featureidkey="properties.name",
        center={"lat": 5.497800, "lon": -73.775426},
        mapbox_style="satellite",
        zoom=14.2,
        color_continuous_scale=["red", "yellow", "green"],
        hover_data={"Lote": True, "Área": True, "Índice de Vegetación": True, "Biomasa": True, "Índice de Hoja": True, "Humedad": True, "mean_value._NDVI": False}
    )
    
    mapa_tab2.update_geos(fitbounds="locations", visible=True)
    
    mapa_tab2.update_layout(
        margin=dict(t=10, r=10, b=10, l=10),
        clickmode = 'event+select',
        mapbox_accesstoken=mapbox_access_token,
        mapbox=dict(
            layers=[
                dict(
                    sourcetype = 'geojson',
                    source = j_file4, 
                    below="water",
                    type = 'line',
                    color = '#3399ff'
                ),   
                dict(
                    sourcetype = 'geojson',
                    source = j_file5, 
                    below="water",
                    type = 'line',
                    color = '#fb8aff'
                )
            ]
        )
    )
    return mapa_tab2

#Gráfico de la pestaña mapa recodo - control lotes/hatos
def fig_tab3():
    df_seguimiento_hatos = df_lotes()[-100:-1]
    mapa_tab3 = px.choropleth_mapbox(
        df_seguimiento_hatos,
        geojson=j_file3, 
        color="HATO",
        locations="name", 
        featureidkey="properties.name",
        center={"lat": 5.497800, "lon": -73.775426},
        mapbox_style="satellite",
        zoom=13.6,
        animation_frame="date",
        #animation_group="name",
        hover_data={"name": True, "TIPO DE FORRAJE": True, "NUMERO ANIMALES": True}
    )
    
    mapa_tab3.update_geos(fitbounds="locations", visible=True)
    
    mapa_tab3.update_layout(
        margin=dict(t=10, r=10, b=10, l=10),
        clickmode = 'select+event',
        mapbox_accesstoken=mapbox_access_token,
        mapbox=dict(
            layers=[
                dict(
                    sourcetype = 'geojson',
                    source = j_file4, 
                    below="water",
                    type = 'line',
                    color = '#3399ff'
                ),   
                dict(
                    sourcetype = 'geojson',
                    source = j_file5, 
                    below="water",
                    type = 'line',
                    color = '#fb8aff'
                )
            ]
        )
    )
    return mapa_tab3


#CONTRUCCION DE LAS PESTAÑAS DEL TABLERO
def elaboracion_tab_1():
    mapa_tab1 = fig_tab1()
    df_DB = table_DB().head(20)
    return [
        html.Div([
                html.Div(
                    [dcc.Graph(id="Grafica_principal",figure=mapa_tab1)],
                    className="pretty_container seven columns"
                ),
                html.Div(
                    [dcc.Graph(id="Grafica_datos")],
                    className="pretty_container five columns"
                )
        ], className="row flex-display"
        ),
        html.Div([
                html.Div(
                    children=[
                        html.H4(children='Historico Actividades Lotes'),
                        dash_table.DataTable(
                            id='tablaDBpotreros',
                            columns=[{"name": i, "id": i} for i in df_DB.columns],
                            page_current=0,
                            page_action='custom'
                        )
                    ], className="pretty_container seven columns"
                ),
                html.Div(
                    [dcc.Graph(id="Grafica_Top")],
                    className="pretty_container five columns"
                )
        ], className="row flex-display"
        )
    ]

def elaboracion_tab_2():
    mapa_tab2 = fig_tab2()
    df_DB = table_DB().head(20)
    return [
            html.Div([
                html.Div(
                    [dcc.Graph(id="Grafica_principal",figure=mapa_tab2)],
                    className="pretty_container seven columns"
                ),
                html.Div(
                    [dcc.Graph(id="Grafica_datos")],
                    className="pretty_container five columns"
                )
            ], className="row flex-display"
            ),
            html.Div([
                html.Div(
                    children=[
                        html.H4(children='Historico Actividades Lotes'),
                        dash_table.DataTable(
                            id='tablaDBpotreros',
                            columns=[{"name": i, "id": i} for i in df_DB.columns],
                            page_current=0,
                            page_action='custom'
                        )
                    ], className="pretty_container seven columns"
                ),
                html.Div(
                    [dcc.Graph(id="Grafica_Top")],
                    className="pretty_container five columns"
                )
            ], className="row flex-display"
            )
    ]

def elaboracion_tab_3():
    mapa_tab3 = fig_tab3()
    df_DB = table_DB().head(20)
    return [
            html.Div([
                html.Div(
                    [dcc.Graph(id="Grafica_principal_tab3",figure=mapa_tab3)],
                    className="pretty_container seven columns"
                ),
                html.Div(
                    [dcc.Graph(id="ts_prod_leche_tab3")],
                    className="pretty_container five columns"
                )
            ], className="row flex-display"
            ),
            html.Div([
                html.Div(
                    children=[
                        html.H4(children='Historico Actividades Lotes'),
                        dash_table.DataTable(
                            id='tablaDBpotreros',
                            columns=[{"name": i, "id": i} for i in df_DB.columns],
                            page_current=0,
                            page_action='custom'
                        )
                    ], className="pretty_container seven columns"
                ),
                html.Div(
                    [dcc.Graph(id="Grafica_Top")],
                    className="pretty_container five columns"
                )
            ], className="row flex-display"
            )
    ]

def elaboracion_tab_4():
    df_sub = df_vacas()[0]
    df_eventos_reg = df_vacas()[2]
    return [
        html.Div([
                html.Div([
                    html.Label('ID Vaca'),
                    dcc.Dropdown(id='filtro_vaca',
                        options=[{'label': i, 'value': i} for i in df_sub],
                        value='1234'
                    )
                ], className="pretty_container five columns"
                ),
                
                
                html.Div([
                    html.Div(
                        html.Img(
                        src= app.get_asset_url('cow.png'),
                        style={'height': '60%','width': '60%','margin-top': '15px'},
                        ), className="pretty_container eight columns", style={'textAlign': 'right'}
                    ),
                    html.Div([
                        dbc.Card([
                            dbc.CardBody([
                                html.H2(id="ID_vaca", className="card-title", style={'color': '#00A99E', 'font-weight': 'bold'}),
                                html.H6(id="Estado_vaca", className="card-text"),
                                html.H6(id="Edad_vaca", className="card-text"),
                                html.H6(id="Raza_vaca", className="card-text"),
                                html.H6(id="Sexo/tipo_vaca", className="card-text")
                            ]
                            )
                        ]
                        )
                    ], className="pretty_container four columns",
                        style={'textAlign': 'left', 'height': '30%','width': '30%'}
                    )  
                ], className="row"
                ),
                
                
                html.Div([
                    html.Div([
                        dbc.Card([
                            dbc.CardImg(
                                src= app.get_asset_url('curve.png'), 
                                top=True, 
                                style={'height': '30%','width': '40%','margin-top': '10px'}
                            ),
                            dbc.CardBody([
                                html.H4(id="DIM", className="card-title", style={'font-weight': 'bold'}),
                                html.P(id="Tercio_lactancia", className="card-title")
                            ]
                            )
                        ]
                        )
                    ], className="pretty_container four columns", 
                        style={'textAlign': 'center', 'height': '30%','width': '30%', 'backgroundColor':'#f7f7f7', 'border-style': 'solid', 'border-color': '#00A99E'}
                    ),
                    
                    html.Div([
                        dbc.Card([
                            dbc.CardImg(
                                src= app.get_asset_url('milk.png'), 
                                top=True, 
                                style={'height': '30%','width': '40%','margin-top': '10px'}
                            ),
                            dbc.CardBody([
                                html.H4(id="Leche_prom_mes", className="card-title", style={'font-weight': 'bold'}),
                                html.H5(id="Lt_lact_vs_hato", className="card-title"),
                                html.P("Lt  Lact. vs. hato", className="card-title")
                            ]
                            )
                        ]
                        )
                    ], className="pretty_container four columns", 
                        style={'textAlign': 'center', 'height': '30%','width': '30%', 'backgroundColor':'#f7f7f7', 'border-style': 'solid', 'border-color': '#00A99E'}
                    ),
                    
                    html.Div([
                        dbc.Card([
                            dbc.CardImg(
                                src= app.get_asset_url('fertilization.png'), 
                                top=True, 
                                style={'height': '30%','width': '40%','margin-top': '10px'}
                            ),
                            dbc.CardBody([
                                html.H4(id="Ultimo_diag_preñez", className="card-title", style={'font-weight': 'bold'}),
                                html.H5(id="Ultimo_resultado", className="card-title"),
                                html.P("Ult. Diag. Preñez", className="card-title")
                            ]
                            )
                        ]
                        )
                    ], className="pretty_container four columns", 
                        style={'textAlign': 'center', 'height': '30%','width': '30%', 'backgroundColor':'#f7f7f7', 'border-style': 'solid', 'border-color': '#00A99E'}
                    )
                ], className="row"
                ),
                
                
                html.Div([
                    html.Div([
                        dbc.Card([
                            dbc.CardImg(
                                src= app.get_asset_url('ubre(1).png'), 
                                top=True, 
                                style={'height': '30%','width': '40%','margin-top': '10px'}
                            ),
                            dbc.CardBody([
                                html.H4(id="Mast_vida", className="card-title", style={'font-weight': 'bold'}),
                                html.H5(id="Mast_activa", className="card-title")
                            ]
                            )
                        ]
                        )
                    ], className="pretty_container four columns", 
                        style={'textAlign': 'center', 'height': '30%','width': '30%', 'backgroundColor':'#f7f7f7', 'border-style': 'solid', 'border-color': '#00A99E'}
                    ),
                    
                    html.Div([
                        dbc.Card([
                            dbc.CardImg(
                                src= app.get_asset_url('muletas.png'), 
                                top=True, 
                                style={'height': '30%','width': '40%','margin-top': '10px'}
                            ),
                            dbc.CardBody([
                                html.H4(id="Cojera_vida", className="card-title", title=" Mes", style={'font-weight': 'bold'}),
                                html.H5(id="Cojera_activa", className="card-title")
                            ]
                            )
                        ]
                        )
                    ], className="pretty_container four columns", 
                        style={'textAlign': 'center', 'height': '30%','width': '30%', 'backgroundColor':'#f7f7f7', 'border-style': 'solid', 'border-color': '#00A99E'}
                    ),
                    
                    html.Div([
                        dbc.Card([
                            dbc.CardImg(
                                src= app.get_asset_url('calf.png'), 
                                top=True, 
                                style={'height': '30%','width': '40%','margin-top': '10px'}
                            ),
                            dbc.CardBody([
                                html.H4(id="No_crias", className="card-title", style={'font-weight': 'bold'}),
                                html.H5(id="Int_entre_partos", className="card-title"),
                                html.P("Intervalo entre partos", className="card-title")
                            ]
                            )
                        ]
                        )
                    ], className="pretty_container four columns", 
                        style={'textAlign': 'center', 'height': '30%','width': '30%', 'backgroundColor':'#f7f7f7', 'border-style': 'solid', 'border-color': '#00A99E'}
                    )
                ], className="row"
                )
                
        ], className="pretty_container six columns"
        ),    
         
        
        html.Div([
            html.Div([
                dash_table.DataTable(
                    id='tablaEventosRegistrados',
                    columns=[{"name": i, "id": i} for i in df_eventos_reg.columns],
                    page_current=0,
                    page_size=25,
                    page_action='custom',
                    style_data_conditional=[{
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                    }
                    ],
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold'
                    }
                )
            ], className="pretty_container twelve columns",
                style={'margin-top': '20px'}
            )   
        ], className="pretty_container six columns"
        ), 

        html.Div([
            html.H2(children='CONTROL DE MASTITIS')
        ], className="pretty_container twelve columns",
            style={'textAlign': 'center', 'height': '10%','width': '100%', 'backgroundColor':'#f7f7f7', 'border-style': 'solid', 'border-color': '#00A99E'}
        ),

        html.Div([            
            html.Div([
                dcc.Graph(id="% UBRE SANA VS % CALIFICACIÓN")
            ], className="pretty_container six columns",
                style={'margin-top': '20px'}
            ),
            
            html.Div([
                dcc.Graph(id="Calificación Pezón")
            ], className="pretty_container six columns",
                style={'margin-top': '20px'}
            )
        ], className="pretty_container twelve columns"
        )
    ]

#ESQUELETO DE DASH
def app_layout(): 
    return html.Div(
        style={'backgroundColor': colors['background']},
        children=[
            html.Div([
                    #ENCABEZADO
                    html.Div(elaboracion_encabezado()),
                    #TABS
                    html.Div(elaboracion_tabs()),
                    #FILTROS       
                    html.Div(
                        id = 'secciones', 
                        children=[
                            #CONTENIDO
                            html.Div(id="app-content")
                        ]
                    )
            ])
        ]
    )

#Este es un callback que cambia entre TABs
@app.callback(
    Output("app-content", "children"),
    [Input("app-tabs", "value")]
)
def render_tab_content(tab_switch):
    if tab_switch == "tab1":
        return elaboracion_tab_1()
    if tab_switch == "tab2":
        return elaboracion_tab_2()
    if tab_switch == "tab3":
        return elaboracion_tab_3()
    if tab_switch == "tab4":
        return elaboracion_tab_4()
#--------------------------------------------------------------------------------------------------------------------------------------------


#TABS 1 Y 2
#Elaboración de Grafico en linea de Tiempo de variables Satelitales por lote
@app.callback(Output("Grafica_datos", "figure"), 
              [Input("Grafica_principal", "selectedData")])
def make_individual_figure(Grafica_principal_click):
    df, df_merge = graficas_all()    
    if Grafica_principal_click is None:
        lote_name = ['Vista Completa']
    else:
        lote_name = Grafica_principal_click['points'][0]['customdata']
        lote_name = lote_name[0].split()
    
    if lote_name[0] == 'Vista Completa':
        df_grouped = df_merge.groupby(['Fecha']).agg(mean_NDVI=('mean_value._NDVI',"mean"),mean_BM=('biomass_corrected',"mean"),mean_LAI=('mean_value._LAI',"mean"),mean_MOIST=('mean_value._MOIST',"mean")).reset_index()
    else:
        df_grouped = df_merge.groupby(['Fecha','name']).agg(mean_NDVI=('mean_value._NDVI',"mean"),mean_BM=('biomass_corrected',"mean"),mean_LAI=('mean_value._LAI',"mean"),mean_MOIST=('mean_value._MOIST',"mean")).reset_index()
        df_grouped = df_grouped[df_grouped['name']== lote_name[0]]
        
    
    ts_tab1_2 = make_subplots(specs=[[{"secondary_y": True}]])
    
    ts_tab1_2.add_trace(
        go.Scatter(x=df_grouped['Fecha'], y=df_grouped['mean_NDVI'], name="NDVI"),
        secondary_y=False
    )
    ts_tab1_2.add_trace(
        go.Scatter(x=df_grouped['Fecha'], y=df_grouped['mean_LAI'], name="LAI"),
        secondary_y=False
    )
    ts_tab1_2.add_trace(
        go.Scatter(x=df_grouped['Fecha'], y=df_grouped['mean_MOIST'], name="MOIST"),
        secondary_y=False
    )
    ts_tab1_2.add_trace(
        go.Scatter(x=df_grouped['Fecha'], y=df_grouped['mean_BM'], name="BIOMASA"),
        secondary_y=True
    )
    
    ts_tab1_2.update_layout(
        title_text="Datos Históricos"
    )
    
    ts_tab1_2.update_layout(
        title_text=lote_name[0],
        autosize = True,
        paper_bgcolor=colors['background'],
        margin=dict(t=70, r=30, b=40, l=0),
        plot_bgcolor = '#ffffff',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis = dict(tickangle= -90),
        yaxis = dict(automargin= True)
    )    
    return ts_tab1_2

#Tabla de registros por lote (db_potreros)
@app.callback(Output("tablaDBpotreros", "data"), 
              [Input("Grafica_principal", "selectedData")])
    
def generate_table(Grafica_principal_click):
    df_DB = table_DB()
    if Grafica_principal_click is None:
        lote_name = ['Vista Completa']
    else:
        lote_name = Grafica_principal_click['points'][0]['customdata']
        lote_name = lote_name[0].split()
    
    if lote_name[0] == 'Vista Completa':
        df_DB = df_DB.copy()
    else:
        df_DB = df_DB[df_DB['NAME']== lote_name[0]]
    df_DB = df_DB.head(20)
    return df_DB.to_dict('records')

#Elaboración de Gráfico Top 5 lotes cercanos
@app.callback(Output("Grafica_Top", "figure"), 
              [Input("Grafica_principal", "selectedData")])
def grafica_top(Grafica_principal_click):
    DB_lotes_cercanos, df, df_merge = lotes_cercanos()
    if Grafica_principal_click is None:
        lote_name = ['Vista Completa']
    else:
        lote_name = Grafica_principal_click['points'][0]['customdata']
        lote_name = lote_name[0].split()
    
    if lote_name[0] == 'Vista Completa':
        df_top = df.nlargest(5,'mean_value._NDVI')
    else:
        df_top = df.nlargest(5,'mean_value._NDVI')
        DB_lotes_cercanos= DB_lotes_cercanos.loc[:,[lote_name[0]]]
        df_top = df[df['name']== DB_lotes_cercanos]
    
    top5_lotes_tab1_2 = px.bar(df_top, x='name', y='mean_value._NDVI')
    
    top5_lotes_tab1_2.update_layout(
        title_text="Top Mejores Lotes Para Traslado de Ganado por NDVI",
        autosize = True,
        paper_bgcolor=colors['background'],
        margin=dict(t=70, r=30, b=40, l=0),
        plot_bgcolor = '#ffffff',
        legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
        xaxis = dict(tickangle= -90),
        yaxis = dict(automargin= True)
    )   
    return top5_lotes_tab1_2
#--------------------------------------------------------------------------------------------------------------------------------------------


#TAB 3
#Elaboración de gráfico en series de tiempo de producción de leche por hato, click por lote
@app.callback(Output("ts_prod_leche_tab3", "figure"), 
              [Input("Grafica_principal_tab3", "selectedData")])
def generate_grafica_produccion_leche(Grafica_principal_click):
    df_seguimiento_hatos = df_lotes()

    if Grafica_principal_click is None:
        lote_name = ['Vista Completa']
    else:
        lote_name = Grafica_principal_click['points'][0]['customdata']
        lote_name = lote_name[0].split()

    if lote_name[0] == 'Vista Completa':
        produccion_leche = df_seguimiento_hatos.copy()
    else:
        produccion_leche = df_seguimiento_hatos[df_seguimiento_hatos['name']== lote_name[0]]    
    
    ts_prod_leche_tab3 = px.line(produccion_leche, x='date', y='LECHE TOTAL', color='HATO')
        
    ts_prod_leche_tab3.update_xaxes(zeroline=True, gridcolor='Grey', zerolinewidth=2, zerolinecolor='#00A99E', title_text='Fecha')
    ts_prod_leche_tab3.update_yaxes(gridcolor='Grey')
    
    ts_prod_leche_tab3.update_layout(
        autosize = True,
        paper_bgcolor=colors['background'],
        margin=dict(t=70, r=30, b=40, l=0),
        plot_bgcolor = '#ffffff',
        title_text="Producción de Leche por fecha-Hato, Lote",
        legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
        xaxis = dict(tickangle= -45),
        yaxis = dict(automargin= True)
    )    
    return ts_prod_leche_tab3
#--------------------------------------------------------------------------------------------------------------------------------------------


#TAB 4
#Elaboración tabla eventos e Indicadores por animal
@app.callback(Output("tablaEventosRegistrados", "data"), 
              [Input("filtro_vaca", 'value'),
               Input('tablaEventosRegistrados', "page_current"),
               Input('tablaEventosRegistrados', "page_size")])
def generate_tabla_ev_vacas(filtro_tabla_ev_vacas,page_current,page_size):
    df_eventos_reg = df_vacas()[2]
    tabla_ev_vacas = df_eventos_reg[df_eventos_reg['Id'] == filtro_tabla_ev_vacas]
    return tabla_ev_vacas.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')[0:25]

@app.callback([Output("ID_vaca", "children"),
               Output("Estado_vaca", "children"),
               Output("Edad_vaca", "children"),
               Output("Raza_vaca", "children"),
               Output("Sexo/tipo_vaca", "children"),
               Output("DIM", "children"), 
               Output("Tercio_lactancia", "children"),
               Output("Leche_prom_mes", "children"),
               Output("Lt_lact_vs_hato", "children"),
               Output("Ultimo_diag_preñez", "children"),
               Output("Ultimo_resultado", "children"),
               Output("Mast_vida", "children"),
               Output("Mast_activa", "children"),
               Output("Cojera_vida", "children"),
               Output("Cojera_activa", "children"),
               Output("No_crias", "children"),
               Output("Int_entre_partos", "children")],
              [Input("filtro_vaca", 'value')])
def generate_Indicadores(filtro_id_indicadores):
    df_todos_los_datos = df_vacas()[1]
    id_indicadores = df_todos_los_datos[df_todos_los_datos['Numero'] == filtro_id_indicadores]
    return (id_indicadores["ID"],
            id_indicadores["Estado"],
            id_indicadores["Edad"],
            id_indicadores["Raza"],
            id_indicadores["Sexo/ tipo"],
            id_indicadores["DIM_c"],
            id_indicadores["Tercio lactancia (groups)"],
            id_indicadores["Leche_prom_mes_c"],
            id_indicadores["Lt Lact. vs.hato_C"],
            id_indicadores["Ult. diag. preñez"],
            id_indicadores["Ult. resultado"],
            id_indicadores["Mast_vida"],
            id_indicadores["Mast_activa"],
            id_indicadores["Cojera_vida"],
            id_indicadores["Cojera_activa"],
            id_indicadores["No_crias"],
            id_indicadores["Int_entre_partos"])

#Elaboración de gráfico en series de tiempo de ubre y calificación por mastitis
@app.callback(Output("% UBRE SANA VS % CALIFICACIÓN", "figure"), 
              [Input("filtro_vaca", 'value')])
def generate_grafica_ubre_sana_vs_calif(filtro_ubre_sana_vs_calif_vacas):
    df_mastitis_vacas = df_vacas()[3]
    ubre_sana_vs_calif_vacas = df_mastitis_vacas[df_mastitis_vacas['NOMBRE'] == filtro_ubre_sana_vs_calif_vacas]
    
    ts_ubre_tab4 = go.Figure()
    
    ts_ubre_tab4.add_trace(
        go.Scatter(x=ubre_sana_vs_calif_vacas['FECHA CHEQUEO'], y=ubre_sana_vs_calif_vacas['UBRE SANA']*100, name="% Ubre Sana", line=dict(width=2))
    )
    ts_ubre_tab4.add_trace(
        go.Scatter(x=ubre_sana_vs_calif_vacas['FECHA CHEQUEO'], y=ubre_sana_vs_calif_vacas['CAL. UBRE']*100, name="% Cal. Ubre", line=dict(width=2))
    )
    
    ts_ubre_tab4.update_xaxes(zeroline=True, gridcolor='Grey', zerolinewidth=2, zerolinecolor='#00A99E', title_text='Fecha de Chequeo')
    ts_ubre_tab4.update_yaxes(gridcolor='Grey', ticksuffix="%")
    
    ts_ubre_tab4.update_layout(
        autosize = True,
        paper_bgcolor=colors['background'],
        margin=dict(t=70, r=30, b=40, l=0),
        plot_bgcolor = '#ffffff',
        title_text="% UBRE SANA VS % CALIFICACIÓN",
        legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
        xaxis = dict(tickangle= -45),
        yaxis = dict(automargin= True)
    )    
    return ts_ubre_tab4

#Elaboración de gráfico en series de tiempo de calificación por pezón
@app.callback(Output("Calificación Pezón", "figure"), 
              [Input("filtro_vaca", 'value')])
def generate_grafica_calif_pezon(filtro_calif_pezon_vacas):
    df_mastitis_vacas = df_vacas()[3]
    calif_pezon_vacas = df_mastitis_vacas[df_mastitis_vacas['NOMBRE'] == filtro_calif_pezon_vacas]
    
    ts_calif_pezon_tab4 = go.Figure()
    
    ts_calif_pezon_tab4.add_trace(
        go.Bar(x=calif_pezon_vacas['FECHA CHEQUEO'], y=calif_pezon_vacas['AI'], name="Pezón AI", hovertext=calif_pezon_vacas['Observación'])
    )
    ts_calif_pezon_tab4.add_trace(
        go.Bar(x=calif_pezon_vacas['FECHA CHEQUEO'], y=calif_pezon_vacas['AD'], name="Pezón AD", hovertext=calif_pezon_vacas['Observación'])
    )
    ts_calif_pezon_tab4.add_trace(
        go.Bar(x=calif_pezon_vacas['FECHA CHEQUEO'], y=calif_pezon_vacas['PI'], name="Pezón PI", hovertext=calif_pezon_vacas['Observación'])
    )
    ts_calif_pezon_tab4.add_trace(
        go.Bar(x=calif_pezon_vacas['FECHA CHEQUEO'], y=calif_pezon_vacas['PD'], name="Pezón PD", hovertext=calif_pezon_vacas['Observación'])
    )
    
    ts_calif_pezon_tab4.update_xaxes(zeroline=True, gridcolor='Grey', title_text='Fecha de Chequeo')
    ts_calif_pezon_tab4.update_yaxes(gridcolor='Grey')
    
    ts_calif_pezon_tab4.update_layout(
        autosize = True,
        paper_bgcolor=colors['background'],
        margin=dict(t=70, r=30, b=40, l=0),
        plot_bgcolor = '#ffffff',
        barmode='group',
        title_text="Calificación por pezón",
        legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
        xaxis = dict(tickangle= -45),
        yaxis = dict(automargin= True)
    )    
    return ts_calif_pezon_tab4           
#--------------------------------------------------------------------------------------------------------------------------------------------


app.layout = app_layout

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader = True)