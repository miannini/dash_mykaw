# -*- coding: utf-8 -*-
'''
Created on Fri Aug 14 08:38:35 2020

@author: Nickair90
'''
#pip install xlrd

import pandas as pd
import datetime as dt
import numpy as np

import os
from datetime import timedelta
from datetime import date


import glob


#Lectura de Todos los datos
df_todos_los_datos = pd.read_csv('data/Raw_data/Todos_los_datos.txt', sep='\t', engine='python', thousands='.', decimal =',')

#Reconocimiento de Fechas
df_todos_los_datos['Nacimiento'] = pd.to_datetime(df_todos_los_datos['Nacimiento'], format='%d/%m/%Y').dt.date
df_todos_los_datos['Destete'] = pd.to_datetime(df_todos_los_datos['Destete'], format='%d/%m/%Y', exact=False).dt.date
df_todos_los_datos['Fecha ultimo peso'] = pd.to_datetime(df_todos_los_datos['Fecha ultimo peso'], format='%d/%m/%Y', exact=False).dt.date
df_todos_los_datos['Ult. parto'] = pd.to_datetime(df_todos_los_datos['Ult. parto'], format='%d/%m/%Y', exact=False).dt.date
df_todos_los_datos['1er. celo'] = pd.to_datetime(df_todos_los_datos['1er. celo'], format='%d/%m/%Y', exact=False).dt.date
df_todos_los_datos['Ult. celo'] = pd.to_datetime(df_todos_los_datos['Ult. celo'], format='%d/%m/%Y', exact=False).dt.date
df_todos_los_datos['1er ser'] = pd.to_datetime(df_todos_los_datos['1er ser'], format='%d/%m/%Y', exact=False).dt.date
df_todos_los_datos['Ult. servicio'] = pd.to_datetime(df_todos_los_datos['Ult. servicio'], format='%d/%m/%Y', exact=False).dt.date
df_todos_los_datos['Ult. diag. preñez'] = pd.to_datetime(df_todos_los_datos['Ult. diag. preñez'], format='%d/%m/%Y', exact=False).dt.date
df_todos_los_datos['Concepción'] = pd.to_datetime(df_todos_los_datos['Concepción'], format='%d/%m/%Y', exact=False).dt.date
df_todos_los_datos['Destete.1'] = pd.to_datetime(df_todos_los_datos['Destete.1'], format='%d/%m/%Y', exact=False).dt.date
df_todos_los_datos['Secado'] = pd.to_datetime(df_todos_los_datos['Secado'], format='%d/%m/%Y', exact=False).dt.date
df_todos_los_datos['Fecha últ. leche'] = pd.to_datetime(df_todos_los_datos['Fecha últ. leche'], format='%d/%m/%Y', exact=False).dt.date
df_todos_los_datos['Próximo parto '] = pd.to_datetime(df_todos_los_datos['Próximo parto '], format='%d/%m/%Y', exact=False).dt.date
df_todos_los_datos['Inicio servicio'] = pd.to_datetime(df_todos_los_datos['Inicio servicio'], format='%d/%m/%Y', exact=False).dt.date
df_todos_los_datos['Ult. aborto'] = pd.to_datetime(df_todos_los_datos['Ult. aborto'], format='%d/%m/%Y', exact=False).dt.date
df_todos_los_datos['Ult. cond. corporal'] = pd.to_datetime(df_todos_los_datos['Ult. cond. corporal'], format='%d/%m/%Y', exact=False).dt.date

#Porcentajes en strings como floats
df_todos_los_datos['Leche vida vs.hato'] = df_todos_los_datos['Leche vida vs.hato'].str.rstrip('%').astype('float')
df_todos_los_datos['Lt  Lact. vs.hato'] = df_todos_los_datos['Lt  Lact. vs.hato'].str.rstrip('%').astype('float')
df_todos_los_datos['Leche vrs. hato '] = df_todos_los_datos['Leche vrs. hato '].str.rstrip('%').astype('float')

