import site
import sys
import os
import re, datetime
from os import write
from pandas.core import groupby
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import seaborn as sns
import plotly.offline as py
import json
from funciones_covid19 import *



st.set_page_config( page_title="Análisis del Covid 19 - Perúsis",  page_icon="🧊",  layout="wide",
                     initial_sidebar_state="expanded" )

st.sidebar.title('Datos')



#######################################

### INFORMACION DE DEPARTAMENTOS 



#######################################


with st.beta_expander(" Comparaciones por Departamentos "):
    
    df1 = load_data()
    departamentos = st.multiselect(label='',  options = (df1.DEPARTAMENTO.unique())) 
    df2 = df_ubicacion( df1, 'DEPARTAMENTO' , departamentos)
    df3 = poblacion_ubicacion( 'DEPARTAMENTO' , 'poblacion_departamento.csv' )
    df2_p = df_ubicacion_muertes_promedio( df2 , df3 )
    graf_tendencia = grafica_tendencia_diaria(df2_p)

    col1, col2 = st.beta_columns(2)


    col1.write(graf_tendencia)
    col2.table(df2_p.tail(8))

    ## Graficas de todos los departamentos del Perú  Barras y  Mapdas

    df2 = df_ubicacion( df1 , 'DEPARTAMENTO' , df1.DEPARTAMENTO.unique() )
    df3 = poblacion_ubicacion( 'DEPARTAMENTO' , 'poblacion_departamento.csv' )
    df2_p = df_ubicacion_muertes_promedio(df2, df3)
    graf_tendencia = grafica_tendencia_diaria( df2_p)
    df_ultima_m = df_muertos_ultimo_dia( df2_p , 'DEPARTAMENTO')
    graf_bar =grafica_bar( df_ultima_m ,'DEPARTAMENTO')
    graf_maps1 = grafica_maps( df_ultima_m , 'DEPARTAMENTO' , 'peru_departamental_simple.geojson' , 'properties.NOMBDEP' )

    col1, col2 = st.beta_columns(2)
    col1.write(graf_bar)
    col2.write(graf_maps1)


#######################################

### INFORMACION DE PROVINCIAS 

st.success('Información de Provincias por millon de habitantes')




#######################################

with st.beta_expander(" Comparaciones por Provincias "):

    df1 = load_data()
    col1 , col2  = st.beta_columns([1,3])
    departamentos = col1.selectbox(label='',  options = (df1.DEPARTAMENTO.unique())) 
    df1= df1[df1['DEPARTAMENTO'] == departamentos]
    provincias = col2.multiselect(label=' ', options = (df1.PROVINCIA.unique()))

    df2 = df_ubicacion( df1 , 'PROVINCIA', provincias)
    df3 = poblacion_ubicacion( 'PROVINCIA' , 'poblacion_provincia.csv')
    df2_p = df_ubicacion_muertes_promedio( df2, df3 )
    graf_tendencia = grafica_tendencia_diaria(df2_p)

    col1, col2  = st.beta_columns(2)
    col1.write(graf_tendencia)
    col2.table(df2_p.tail(10))

    ## Graficas de todos los departamentos del Perú  Barras y  Mapa

    df2 = df_ubicacion( df1 , 'PROVINCIA' , df1.PROVINCIA.unique() )
    df3 = poblacion_ubicacion( 'PROVINCIA', 'poblacion_provincia.csv' )      ### Caundo seleciono proviincia Arequipa e imprimo  st.write(df2). 
    df2_p = df_ubicacion_muertes_promedio(df2 , df3 )
    graf_tendencia = grafica_tendencia_diaria(df2_p)
    df_ultima_m = df_muertos_ultimo_dia(df2_p , 'PROVINCIA')
    graf_bar =grafica_bar(df_ultima_m , 'PROVINCIA')
    graf_maps = grafica_maps( df_ultima_m , 'PROVINCIA' , 'peru_provincial_simple.geojson' , 'properties.NOMBPROV' )
    #st.write(df2.tail(10))

    col1, col2 = st.beta_columns(2)
    col1.write(graf_bar)
    col2.write(graf_maps)

#######################################

### INFORMACION DE PROVINCIAS 

st.success('Información de Distritos por millon de habitantes')


#######################################

with st.beta_expander(" Comparaciones por Provincias "):

    df1 = load_data()
    col1, col2 = st.beta_columns([1,4])
    departamentos = col1.radio(label='',  options = (df1.DEPARTAMENTO.unique())) 
    df1= df1[df1['DEPARTAMENTO'] == departamentos]
    provincias = col2.selectbox(label=' ', options = (df1.PROVINCIA.unique()))
    df1= df1[df1['PROVINCIA'] == provincias]
    distritos = col2.multiselect(label=' ',  options = (df1.DISTRITO.unique()))

    df2 = df_ubicacion( df1, 'DISTRITO', distritos)
    for i in df2.columns:  # df_ubicacion_muertes_promedio
        df2[i] = df2[i].rolling(7).mean()
    df2_p=df2 # df_ubicacion_muertes_promedio
    graf_tendencia = grafica_tendencia_diaria(df2_p)

    col2.table(df2_p.tail(10))

    col1, col2  = st.beta_columns(2)
    col1.write(graf_tendencia)
    
    

    # Tabla de muerte promedio de ultima fecha de todos los distritos 

    df2 = df_ubicacion( df1, 'DISTRITO', df1.DISTRITO.unique())
    for i in df2.columns:  # df_ubicacion_muertes_promedio
        df2[i] = df2[i].rolling(7).mean()
    df2_p=df2 # df_ubicacion_muertes_promedio
    df_ultima_m = df_muertos_ultimo_dia(df2_p , 'PROVINCIA')
    graf_bar =grafica_bar(df_ultima_m , 'DISTRITO')
    #graf_maps = grafica_maps( 'DISTRITO' , 'peru_distrital_simple.geojson' , 'properties.NOMBDIST' ) No ajusta todos 

    st.write(graf_bar)

    if provincias == 'LIMA':
        graf_maps = grafica_maps(  df_ultima_m , 'DISTRITO' , 'lima_callao_distritos.geojson' , 'properties.distrito' )
        st.write(graf_maps)
        



