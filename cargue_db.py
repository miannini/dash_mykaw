# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 22:08:23 2020

@author: ASUS-PC
"""
import pandas as pd
import mysql.connector
db_connection = mysql.connector.connect(
  	host="35.185.0.199",
  	user="m4a.MI",
  	passwd="m4a2020"
    )

# creating database_cursor to perform SQL operation
db_cursor = db_connection.cursor()
# get list of all databases
db_cursor.execute("SHOW DATABASES")
#print all databases
for db in db_cursor:
	print(db)
    

sql = '''select * from m4a_bi.resumen_lotes_medidas'''
prueba  = pd.read_sql(sql, db_connection)

sql = '''select * from m4a_bi.Data_lotes'''
prueba2  = pd.read_sql(sql, db_connection)

#Crear tabla

#Data_lotes = pd.read_csv( 'D:\M4A\SQLDB\Dash\data\Data_lotes.csv')  



#Se usa la conexión con alchemy para to_sql

# import pymysql
# import sqlalchemy as sa
# engine = sa.create_engine("mysql+pymysql://" + "m4a.DA" + ":" + "m4a2020" + "@" + "35.185.0.199" + "/" + "m4a_bi")

# Data_lotes.to_sql('Data_lotes', engine,  if_exists='append', index=False)