#Agregación de columnas de % de Prod vs. Hato con texto para stickers en Dash
df_todos_los_datos['Leche vida vs.hato/prom'] = df_todos_los_datos['Leche vida vs.hato']-100
df_todos_los_datos['Leche vida vs.hato/prom'] = df_todos_los_datos['Leche vida vs.hato/prom'].fillna('0').astype(int)
df_todos_los_datos.loc[df_todos_los_datos['Leche vida vs.hato/prom']<0, 'Leche vida vs.hato_C'] = df_todos_los_datos['Leche vida vs.hato/prom'].astype(str)+ '% /Prom'
df_todos_los_datos.loc[df_todos_los_datos['Leche vida vs.hato/prom']>=0, 'Leche vida vs.hato_C'] = '+'+ df_todos_los_datos['Leche vida vs.hato/prom'].astype(str)+ '% /Prom'
df_todos_los_datos['Lt Lact. vs.hato/prom'] = df_todos_los_datos['Lt  Lact. vs.hato']-100
df_todos_los_datos['Lt Lact. vs.hato/prom'] = df_todos_los_datos['Lt Lact. vs.hato/prom'].fillna('0').astype(int)
df_todos_los_datos.loc[df_todos_los_datos['Lt Lact. vs.hato/prom']<0, 'Lt Lact. vs.hato_C'] = df_todos_los_datos['Lt Lact. vs.hato/prom'].astype(str)+ '% /Prom'
df_todos_los_datos.loc[df_todos_los_datos['Lt Lact. vs.hato/prom']>=0, 'Lt Lact. vs.hato_C'] = '+'+ df_todos_los_datos['Lt Lact. vs.hato/prom'].astype(str)+ '% /Prom'
df_todos_los_datos['Leche vrs. hato/prom'] = df_todos_los_datos['Leche vrs. hato ']-100
df_todos_los_datos['Leche vrs. hato/prom'] = df_todos_los_datos['Leche vrs. hato/prom'].fillna('0').astype(int)
df_todos_los_datos.loc[df_todos_los_datos['Leche vrs. hato/prom']<0, 'Leche vrs. hato_C'] = df_todos_los_datos['Leche vrs. hato/prom'].astype(str)+ '% /Prom'
df_todos_los_datos.loc[df_todos_los_datos['Leche vrs. hato/prom']>=0, 'Leche vrs. hato_C'] = '+'+ df_todos_los_datos['Leche vrs. hato/prom'].astype(str)+ '% /Prom'

#Agregación de fecha actual
df_todos_los_datos['Hoy'] = dt.datetime.today().strftime('%d/%m/%Y')
df_todos_los_datos['Hoy'] = pd.to_datetime(df_todos_los_datos['Hoy'], format='%d/%m/%Y').dt.date

#Calculo de edad actual en meses
df_todos_los_datos['Edad_actual'] = ((df_todos_los_datos['Hoy'] - df_todos_los_datos['Nacimiento']) / np.timedelta64(1, 'M'))
df_todos_los_datos['Edad_actual'] = df_todos_los_datos['Edad_actual'].fillna('0').astype(int)
df_todos_los_datos['Edad_actual'] = df_todos_los_datos['Edad_actual'].astype(int)

#Calculo de Leche promedio por mes por vaca
df_todos_los_datos['Leche_prom_mes'] = df_todos_los_datos['Leche acumulada']/df_todos_los_datos['Edad_actual']
df_todos_los_datos['Leche_prom_mes'] = df_todos_los_datos['Leche_prom_mes'].replace(np.inf, np.nan)
df_todos_los_datos['Leche_prom_mes'] = df_todos_los_datos['Leche_prom_mes'].fillna('0.0').astype('float64')
df_todos_los_datos['Leche_prom_mes'] = df_todos_los_datos['Leche_prom_mes'].round(2)
df_todos_los_datos['Leche_prom_mes_c'] = df_todos_los_datos['Leche_prom_mes'].astype(str)+ ' Lt. Mes'

#Calculo de ciclo de lactancia 'DIM' y Tercio de Lactancia
df_todos_los_datos['DIM'] = ((df_todos_los_datos['Hoy'] - df_todos_los_datos['Ult. parto']) / np.timedelta64(1, 'D'))
df_todos_los_datos['DIM'] = df_todos_los_datos['DIM'].fillna('0').astype(int)
df_todos_los_datos['DIM_c'] = df_todos_los_datos['DIM'].astype(str)+ ' DIM'
df_todos_los_datos['Tercio lactancia (groups)'] = df_todos_los_datos['Tercio lactancia'].replace({'1 0-100': '1er Terc. Lactancia', 
                                                                                                  '2 101-200': '2do Terc. Lactancia', 
                                                                                                  '3 >200': '3er Terc. Lactancia', 
                                                                                                  np.nan:  'Sin Terc. Lactancia'})

