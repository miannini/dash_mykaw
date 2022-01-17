# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 11:01:48 2020

@author: ANGEL_MARTINEZ
"""

import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import os
import json
import dash_table
from datetime import timedelta
from datetime import date

import datetime
import dash_bootstrap_components as dbc

import mysql.connector
db_connection = mysql.connector.connect(
    host="35.229.36.251",
      user="m4a.DA",
      passwd="m4a2020"
    )
#--------------------------------------------------------------------------------------------------------------------------------------------


#LEE ARCHIVO BASE
def data_in():
    db_connection = mysql.connector.connect(host="35.229.36.251", user="m4a.DA", passwd="m4a2020")

    # df = pd.read_csv(os.path.join("data/Data_lotes.csv"))
    sql_df = '''select * from m4a_bi.Data_lotes'''
    df  = pd.read_sql(sql_df, db_connection)
    df['KEY'] = df['Lat'].round(decimals=5).map(str) +"_"+ df['Lon'].round(decimals=5).map(str)
    df_1 = pd.read_csv(os.path.join("data/resumen_lotes_medidas.csv"))
    # sql_df_1 = '''select * from m4a_bi.resumen_lotes_medidas'''
    # df_1  = pd.read_sql(sql_df_1, db_connection)
    df_1['KEY'] = df_1['y'].round(decimals=5).map(str) +"_"+ df_1['x'].round(decimals=5).map(str)
    df_merge = pd.merge(df_1,df,on='KEY',how='left')
    df_merge['Fecha']= pd.to_datetime(df_merge['date'], format='%Y%m%d').dt.date
    df = df_merge[df_merge['Fecha']==max(df_merge['Fecha'])]
    
    db_connection.close()
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
    df_todos_los_datos2 = pd.read_csv(os.path.join("data/Todos_los_datos2.csv"))
    df_sub = df_todos_los_datos['Numero'].unique()
    df_grupo = df_todos_los_datos2['Grupo'].unique()
    df_eventos_reg = pd.read_csv(os.path.join("data/Eventos_registrados.csv"))
    df_mastitis_vacas = pd.read_csv(os.path.join("data/Historico_Mastitis_Inversiones_Camacho-Vacas.csv"))
    df_reg_leche_lactx = pd.read_csv(os.path.join("data/Registros_de_Leche_Lactx.csv"))
    df_reg_leche_lactx['Id'] = df_reg_leche_lactx['Id'].astype(str)
    df_res_estado = pd.read_csv(os.path.join("data/Resumen_de_Estado.csv"))
    df_res_estado['Id'] = df_res_estado['Id'].astype(str)
    df_reg_peso_lact0 = pd.read_csv(os.path.join("data/Registro_de_Peso_Lact0.csv"))
    df_reg_peso_lact0['Id'] = df_reg_peso_lact0['Id'].astype(str)
    return df_sub, df_todos_los_datos, df_eventos_reg, df_reg_leche_lactx, df_mastitis_vacas, df_res_estado, df_reg_peso_lact0, df_todos_los_datos2, df_grupo

def df_lotes():
    df_seguimiento_hatos = pd.read_csv(os.path.join("data/seguimiento_hatos(Test).csv"))
    df_lag_lotes = pd.read_csv(os.path.join("data/lag_lotes(Test).csv"))
    return df_seguimiento_hatos, df_lag_lotes

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
#--------------------------------------------------------------------------------------------------------------------------------------------
  

#ESTILOS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server
app.config["suppress_callback_exceptions"] = True

#ELABORACION MAPA La Isla, Juncalito y Paraiso
mapbox_access_token = "pk.eyJ1IjoiYmxhY2thbmdlbGl0byIsImEiOiJja2NlN2Rhc2YwMmU5MnFtZ25rMDBwcWZoIn0.s3voGZglWzPU5OOZHYWjHw"

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
#--------------------------------------------------------------------------------------------------------------------------------------------


#DEFINICION FUNCIONES 
def elaboracion_encabezado():
    return [
    html.Div(
        [
        html.H1(
            children='DASHBOARD INVERSIONES CAMACHO-BORDA',
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
                        label="Control Fincas - Lotes",
                        value="tab1",
                        className="custom-tab",
                        selected_className="custom-tab--selected"
                    ),
                    dcc.Tab(
                        id="TAB2",
                        label="Control Hatos",
                        value="tab2",
                        className="custom-tab",
                        selected_className="custom-tab--selected"
                    ),
                    dcc.Tab(
                        id="TAB3",
                        label="Monitoreo de mi ganado",
                        value="tab3",
                        className="custom-tab",
                        selected_className="custom-tab--selected"
                    )
                ],style={'textAlign': 'center','color': colors['title'], 'font-size': '25px'}
            )
        ]
    )
    ]
#--------------------------------------------------------------------------------------------------------------------------------------------


#CONTRUCCION DE LAS PESTAÑAS DEL TABLERO
def elaboracion_tab_lotes():
    df_DB = table_DB().head(20)
    return [
        html.Div([
                html.Div([
                        html.Label('Seleccionar Finca'),
                        dcc.Dropdown(id="chart_dropdown_lotes",
                            options=[
                                {"label": "Finca La Isla", "value": "Finca_La_Isla"},
                                {"label": "Finca El Recodo", "value": "Finca_El_Recodo"}
                            ], value="Finca_La_Isla"   
                        )
                ], className="pretty_container six columns"
                ),
                html.Div([
                        html.Label('Seleccionar Variable'),
                        dcc.Dropdown(id="seleccion_variable_lotes",
                            options=[
                                {"label": "Índice de Vegetacion", "value": "NDVI"},
                                {"label": "Biomasa", "value": "Biomass"},
                                {"label": "Índice de Hoja", "value": "LAI"},
                                {"label": "Humedad", "value": "Moist"}
                            ], value="NDVI"
                        )
                ], className="pretty_container six columns"
                )
        ], className="row flex-display"
        ),
        
        html.Div([
                html.Div(
                    [dcc.Graph(id="Grafica_principal_lotes")],
                    className="pretty_container seven columns"
                ),
                html.Div(
                    [dcc.Graph(id="Grafica_datos_lotes")],
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


def elaboracion_tab_hatos():
    df_DB = table_DB().head(20)
    df_grupo = df_vacas()[8]
    df_todos_los_datos2 = df_vacas()[7]
    return [
        html.Div([
            html.Div([
                html.Label('Seleccionar Finca'),
                dcc.Dropdown(
                    id="chart_dropdown_hatos",
                    options=[
                        {"label": "Finca La Isla", "value": "Finca_La_Isla"},
                        {"label": "Finca El Recodo", "value": "Finca_El_Recodo"}
                    ], value="Finca_La_Isla"   
                )
            ], className="pretty_container six columns"
            ),
            html.Div([
                html.Label('Grupo - Hato'),
                dcc.Dropdown(
                    id='filtro_grupo_hato',
                    options=[{'label': i, 'value': i} for i in df_grupo],
                    value='R 1'
                )
            ], className="pretty_container six columns"
            ),
        ], className="row flex-display"
        ),
        
        html.Div([
            html.Div(
                [dcc.Graph(id="Grafica_principal_hatos")],
                className="pretty_container seven columns"
            ),
            html.Div(
                [dcc.Graph(id="ts_tab_hatos")],
                className="pretty_container five columns"
            )
        ], className="pretty_container twelve columns"
        ),
        
        html.Div([
            html.H2(children='INDICADORES DE HATOS')
        ], className="pretty_container twelve columns",
            style={'textAlign': 'center', 'height': '10%','width': '100%', 'backgroundColor':'#f7f7f7', 'border-style': 'solid', 'border-color': '#00A99E', 'margin-top': '10px', 'margin-bottom': '10px'}
        ),
        
        html.Div([
            html.Div([
                html.Div(
                    [daq.Gauge(
                        id="Ind_Mastitis",
                        label="Indicador Mastitis Prom/Vaca",
                        # size = 100,
                        showCurrentValue=True,
                        scale={'start': 0, 'interval': 0.5, 'labelInterval': 0.5},
                        color={"gradient": True, "ranges":{"green":[0,0.5],"yellow":[0.5,1], "orange":[1,1.5], "red":[1.5,2]}},
                        min=0,
                        max=2,
                        value=1
                    )
                    ], className="pretty_container five columns"
                ),
                html.Div([
                    html.Div(id="Top_vacas_mastitis")
                ], className="pretty_container seven columns",
                    style={'margin-top': '10px', 'margin-bottom': '10px'}
                ),
            ], className="pretty_container four columns"
            ),
            html.Div([
                html.Div(
                    [daq.Gauge(
                        id="Ind_Cojeras",
                        label="Indicador Cojeras Prom/Vaca",
                        # size = 100,
                        showCurrentValue=True,
                        scale={'start': 0, 'interval': 0.125, 'labelInterval': 0.125},
                        color={"gradient": True, "ranges":{"green":[0,0.125],"yellow":[0.125,0.25], "orange":[0.25,0.375], "red":[0.375,0.5]}},
                        min=0,
                        max=0.5,
                        value=0.25
                    )
                    ], className="pretty_container five columns"
                ),
                html.Div([
                    html.Div(id="Top_vacas_cojeras")
                ], className="pretty_container seven columns",
                    style={'margin-top': '10px', 'margin-bottom': '10px'}
                ),
            ], className="pretty_container four columns"
            ),
            html.Div([
                html.Div(
                    [daq.Gauge(
                        id="Ind_Abortos",
                        label="Indicador Abortos Prom/Vaca",
                        # size = 100,
                        showCurrentValue=True,
                        scale={'start': 0, 'interval': 0.5, 'labelInterval': 0.5},
                        color={"gradient": True, "ranges":{"green":[0,0.5],"yellow":[0.5,1], "orange":[1,1.5], "red":[1.5,2]}},
                        min=0,
                        max=2,
                        value=1
                    )
                    ], className="pretty_container five columns"
                ),
                html.Div([
                    html.Div(id="Top_vacas_abortos")
                ], className="pretty_container seven columns",
                    style={'margin-top': '10px', 'margin-bottom': '10px'}
                ),
            ], className="pretty_container four columns"
            ),
            
        ], className="pretty_container twelve columns"
        )
        
    ]

def elaboracion_tab_animales():
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
                                style={'height': '30%','width': '40%','margin-top': '5px', 'margin-bottom': '5px'}
                            ),
                            dbc.CardBody([
                                html.H4(id="DIM_vaca", className="card-title", style={'font-weight': 'bold'}),
                                html.P(id="Tercio_lactancia_vaca", className="card-title")
                            ]
                            )
                        ]
                        )
                    ], className="pretty_container four columns", 
                        style={'textAlign': 'center', 'height': '30%','width': '30%',} #'backgroundColor':'#f7f7f7', 'border-style': 'solid', 'border-color': '#00A99E'}
                    ),
                    
                    html.Div([
                        dbc.Card([
                            dbc.CardImg(
                                src= app.get_asset_url('milk.png'), 
                                top=True, 
                                style={'height': '30%','width': '40%','margin-top': '5px', 'margin-bottom': '5px'}
                            ),
                            dbc.CardBody([
                                html.H4(id="Leche_prom_mes_vaca", className="card-title", style={'font-weight': 'bold'}),
                                html.H5(id="Lt_lact_vs_hato_vaca", className="card-title"),
                                html.P("Lt  Lact. vs. hato", className="card-title")
                            ]
                            )
                        ]
                        )
                    ], className="pretty_container four columns", 
                        style={'textAlign': 'center', 'height': '30%','width': '30%',} #'backgroundColor':'#f7f7f7', 'border-style': 'solid', 'border-color': '#00A99E'}
                    ),
                    
                    html.Div([
                        dbc.Card([
                            dbc.CardImg(
                                src= app.get_asset_url('fertilization.png'), 
                                top=True, 
                                style={'height': '30%','width': '40%','margin-top': '5px', 'margin-bottom': '5px'}
                            ),
                            dbc.CardBody([
                                html.H4(id="Ultimo_diag_preñez_vaca", className="card-title", style={'font-weight': 'bold'}),
                                html.H5(id="Ultimo_resultado_vaca", className="card-title"),
                                html.P("Ult. Diag. Preñez", className="card-title")
                            ]
                            )
                        ]
                        )
                    ], className="pretty_container four columns", 
                        style={'textAlign': 'center', 'height': '30%','width': '30%',} #'backgroundColor':'#f7f7f7', 'border-style': 'solid', 'border-color': '#00A99E'}
                    )
                ], className="row"
                ),
                
                
                html.Div([
                    html.Div([
                        dbc.Card([
                            dbc.CardImg(
                                src= app.get_asset_url('ubre(1).png'), 
                                top=True, 
                                style={'height': '30%','width': '40%','margin-top': '5px', 'margin-bottom': '5px'}
                            ),
                            dbc.CardBody([
                                html.H4(id="Mast_vida_vaca", className="card-title", style={'font-weight': 'bold'}),
                                html.H5(id="Mast_activa_vaca", className="card-title")
                            ]
                            )
                        ]
                        )
                    ], className="pretty_container four columns", 
                        style={'textAlign': 'center', 'height': '30%','width': '30%',} #'backgroundColor':'#f7f7f7', 'border-style': 'solid', 'border-color': '#00A99E'}
                    ),
                    
                    html.Div([
                        dbc.Card([
                            dbc.CardImg(
                                src= app.get_asset_url('muletas.png'), 
                                top=True, 
                                style={'height': '30%','width': '40%','margin-top': '5px', 'margin-bottom': '5px'}
                            ),
                            dbc.CardBody([
                                html.H4(id="Cojera_vida_vaca", className="card-title", title=" Mes", style={'font-weight': 'bold'}),
                                html.H5(id="Cojera_activa_vaca", className="card-title")
                            ]
                            )
                        ]
                        )
                    ], className="pretty_container four columns", 
                        style={'textAlign': 'center', 'height': '30%','width': '30%',} #'backgroundColor':'#f7f7f7', 'border-style': 'solid', 'border-color': '#00A99E'}
                    ),
                    
                    html.Div([
                        dbc.Card([
                            dbc.CardImg(
                                src= app.get_asset_url('calf.png'), 
                                top=True, 
                                style={'height': '30%','width': '40%','margin-top': '5px', 'margin-bottom': '5px'}
                            ),
                            dbc.CardBody([
                                html.H4(id="No_crias_vaca", className="card-title", style={'font-weight': 'bold'}),
                                html.H5(id="Int_entre_partos_vaca", className="card-title"),
                                html.P("Intervalo entre partos", className="card-title")
                            ]
                            )
                        ]
                        )
                    ], className="pretty_container four columns", 
                        style={'textAlign': 'center', 'height': '30%','width': '30%',} #'backgroundColor':'#f7f7f7', 'border-style': 'solid', 'border-color': '#00A99E'}
                    )
                ], className="row"
                )
                
        ], className="pretty_container six columns"
        ),    
         
        
        html.Div([
            html.Div([
                dash_table.DataTable(
                    id='tablaEventosRegistrados_vaca',
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
                style={'margin-top': '10px', 'margin-bottom': '10px'}
            )   
        ], className="pretty_container six columns"
        ), 

        html.Div([
            html.H2(children='CURVA DE PRODUCCIÓN, MONITOREO DE PESO Y RESUMEN DE ESTADO')
        ], className="pretty_container twelve columns",
            style={'textAlign': 'center', 'height': '10%','width': '100%', 'backgroundColor':'#f7f7f7', 'border-style': 'solid', 'border-color': '#00A99E', 'margin-top': '10px', 'margin-bottom': '10px'}
        ),

        html.Div([            
            html.Div([
                dcc.Graph(id="Leche(lact)_Peso_Concentrado")
            ], className="pretty_container six columns",
                style={'margin-top': '10px', 'margin-bottom': '10px'}
            ),
            
            html.Div([
                html.Div(id="Resumen_Estado_Vaca")
            ], className="pretty_container six columns",
                style={'margin-top': '10px', 'margin-bottom': '10px'}
            )
        ], className="pretty_container twelve columns"
        ),
        
        html.Div([
            html.H2(children='CONTROL DE MASTITIS')
        ], className="pretty_container twelve columns",
            style={'textAlign': 'center', 'height': '10%','width': '100%', 'backgroundColor':'#f7f7f7', 'border-style': 'solid', 'border-color': '#00A99E'}
        ),

        html.Div([            
            html.Div([
                dcc.Graph(id="%_ubre_sana_vs_%_calificacion_vaca")
            ], className="pretty_container six columns",
                style={'margin-top': '10px', 'margin-bottom': '10px'}
            ),
            
            html.Div([
                dcc.Graph(id="calificacion_pezon_vaca")
            ], className="pretty_container six columns",
                style={'margin-top': '10px', 'margin-bottom': '10px'}
            )
        ], className="pretty_container twelve columns"
        )
    ]
#--------------------------------------------------------------------------------------------------------------------------------------------


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
#--------------------------------------------------------------------------------------------------------------------------------------------


#Este es un callback que cambia entre TABs
@app.callback(
    Output("app-content", "children"),
    [Input("app-tabs", "value")]
)
def render_tab_content(tab_switch):
    if tab_switch == "tab1":
        return elaboracion_tab_lotes()
    if tab_switch == "tab2":
        return elaboracion_tab_hatos()
    if tab_switch == "tab3":
        return elaboracion_tab_animales()
#--------------------------------------------------------------------------------------------------------------------------------------------

#TAB LOTES
#Elaboración de Grafico de mapa de variables Satelitales por lote-Finca
@app.callback(Output("Grafica_principal_lotes", "figure"),
              [Input("chart_dropdown_lotes", "value"),
               Input("seleccion_variable_lotes", "value")])
def mapa_tab_lotes(chart_dropdown_lotes, seleccion_variable_lotes):
    def color_variable_lotes():
        if seleccion_variable_lotes == 'NDVI':
            return 'Índice de Vegetación'
        if seleccion_variable_lotes == 'Biomass':
            return 'Biomasa'
        if seleccion_variable_lotes == 'LAI':
            return 'Índice de Hoja'
        if seleccion_variable_lotes == 'Moist':
            return 'Humedad'
    
    def color_scale_lotes():
        if seleccion_variable_lotes == 'NDVI':
            return 'RdYlGn'
        if seleccion_variable_lotes == 'Biomass':
            return 'Viridis'
        if seleccion_variable_lotes == 'LAI':
            return 'speed'
        if seleccion_variable_lotes == 'Moist':
            return 'tempo'
        
    def mapa_isla_tab_lotes():
        df, df_merge = graficas_all()
        mapa_isla_tab1 = px.choropleth_mapbox(
            df,
            geojson=j_file_complete,
            color=color_variable_lotes(),
            locations="Lote", 
            featureidkey="properties.name",
            center={"lat": 5.534985, "lon": -73.796751},
            mapbox_style="satellite", 
            zoom=14.2,
            color_continuous_scale=color_scale_lotes(),
            hover_data={"Lote": True, "Área": True, "Índice de Vegetación": True, "Biomasa": True, "Índice de Hoja": True, "Humedad": True, "mean_value._NDVI": False}
        )
        
        mapa_isla_tab1.update_geos(fitbounds="locations", visible=True)
        
        mapa_isla_tab1.update_layout(
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
        return mapa_isla_tab1
    
    def mapa_recodo_tab_lotes():
        df, df_merge = graficas_all()
        mapa_recodo_tab1 = px.choropleth_mapbox(
            df,
            geojson=j_file3, 
            color=color_variable_lotes(),
            locations="Lote", 
            featureidkey="properties.name",
            center={"lat": 5.497800, "lon": -73.775426},
            mapbox_style="satellite",
            zoom=14.2,
            color_continuous_scale=color_scale_lotes(),
            hover_data={"Lote": True, "Área": True, "Índice de Vegetación": True, "Biomasa": True, "Índice de Hoja": True, "Humedad": True, "mean_value._NDVI": False}
        )
        
        mapa_recodo_tab1.update_geos(fitbounds="locations", visible=True)
        
        mapa_recodo_tab1.update_layout(
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
        return mapa_recodo_tab1
    
    if chart_dropdown_lotes == "Finca_La_Isla":
        Grafica_principal_lotes = mapa_isla_tab_lotes()
    elif chart_dropdown_lotes == "Finca_El_Recodo":
        Grafica_principal_lotes = mapa_recodo_tab_lotes()
    return Grafica_principal_lotes

#Elaboración de Grafico en linea de Tiempo de variables Satelitales por lote
@app.callback(Output("Grafica_datos_lotes", "figure"), 
              [Input("Grafica_principal_lotes", "selectedData")])
def ts_variables_lotes(Grafica_principal_lotes_click):
    df, df_merge = graficas_all()
    if Grafica_principal_lotes_click is None:
        lote_name = ['Vista Completa']
    else:
        lote_name = Grafica_principal_lotes_click['points'][0]['customdata']
        lote_name = lote_name[0].split()
    
    if lote_name[0] == 'Vista Completa':
        df_grouped = df_merge.groupby(['Fecha']).agg(mean_NDVI=('mean_value._NDVI',"mean"),mean_BM=('biomass_corrected',"mean"),mean_LAI=('mean_value._LAI',"mean"),mean_MOIST=('mean_value._MOIST',"mean")).reset_index()
    else:
        df_grouped = df_merge.groupby(['Fecha','name']).agg(mean_NDVI=('mean_value._NDVI',"mean"),mean_BM=('biomass_corrected',"mean"),mean_LAI=('mean_value._LAI',"mean"),mean_MOIST=('mean_value._MOIST',"mean")).reset_index()
        df_grouped = df_grouped[df_grouped['name']== lote_name[0]]
        
    ts_tab_lotes = make_subplots(specs=[[{"secondary_y": True}]])
    
    ts_tab_lotes.add_trace(
        go.Scatter(x=df_grouped['Fecha'], y=df_grouped['mean_NDVI'], name="NDVI"),
        secondary_y=False
    )
    ts_tab_lotes.add_trace(
        go.Scatter(x=df_grouped['Fecha'], y=df_grouped['mean_LAI'], name="LAI"),
        secondary_y=False
    )
    ts_tab_lotes.add_trace(
        go.Scatter(x=df_grouped['Fecha'], y=df_grouped['mean_MOIST'], name="MOIST"),
        secondary_y=False
    )
    ts_tab_lotes.add_trace(
        go.Scatter(x=df_grouped['Fecha'], y=df_grouped['mean_BM'], name="BIOMASA"),
        secondary_y=True
    )
    
    ts_tab_lotes.update_layout(
        title_text="Datos Históricos"
    )
    
    ts_tab_lotes.update_xaxes(zeroline=True, gridcolor='Grey', zerolinewidth=2, zerolinecolor='#00A99E', title_text='Fecha')
    
    ts_tab_lotes.update_layout(
        title_text=lote_name[0],
        autosize = True,
        paper_bgcolor=colors['background'],
        margin=dict(t=70, r=30, b=40, l=0),
        plot_bgcolor = '#ffffff',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis = dict(tickangle= -45),
        yaxis = dict(automargin= True)
    )    
    return ts_tab_lotes


#Tabla de registros por lote (db_potreros)
@app.callback(Output("tablaDBpotreros", "data"), 
              [Input("Grafica_principal_lotes", "selectedData")])
    
def table_evt_lotes(Grafica_principal_lotes_click):
    df_DB = table_DB()
    if Grafica_principal_lotes_click is None:
        lote_name = ['Vista Completa']
    else:
        lote_name = Grafica_principal_lotes_click['points'][0]['customdata']
        lote_name = lote_name[0].split()
    
    if lote_name[0] == 'Vista Completa':
        df_DB = df_DB.copy()
    else:
        df_DB = df_DB[df_DB['NAME']== lote_name[0]]
    df_DB = df_DB.head(20)
    return df_DB.to_dict('records')

#Elaboración de Gráfico Top 5 lotes cercanos
@app.callback(Output("Grafica_Top", "figure"), 
              [Input("Grafica_principal_lotes", "selectedData")])
def top_lotes(Grafica_principal_lotes_click):
    DB_lotes_cercanos, df, df_merge = lotes_cercanos()
    if Grafica_principal_lotes_click is None:
        lote_name = ['Vista Completa']
    else:
        lote_name = Grafica_principal_lotes_click['points'][0]['customdata']
        lote_name = lote_name[0].split()
    
    if lote_name[0] == 'Vista Completa':
        df_top = df.nlargest(5,'mean_value._NDVI')
    else:
        df_top = df.nlargest(5,'mean_value._NDVI')
        DB_lotes_cercanos= DB_lotes_cercanos.loc[:,[lote_name[0]]]
        df_top = df[df['name']== DB_lotes_cercanos]
    
    top5_lotes_tab_lotes = px.bar(df_top, x='name', y='mean_value._NDVI')
    
    top5_lotes_tab_lotes.update_layout(
        title_text="Top Mejores Lotes Para Traslado de Ganado por NDVI",
        autosize = True,
        paper_bgcolor=colors['background'],
        margin=dict(t=70, r=30, b=40, l=0),
        plot_bgcolor = '#ffffff',
        legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
        xaxis = dict(tickangle= -90),
        yaxis = dict(automargin= True)
    )   
    return top5_lotes_tab_lotes
#--------------------------------------------------------------------------------------------------------------------------------------------


#TAB 2
#Elaboración de Grafico de mapa de variables Satelitales por lote-Finca
@app.callback(Output("Grafica_principal_hatos", "figure"),
              [Input("chart_dropdown_hatos", "value")])
def mapa_tab_hatos(chart_dropdown_hatos):
    def mapa_isla_tab_hatos():
        df_seguimiento_hatos = df_lotes()[1]
        df_seguimiento_hatos = df_seguimiento_hatos[df_seguimiento_hatos['HATO']<'REC']
        df_seguimiento_hatos = df_seguimiento_hatos[df_seguimiento_hatos['date']>='2020-04-01']
        mapa_isla_tab2 = px.choropleth_mapbox(
            df_seguimiento_hatos,
            geojson=j_file_complete,
            color='HATO_C',
            locations="value", 
            featureidkey="properties.name",
            center={"lat": 5.534985, "lon": -73.796751},
            mapbox_style="satellite", 
            zoom=13.8,
            animation_frame="date",
            hover_data={"value": True, "TIPO DE FORRAJE": True, "NUMERO ANIMALES": True},
            color_discrete_map={
                "ISLA": '#005b5c', "ISLA_1": '#058d8d', "ISLA_2": '#53bebd', "ISLA_3": '#89f2f0',
                "JUNCAL": '#0a3c90', "JUNCAL_1": '#4f64bf', "JUNCAL_2": '#8290f1', "JUNCAL_3": '#b9c3ff',
                "PARAISO": '#930b07', "PARAISO_1": '#c2402b', "PARAISO_2": '#f26a4f', "PARAISO_3": '#ffa888'
            }
        )
        
        mapa_isla_tab2.update_geos(fitbounds="locations", visible=True)
        
        mapa_isla_tab2.update_layout(
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
        return mapa_isla_tab2
    
    def mapa_recodo_tab_hatos():
        df_seguimiento_hatos = df_lotes()[1]
        df_seguimiento_hatos = df_seguimiento_hatos[df_seguimiento_hatos['HATO']>='PEC']
        df_seguimiento_hatos = df_seguimiento_hatos[df_seguimiento_hatos['date']>='2020-04-01']
        mapa_recodo_tab2 = px.choropleth_mapbox(
            df_seguimiento_hatos,
            geojson=j_file3, 
            color="HATO_C",
            locations="value", 
            featureidkey="properties.name",
            center={"lat": 5.497800, "lon": -73.775426},
            mapbox_style="satellite",
            zoom=13.6,
            animation_frame="date",
            #hover_data={"name": True, "TIPO DE FORRAJE": True, "NUMERO ANIMALES": True},
            color_discrete_map={
                "RECODO 1": '#005c02', "RECODO 1_1": '#068e2c', "RECODO 1_2": '#51bf5a', "RECODO 1_3": '#86f389',
                "RECODO 2": '#6f0c94', "RECODO 2_1": '#9d43c1', "RECODO 2_2": '#cd71f1', "RECODO 2_3": '#ffa5ff',
                "RECODO 3": '#8c3300', "RECODO 3_1": '#bf5d00', "RECODO 3_2": '#f28a2e', "RECODO 3_3": '#ffc96f'
            }
        )
        
        mapa_recodo_tab2.update_geos(fitbounds="locations", visible=True)
        
        mapa_recodo_tab2.update_layout(
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
        return mapa_recodo_tab2

    if chart_dropdown_hatos == "Finca_La_Isla":
        Grafica_principal_hatos = mapa_isla_tab_hatos()
    elif chart_dropdown_hatos == "Finca_El_Recodo":
        Grafica_principal_hatos = mapa_recodo_tab_hatos()
    return Grafica_principal_hatos

#Elaboración de gráfico en series de tiempo de producción de leche por hato, click por lote
@app.callback(Output("ts_tab_hatos", "figure"), 
              [Input("Grafica_principal_hatos", "selectedData")])
def ts_variables_hatos(Grafica_principal_hatos_click):
    df_seguimiento_hatos = df_lotes()[0]

    if Grafica_principal_hatos_click is None:
        lote_name = ['Vista Completa']
    else:
        lote_name = Grafica_principal_hatos_click['points'][0]['customdata']
        lote_name = lote_name[0].split()

    if lote_name[0] == 'Vista Completa':
        produccion_leche = df_seguimiento_hatos.copy()
    else:
        produccion_leche = df_seguimiento_hatos[df_seguimiento_hatos['name']== lote_name[0]]    
    
    ts_tab_hatos = px.line(produccion_leche, x='date', y='LECHE TOTAL', color='HATO')
        
    ts_tab_hatos.update_xaxes(zeroline=True, gridcolor='Grey', zerolinewidth=2, zerolinecolor='#00A99E', title_text='Fecha')
    ts_tab_hatos.update_yaxes(gridcolor='Grey')
    
    ts_tab_hatos.update_layout(
        title_text="Producción de Leche por fecha-Hato " + lote_name[0],
        autosize = True,
        paper_bgcolor=colors['background'],
        margin=dict(t=70, r=30, b=40, l=0),
        plot_bgcolor = '#ffffff',
        legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
        xaxis = dict(tickangle= -45),
        yaxis = dict(automargin= True)
    )    
    return ts_tab_hatos

#Elaboración de Gauge Mastitis Promedio por Vaca dentro de Hato
@app.callback([Output("Ind_Mastitis", "value"),
              Output("Ind_Cojeras", "value"),
              Output("Ind_Abortos", "value")],
              [Input("filtro_grupo_hato", "value")])
def ind_mast(filtro_grupo_hato):
    df_todos_los_datos2 = df_vacas()[7]
    df_todos_los_datos2 = df_todos_los_datos2[df_todos_los_datos2['Grupo'] == filtro_grupo_hato]
    ind_mastitis = df_todos_los_datos2['Mast. vida'].mean()
    ind_cojeras = df_todos_los_datos2['Cojera vida'].mean()
    ind_abortos = df_todos_los_datos2['No. abo (vida)'].mean()
    return (ind_mastitis, ind_cojeras, ind_abortos)

#Elaboración Top Vacas con Mastitis
@app.callback(Output("Top_vacas_mastitis", "children"), 
              [Input("filtro_grupo_hato", 'value')])
def generate_tabla_top_mastitis(filtro_tabla_top_mastitis):
    df_top_mastitis = df_vacas()[1]
    df_top_mastitis = df_top_mastitis[['ID', 'Grupo', 'Edad', 'Mast. vida', 'Mast_activa']].copy()
    df_top_mastitis = df_top_mastitis.sort_values('Mast. vida', ascending=False)
    tabla_top_mastitis = df_top_mastitis[df_top_mastitis['Grupo'] == filtro_tabla_top_mastitis]
    return html.Div([
                dash_table.DataTable(
                    columns=[{"name": i, "id": i} for i in tabla_top_mastitis.columns],
                    data = tabla_top_mastitis.to_dict('records')[0:8],
                    page_current=0,
                    page_size=8,
                    page_action='custom',
                    style_table={'overflowX': 'auto'},
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                        },
                    ],
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold',
                        'whiteSpace': 'normal',
                        'height': 'auto'
                    }
                )
    ])

#Elaboración Top Vacas con Cojeras
@app.callback(Output("Top_vacas_cojeras", "children"), 
              [Input("filtro_grupo_hato", 'value')])
def generate_tabla_top_cojeras(filtro_tabla_top_cojeras):
    df_top_cojeras = df_vacas()[1]
    df_top_cojeras = df_top_cojeras[['ID', 'Grupo', 'Edad', 'Cojera vida', 'Cojera_activa']].copy()
    df_top_cojeras = df_top_cojeras.sort_values(by=['Cojera vida', 'Edad'], ascending=False)
    tabla_top_cojeras = df_top_cojeras[df_top_cojeras['Grupo'] == filtro_tabla_top_cojeras]
    return html.Div([
                dash_table.DataTable(
                    columns=[{"name": i, "id": i} for i in tabla_top_cojeras.columns],
                    data = tabla_top_cojeras.to_dict('records')[0:8],
                    page_current=0,
                    page_size=8,
                    page_action='custom',
                    style_table={'overflowX': 'auto'},
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                        },
                    ],
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold',
                        'whiteSpace': 'normal',
                        'height': 'auto'
                    }
                )
    ])

#Elaboración Top Vacas con Abortos
@app.callback(Output("Top_vacas_abortos", "children"), 
              [Input("filtro_grupo_hato", 'value')])
def generate_tabla_top_abortos(filtro_tabla_top_abortos):
    df_top_abortos = df_vacas()[1]
    df_top_abortos = df_top_abortos[['ID', 'Grupo', 'Edad', 'No. abo (vida)', 'No. crías']].copy()
    df_top_abortos = df_top_abortos.sort_values(by=['No. abo (vida)', 'Edad'], ascending=False)
    tabla_top_abortos = df_top_abortos[df_top_abortos['Grupo'] == filtro_tabla_top_abortos]
    return html.Div([
                dash_table.DataTable(
                    columns=[{"name": i, "id": i} for i in tabla_top_abortos.columns],
                    data = tabla_top_abortos.to_dict('records')[0:8],
                    page_current=0,
                    page_size=8,
                    page_action='custom',
                    style_table={'overflowX': 'auto'},
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                        },
                    ],
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold',
                        'whiteSpace': 'normal',
                        'height': 'auto'
                    }
                )
    ])
#--------------------------------------------------------------------------------------------------------------------------------------------


#TAB 3
#Elaboración tabla eventos e Indicadores por animal
@app.callback(Output("tablaEventosRegistrados_vaca", "data"), 
              [Input("filtro_vaca", 'value'),
               Input('tablaEventosRegistrados_vaca', "page_current"),
               Input('tablaEventosRegistrados_vaca', "page_size")])
def generate_tabla_ev_vacas(filtro_tabla_ev_vacas,page_current,page_size):
    df_eventos_reg = df_vacas()[2]
    tabla_ev_vacas = df_eventos_reg[df_eventos_reg['Id'] == filtro_tabla_ev_vacas]
    return tabla_ev_vacas.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')[0:25]

@app.callback([Output("ID_vaca", "children"),
               Output("Estado_vaca", "children"),
               Output("Edad_vaca", "children"),
               Output("Raza_vaca", "children"),
               Output("Sexo/tipo_vaca", "children"),
               Output("DIM_vaca", "children"), 
               Output("Tercio_lactancia_vaca", "children"),
               Output("Leche_prom_mes_vaca", "children"),
               Output("Lt_lact_vs_hato_vaca", "children"),
               Output("Ultimo_diag_preñez_vaca", "children"),
               Output("Ultimo_resultado_vaca", "children"),
               Output("Mast_vida_vaca", "children"),
               Output("Mast_activa_vaca", "children"),
               Output("Cojera_vida_vaca", "children"),
               Output("Cojera_activa_vaca", "children"),
               Output("No_crias_vaca", "children"),
               Output("Int_entre_partos_vaca", "children")],
              [Input("filtro_vaca", 'value')])
def generate_indicadores_vaca(filtro_id_indicadores_vaca):
    df_todos_los_datos = df_vacas()[1]
    id_indicadores_vacas = df_todos_los_datos[df_todos_los_datos['Numero'] == filtro_id_indicadores_vaca]
    return (id_indicadores_vacas["ID"],
            id_indicadores_vacas["Estado"],
            id_indicadores_vacas["Edad"],
            id_indicadores_vacas["Raza"],
            id_indicadores_vacas["Sexo/ tipo"],
            id_indicadores_vacas["DIM_c"],
            id_indicadores_vacas["Tercio lactancia (groups)"],
            id_indicadores_vacas["Leche_prom_mes_c"],
            id_indicadores_vacas["Lt Lact. vs.hato_C"],
            id_indicadores_vacas["Ult. diag. preñez"],
            id_indicadores_vacas["Ult. resultado"],
            id_indicadores_vacas["Mast_vida"],
            id_indicadores_vacas["Mast_activa"],
            id_indicadores_vacas["Cojera_vida"],
            id_indicadores_vacas["Cojera_activa"],
            id_indicadores_vacas["No_crias"],
            id_indicadores_vacas["Int_entre_partos"])

#Elaboración de gráfico en series de tiempo de ubre y calificación por mastitis
@app.callback(Output("Leche(lact)_Peso_Concentrado", "figure"), 
              [Input("filtro_vaca", 'value')])
def ts_leche_conc(filtro_leche_conc):
    df_reg_leche_lactx = df_vacas()[3]
    df_eventos_reg = df_vacas()[2]
    df_reg_peso_lact0 = df_vacas()[6]
    
    prod_leche_conc_lact = df_reg_leche_lactx[df_reg_leche_lactx['Id'] == filtro_leche_conc]
    peso_vaca = df_reg_peso_lact0[df_reg_peso_lact0['Id'] == filtro_leche_conc]
    
    min_fecha = min(prod_leche_conc_lact['Fecha'])
    
    # def min_fecha():
    #     if min(prod_leche_conc_lact['Fecha']) != None:
    #         min_fecha_ = min(prod_leche_conc_lact['Fecha'])
    #     else:
    #         min_fecha_ = min(peso_vaca['Fecha'])
    #     return min_fecha_
    
    evt_vaca = df_eventos_reg[df_eventos_reg['Id'] == filtro_leche_conc]
    evt_vaca = evt_vaca[evt_vaca['Fecha'] >= min_fecha]
        
    ts_leche_conc_lact = go.Figure()
    
    ts_leche_conc_lact.add_trace(
        go.Scatter(x=prod_leche_conc_lact['Fecha'], y=prod_leche_conc_lact['Día kg'], name="Leche kg", line=dict(width=2))
    )
    ts_leche_conc_lact.add_trace(
        go.Bar(x=prod_leche_conc_lact['Fecha'], y=prod_leche_conc_lact['Conc.'], name="Concentrado kg")
    )
    ts_leche_conc_lact.add_trace(
        go.Scatter(x=evt_vaca['Fecha'], y=evt_vaca['Evento(0)'], text=evt_vaca['Evento'], name="Evento", textposition='top center', mode="markers+text")
    )
    ts_leche_conc_lact.add_trace(
        go.Scatter(x=peso_vaca['Fecha'], y=peso_vaca['Peso'], name="Peso kg", line=dict(width=2))
    )

    ts_leche_conc_lact.update_xaxes(zeroline=True, gridcolor='Grey', zerolinewidth=2, zerolinecolor='#00A99E', title_text='Fecha')
    ts_leche_conc_lact.update_yaxes(gridcolor='Grey', ticksuffix="kg")
    
    ts_leche_conc_lact.update_layout(
        autosize = True,
        paper_bgcolor=colors['background'],
        margin=dict(t=70, r=30, b=40, l=0),
        plot_bgcolor = '#ffffff',
        title_text="CURVA DE PRODUCCIÓN DE LECHE - "+ min(prod_leche_conc_lact['Lactancia']),
        legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
        xaxis = dict(tickangle= -45),
        yaxis = dict(automargin= True)
    )    
    return ts_leche_conc_lact

#Elaboración tabla Resumen de Estado por Animal
@app.callback(Output("Resumen_Estado_Vaca", "children"), 
              [Input("filtro_vaca", 'value')])
def generate_tabla_res_estado(filtro_tabla_res_estado):
    df_res_estado = df_vacas()[5]
    tabla_res_estado = df_res_estado[df_res_estado['Id'] == filtro_tabla_res_estado]
    return html.Div([
                dash_table.DataTable(
                    columns=[{"name": i, "id": i} for i in tabla_res_estado.columns],
                    data = tabla_res_estado.to_dict('records'),
                    page_current=0,
                    page_action='custom',
                    style_table={'overflowX': 'auto'},
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                        },
                        {
                            'if': {
                                'filter_query': '{Int.} > 305 && {Int.} < 400',
                                'column_id': 'Int.'
                            },
                            'backgroundColor': '#FFDC00',
                            'color': 'white'
                        },
                        {
                            'if': {
                                'filter_query': '{Int.} >= 400 && {Int.} < 800',
                                'column_id': 'Int.'
                            },
                            'backgroundColor': '#FF4136',
                            'color': 'white'
                        },
                        {
                            'if': {
                                'filter_query': '{No. Mast} >= 1',
                                'column_id': 'No. Mast'
                            },
                            'fontWeight': 'bold',
                            'color': '#FFDC00'
                        },
                        {
                            'if': {
                                'filter_query': '{No. Abort.} >= 1',
                                'column_id': 'No. Abort.'
                            },
                            'fontWeight': 'bold',
                            'color': '#FF4136'
                        }
                    ] + 
                    [
                        {
                            'if': {
                                'filter_query': '{{Leche acum.}} = {}'.format(tabla_res_estado['Leche acum.'].max()),
                                'column_id': 'Leche acum.'
                            },
                            'backgroundColor': '#2ECC40',
                            'color': 'white'
                        },
                        {
                            'if': {
                                'filter_query': '{{Leche acum.}} = {}'.format(tabla_res_estado['Leche acum.'].min()),
                                'column_id': 'Leche acum.'
                            },
                            'backgroundColor': '#FF4136',
                            'color': 'white'
                        },
                        {
                            'if': {
                                'filter_query': '{{Leche/ día}} = {}'.format(tabla_res_estado['Leche/ día'].max()),
                                'column_id': 'Leche/ día'
                            },
                            'backgroundColor': '#2ECC40',
                            'color': 'white'
                        },
                        {
                            'if': {
                                'filter_query': '{{Leche/ día}} = {}'.format(tabla_res_estado['Leche/ día'].min()),
                                'column_id': 'Leche/ día'
                            },
                            'backgroundColor': '#FF4136',
                            'color': 'white'
                        },
                        {
                            'if': {
                                'filter_query': '{{Conc/ leche}} = {}'.format(tabla_res_estado['Conc/ leche'].max()),
                                'column_id': 'Conc/ leche'
                            },
                            'backgroundColor': '#FF4136',
                            'color': 'white'
                        },
                        {
                            'if': {
                                'filter_query': '{{Conc/ leche}} = {}'.format(tabla_res_estado['Conc/ leche'].min()),
                                'column_id': 'Conc/ leche'
                            },
                            'backgroundColor': '#2ECC40',
                            'color': 'white'
                        }
                    ],
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold',
                        'whiteSpace': 'normal',
                        'height': 'auto'
                    }
                )
    ]
    )


#Elaboración de gráfico en series de tiempo de ubre y calificación por mastitis
@app.callback(Output("%_ubre_sana_vs_%_calificacion_vaca", "figure"), 
              [Input("filtro_vaca", 'value')])
def ts_ubre_sana_vs_calif(filtro_ubre_sana_vs_calif_vacas):
    df_mastitis_vacas = df_vacas()[4]
    ubre_sana_vs_calif_vacas = df_mastitis_vacas[df_mastitis_vacas['NOMBRE'] == filtro_ubre_sana_vs_calif_vacas]
    
    ts_ubre_tab_animales = go.Figure()
    
    ts_ubre_tab_animales.add_trace(
        go.Scatter(x=ubre_sana_vs_calif_vacas['FECHA CHEQUEO'], y=ubre_sana_vs_calif_vacas['UBRE SANA']*100, name="% Ubre Sana", line=dict(width=2))
    )
    ts_ubre_tab_animales.add_trace(
        go.Scatter(x=ubre_sana_vs_calif_vacas['FECHA CHEQUEO'], y=ubre_sana_vs_calif_vacas['CAL. UBRE']*100, name="% Cal. Ubre", line=dict(width=2))
    )
    
    ts_ubre_tab_animales.update_xaxes(zeroline=True, gridcolor='Grey', zerolinewidth=2, zerolinecolor='#00A99E', title_text='Fecha de Chequeo')
    ts_ubre_tab_animales.update_yaxes(gridcolor='Grey', ticksuffix="%")
    
    ts_ubre_tab_animales.update_layout(
        autosize = True,
        paper_bgcolor=colors['background'],
        margin=dict(t=70, r=30, b=40, l=0),
        plot_bgcolor = '#ffffff',
        title_text="% UBRE SANA VS % CALIFICACIÓN",
        legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
        xaxis = dict(tickangle= -45),
        yaxis = dict(automargin= True)
    )    
    return ts_ubre_tab_animales

#Elaboración de gráfico en series de tiempo de calificación por pezón
@app.callback(Output("calificacion_pezon_vaca", "figure"), 
              [Input("filtro_vaca", 'value')])
def ts_calif_pezon(filtro_calif_pezon_vacas):
    df_mastitis_vacas = df_vacas()[4]
    calif_pezon_vacas = df_mastitis_vacas[df_mastitis_vacas['NOMBRE'] == filtro_calif_pezon_vacas]
    
    ts_calif_pezon_tab_animales = go.Figure()
    
    ts_calif_pezon_tab_animales.add_trace(
        go.Bar(x=calif_pezon_vacas['FECHA CHEQUEO'], y=calif_pezon_vacas['AI'], name="Pezón AI", hovertext=calif_pezon_vacas['Observación'])
    )
    ts_calif_pezon_tab_animales.add_trace(
        go.Bar(x=calif_pezon_vacas['FECHA CHEQUEO'], y=calif_pezon_vacas['AD'], name="Pezón AD", hovertext=calif_pezon_vacas['Observación'])
    )
    ts_calif_pezon_tab_animales.add_trace(
        go.Bar(x=calif_pezon_vacas['FECHA CHEQUEO'], y=calif_pezon_vacas['PI'], name="Pezón PI", hovertext=calif_pezon_vacas['Observación'])
    )
    ts_calif_pezon_tab_animales.add_trace(
        go.Bar(x=calif_pezon_vacas['FECHA CHEQUEO'], y=calif_pezon_vacas['PD'], name="Pezón PD", hovertext=calif_pezon_vacas['Observación'])
    )
    
    ts_calif_pezon_tab_animales.update_xaxes(zeroline=True, gridcolor='Grey', title_text='Fecha de Chequeo')
    ts_calif_pezon_tab_animales.update_yaxes(gridcolor='Grey')
    
    ts_calif_pezon_tab_animales.update_layout(
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
    return ts_calif_pezon_tab_animales          
#--------------------------------------------------------------------------------------------------------------------------------------------


app.layout = app_layout

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader = True)