#Agregación de columnas de datos para tarjetas de animal
df_todos_los_datos['Mast. vida'] = df_todos_los_datos['Mast. vida'].fillna('0').astype(int)
df_todos_los_datos['Mast_vida'] = df_todos_los_datos['Mast. vida'].astype(str)+ ' Mastitis'
df_todos_los_datos['Mast. act.'] = df_todos_los_datos['Mast. act.'].fillna('0').astype(int)
df_todos_los_datos['Mast. act.'] = df_todos_los_datos['Mast. act.'].astype(str)
df_todos_los_datos['Mast_activa'] = df_todos_los_datos['Mast. act.'].replace({'0': 'No Activa', '1': 'Activa', '2': 'Activa', '3': 'Activa', '4':'Activa', '5':'Activa', '6':'Activa', '7':'Activa'})
df_todos_los_datos['Cojera vida'] = df_todos_los_datos['Cojera vida'].fillna('0').astype(int)
df_todos_los_datos['Cojera_vida'] = df_todos_los_datos['Cojera vida'].astype(str)+ ' Cojeras'
df_todos_los_datos['Cojera act.'] = df_todos_los_datos['Cojera act.'].fillna('0').astype(int)
df_todos_los_datos['Cojera act.'] = df_todos_los_datos['Cojera act.'].astype(str)
df_todos_los_datos['Cojera_activa'] = df_todos_los_datos['Cojera act.'].str.replace('0', 'No Activa', case = False).str.replace('1', 'Activa', case = False)
df_todos_los_datos['No. crías'] = df_todos_los_datos['No. crías'].fillna('0').astype(int)
df_todos_los_datos['No_crias'] = df_todos_los_datos['No. crías'].astype(str)+ ' Crías'
df_todos_los_datos['Int. entre partos'] = df_todos_los_datos['Int. entre partos'].fillna('0').astype(int)
df_todos_los_datos['Int_entre_partos'] = df_todos_los_datos['Int. entre partos'].astype(str)+ ' Días'
df_todos_los_datos2 = df_todos_los_datos.copy()

#Agregado de columnas 'label' y 'value' para filtro por animal
df_todos_los_datos['label']= df_todos_los_datos['Numero']
df_todos_los_datos['value']= df_todos_los_datos['Numero']
df_todos_los_datos2['label']= df_todos_los_datos2['Grupo']
df_todos_los_datos2['value']= df_todos_los_datos2['Grupo']

#Remoción de duplicados por Numero de animal
df_todos_los_datos.drop_duplicates(subset=['Numero'], keep='last')
df_todos_los_datos2.drop_duplicates(subset=['Numero'], keep='last')

#Exportar dataframe a .csv
df_todos_los_datos.to_csv(r'data/Todos_los_datos.csv', index= False, header=True)
df_todos_los_datos2.to_csv(r'data/Todos_los_datos2.csv', index= False, header=True)
#--------------------------------------------------------------------------------------------------------------------------------------------


#Lectura de datos de control de mastitis
df_mastitis_vacas = pd.read_excel(os.path.join("data/Raw_data/HISTORICO MASTITIS INVERSIONES CAMACHO.xlsm"), sheet_name= 'Base de Datos')   
#df_mastitis_vacas['UBRE SANA'] = pd.Series(["{0:.2f}%".format(val * 100) for val in df_mastitis_vacas['UBRE SANA']], index = df_mastitis_vacas.index)
#df_mastitis_vacas['CAL. UBRE'] = pd.Series(["{0:.2f}%".format(val * 100) for val in df_mastitis_vacas['CAL. UBRE']], index = df_mastitis_vacas.index)
#df_mastitis_vacas['GAP'] = pd.Series(["{0:.2f}%".format(val * 100) for val in df_mastitis_vacas['GAP']], index = df_mastitis_vacas.index)

#Exportar dataframe a .csv
df_mastitis_vacas.to_csv(r'data/Historico_Mastitis_Inversiones_Camacho-Vacas.csv', index= False, header=True)
#--------------------------------------------------------------------------------------------------------------------------------------------


#Lectura de eventos registrados
df_eventos_reg = pd.read_csv('data/Raw_data/Eventos_registrados.txt', sep='\t', engine='python')
df_eventos_reg['Id'] = df_eventos_reg['Id'].str.strip()
df_eventos_reg['Evento'] = df_eventos_reg['Evento'].str.strip()
df_eventos_reg['Resultado'] = df_eventos_reg['Resultado'].str.strip()
df_eventos_reg['Categorías'] = df_eventos_reg['Categorías'].str.strip()
df_eventos_reg['Toro'] = df_eventos_reg['Toro'].str.strip()
df_eventos_reg['Operario'] = df_eventos_reg['Operario'].str.strip()
df_eventos_reg['Comentarios'] = df_eventos_reg['Comentarios'].str.strip()
#df_eventos_reg['Fecha']= df_eventos_reg['Fecha'].apply(lambda x: dt.datetime.strptime(x, '%d/%m/%Y').date())  
df_eventos_reg['Fecha'] = pd.to_datetime(df_eventos_reg['Fecha'], format='%d/%m/%Y')
df_eventos_reg['Evento(0)'] = 0
df_eventos_reg = df_eventos_reg.sort_values('Fecha',ascending=False)

#Exportar dataframe a .csv
df_eventos_reg.to_csv(r'data/Eventos_registrados.csv', index= False, header=True)
#--------------------------------------------------------------------------------------------------------------------------------------------


#Lectura de seguimiento de hatos
df_seguimiento_hatos = pd.read_csv(os.path.join("data/Raw_data/seguimiento_hatos.csv"))
#reliable_date='20190101'
#df_seguimiento_hatos = df_seguimiento_hatos[df_seguimiento_hatos.date>=dt.datetime.strptime(reliable_date,'%Y%m%d')]
df_seguimiento_hatos['date'] = pd.to_datetime(df_seguimiento_hatos['date'], format='%Y/%m/%d')#.dt.date
df_seguimiento_hatos = df_seguimiento_hatos.sort_values(by=['date','HATO'])
df_seguimiento_hatos.reset_index(drop = True, inplace=True)

#Exportar dataframe a .csv
df_seguimiento_hatos.to_csv(r'data/seguimiento_hatos(Test).csv', index= False, header=True)
#--------------------------------------------------------------------------------------------------------------------------------------------


#Lectura de eventos registrados
df_hatos_lag = pd.read_csv(os.path.join("data/Raw_data/lag_lotes.csv"))
#reliable_date='20190101'
#df_seguimiento_hatos = df_seguimiento_hatos[df_seguimiento_hatos.date>=dt.datetime.strptime(reliable_date,'%Y%m%d')]
df_hatos_lag['date'] = pd.to_datetime(df_hatos_lag['date'], format='%Y/%m/%d')#.dt.date
df_hatos_lag = df_hatos_lag.sort_values(by=['date','HATO'])
df_hatos_lag.reset_index(drop = True, inplace=True)
df_hatos_lag1 = df_hatos_lag.merge(df_seguimiento_hatos, how='left', left_on= ['date','HATO','value'], right_on=['date','HATO','name'])


#Exportar dataframe a .csv
df_hatos_lag1.to_csv(r'data/lag_lotes(Test).csv', index= False, header=True)
#--------------------------------------------------------------------------------------------------------------------------------------------


#set working directory
os.chdir("data/Raw_data/Registros_de_Leche_Lactx")

globbed_files_reg_leche = glob.glob("*.TXT")
data_reg_leche = []
for TXT in globbed_files_reg_leche:
    frame_reg_leche = pd.read_csv(TXT, sep='\t', engine='python')
    frame_reg_leche['filename'] = os.path.basename(TXT)
    data_reg_leche.append(frame_reg_leche)
df_reg_leche_lactx = pd.concat(data_reg_leche, ignore_index=True)
df_reg_leche_lactx = df_reg_leche_lactx[df_reg_leche_lactx['N'].notna()]
df_reg_leche_lactx['Fecha'] = pd.to_datetime(df_reg_leche_lactx['Fecha'], format='%d/%m/%Y')#.dt.date
df_reg_leche_lactx = df_reg_leche_lactx.sort_values('Fecha',ascending=False)
df_reg_leche_lactx['Id'] = df_reg_leche_lactx['filename'].apply(lambda st: st[st.find("#")+1:st.find("_")])
df_reg_leche_lactx['Id'] = df_reg_leche_lactx['Id'].str.strip()
df_reg_leche_lactx['Lactancia'] = df_reg_leche_lactx['filename'].apply(lambda st: st[st.find("L")+6:st.find(".")])
df_reg_leche_lactx['Color_lact'] = df_reg_leche_lactx['Lactancia'].str.strip().str[-1].astype(int)
df_reg_leche_lactx.reset_index(drop = True, inplace=True)


# df_reg_leche_lactx_reg = df_reg_leche_lactx[df_reg_leche_lactx['Id'] == '1234']
# df_reg_leche_lactx_reg = df_reg_leche_lactx_reg.sort_values('N',ascending=True)

# from sklearn import datasets, linear_model
# from sklearn.metrics import mean_squared_error, r2_score

# X = df_reg_leche_lactx.iloc[:, 1:2].values
# y = df_reg_leche_lactx.iloc[:, 3:4].values

# # Splitting the dataset into the Training set and Test set
# from sklearn.model_selection import train_test_split
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

# from sklearn.linear_model import LinearRegression

# regressor = LinearRegression()
# regressor.fit(X_train, y_train)

# y_pred = regressor.predict(X_test)

# import matplotlib.pyplot as plt
# #vis
# #Test results for 2D problems
# plt.scatter(X, y, c=df_reg_leche_lactx['Color_lact'])
# #plt.scatter(X_train, y_train, color='green')
# plt.plot(X_train, regressor.predict(X_train), color='blue')
# plt.title('Curva de Prod de Leche')
# plt.xlabel('Días') #x variable name
# plt.ylabel('Leche kg') # y variable name
# plt.legend(['3','6','7'], loc = "center left", bbox_to_anchor = (1, 0.5), numpoints = 1)
# plt.show()

# # Visualising the Regression results (for higher resolution and smoother curve) /mandatory for RF and trees
# X_grid = np.arange(15, 400, 1) 
# X_grid = X_grid.reshape((len(X_grid),1))
# plt.scatter(X, y, color='red')
# plt.plot(X_grid, regressor.predict(X_grid), color='orange')
# plt.title('Curva de Prod de Leche')
# plt.xlabel('Días') #x variable name
# plt.ylabel('Leche kg') # y variable name
# plt.show()


#Exportar dataframes concatenados a .csv
os.chdir("C:/Users/Nickair90/Nicolas/Analytics_Lab/Proyecto_Lotes_Vacas/Dashboard-Dash/data/")
df_reg_leche_lactx.to_csv(r'Registros_de_Leche_Lactx.csv', index=False, header=True)
#--------------------------------------------------------------------------------------------------------------------------------------------


#set working directory
os.chdir("Raw_data/Registro_de_Peso_Lact0")

globbed_files_reg_peso = glob.glob("*.TXT")
data_reg_peso = []
for TXT in globbed_files_reg_peso:
    frame_reg_peso = pd.read_csv(TXT, sep='\t', engine='python')
    frame_reg_peso['filename'] = os.path.basename(TXT)
    data_reg_peso.append(frame_reg_peso)
df_reg_peso_lact0 = pd.concat(data_reg_peso, ignore_index=True)
# df_reg_peso_lact0 = df_reg_peso_lact0[df_reg_peso_lact0['N'].notna()]
df_reg_peso_lact0['Fecha'] = pd.to_datetime(df_reg_peso_lact0['Fecha'], format='%d/%m/%Y', exact=False)#.dt.date
df_reg_peso_lact0 = df_reg_peso_lact0.sort_values('Fecha',ascending=False)
df_reg_peso_lact0['Id'] = df_reg_peso_lact0['filename'].apply(lambda st: st[st.find("#")+1:st.find("_")])
df_reg_peso_lact0['Id'] = df_reg_peso_lact0['Id'].str.strip()
df_reg_peso_lact0['Lactancia'] = df_reg_peso_lact0['filename'].apply(lambda st: st[st.find("L"):st.find(".")])
df_reg_peso_lact0.reset_index(drop = True, inplace=True)

#Exportar dataframes concatenados a .csv
os.chdir("C:/Users/Nickair90/Nicolas/Analytics_Lab/Proyecto_Lotes_Vacas/Dashboard-Dash/data/")
df_reg_peso_lact0.to_csv(r'Registro_de_Peso_Lact0.csv', index=False, header=True)
#--------------------------------------------------------------------------------------------------------


#set working directory
os.chdir("Raw_data/Resumen_de_Estado")

globbed_files_res_estado = glob.glob("*.TXT")
data_res_estado = []
for TXT in globbed_files_res_estado:
    frame_res_estado = pd.read_csv(TXT, sep='\t', engine='python')
    frame_res_estado['filename'] = os.path.basename(TXT)
    data_res_estado.append(frame_res_estado)
df_res_estado = pd.concat(data_res_estado, ignore_index=True)
df_res_estado = df_res_estado[df_res_estado['N'].notna()]
df_res_estado['Parto'] = pd.to_datetime(df_res_estado['Parto'], format='%d/%m/%Y', exact=False).dt.date
df_res_estado = df_res_estado.sort_values('N',ascending=True)
df_res_estado['1er. servicio'] = pd.to_datetime(df_res_estado['1er. servicio'], format='%d/%m/%Y', exact=False).dt.date
df_res_estado['Ult. servicio'] = pd.to_datetime(df_res_estado['Ult. servicio'], format='%d/%m/%Y', exact=False).dt.date
df_res_estado['Concepción'] = pd.to_datetime(df_res_estado['Concepción'], format='%d/%m/%Y', exact=False).dt.date
df_res_estado['Secado'] = pd.to_datetime(df_res_estado['Secado'], format='%d/%m/%Y', exact=False).dt.date
df_res_estado['Id'] = df_res_estado['filename'].apply(lambda st: st[st.find("#")+1:st.find("_")])
df_res_estado['Id'] = df_res_estado['Id'].str.strip()
# df_res_estado['Int.'] = df_res_estado['Int.'].str.replace("'", "")
# df_res_estado['Int.'] = df_res_estado['Int.'].fillna('0').astype(int)
# df_res_estado['Int.'] = df_res_estado['Int.'].astype(int)
df_res_estado['Lact.'] = df_res_estado['Lact.'].str.replace('\'', '')
# df_res_estado['Lact.'] = df_res_estado['Lact.'].fillna('0').astype(int)
# df_res_estado['Lact.'] = df_res_estado['Lact.'].astype(int)
df_res_estado['305-d.'] = df_res_estado['305-d.'].str.replace('\'', '')
# df_res_estado['305-d.'] = df_res_estado['305-d.'].fillna('0').astype(int)
# df_res_estado['305-d.'] = df_res_estado['305-d.'].astype(int)
df_res_estado['Leche acum.'] = df_res_estado['Leche acum.'].str.replace('\'', '')
# df_res_estado['Leche acum.'] = df_res_estado['Leche acum.'].fillna('0').astype(int)
# df_res_estado['Leche acum.'] = df_res_estado['Leche acum.'].astype(int)
df_res_estado['Conc. acum.'] = df_res_estado['Conc. acum.'].str.replace('\'', '')
# df_res_estado['Conc. acum.'] = df_res_estado['Conc. acum.'].fillna('0').astype(int)
# df_res_estado['Conc. acum.'] = df_res_estado['Conc. acum.'].astype(int)
df_res_estado = df_res_estado.drop(columns=['filename'])
df_res_estado.reset_index(drop = True, inplace=True)

#Exportar dataframes concatenados a .csv
os.chdir("C:/Users/Nickair90/Nicolas/Analytics_Lab/Proyecto_Lotes_Vacas/Dashboard-Dash/data/")
df_res_estado.to_csv(r'Resumen_de_Estado.csv', index=False, header=True)


