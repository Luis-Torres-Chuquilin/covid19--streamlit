
from os import write
from pandas.core import groupby
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
import json
import streamlit as st

@st.cache
def load_data():
    import pandas as pd
    df = pd.read_csv('SINADEF_DATOS_ABIERTOS_11022021.csv' )
    df['Muertes'] = 1 

    df.rename(columns={"DEPARTAMENTO DOMICILIO": "DEPARTAMENTO", 
                            "PROVINCIA DOMICILIO": "PROVINCIA" , 
                            "DISTRITO DOMICILIO": "DISTRITO" }, inplace=True)
    df = df[~df['MUERTE VIOLENTA'].str.endswith(('ACCIDENTE DE TRANSITO' , 'HOMICIDIO', 'NO SE CONOCE' , 'OTRO ACCIDENTE' , 'SUICIDIO' , 'ACCIDENTE DE TRABAJO'))]
    df = df[[ 'DEPARTAMENTO' , 'PROVINCIA' , 'DISTRITO' , 'FECHA' ,'Muertes']]
    df = df[df["FECHA"] >= "2019-01-01" ].sort_values("FECHA",ascending=True)
    df = df[~df['DEPARTAMENTO'].str.endswith(('TRANJERO', 'GISTRO'))]
    df = df[~df['PROVINCIA'].str.endswith(('TRANJERO', 'GISTRO'))]
    df = df[~df['DISTRITO'].str.endswith(('TRANJERO', 'GISTRO'))]
    #df = df[~df['DISTRITO'].str.endswith(('LURIGANCHO'))]
              
    return df
       
       
def df_ubicacion( df1 , ubicacion ,ubicaciones ):
    import pandas as pd
    df_index = df1.groupby(["FECHA"])[["Muertes"]].sum().reset_index().sort_values("FECHA",ascending=True)
    df0 = pd.DataFrame()
    df0['FECHA'] = df_index['FECHA']
    df0.set_index(df0['FECHA'], inplace=True)
    df0.drop(['FECHA'] , axis=1 , inplace=True)
    
    for i in ubicaciones:
        df_ubicaciones = df1[df1[ubicacion] == i].groupby(["FECHA"])[["Muertes"]].sum().reset_index().sort_values("FECHA",ascending=True).rename(columns={'Muertes': i})
        df_ubicaciones.set_index(df_ubicaciones['FECHA'], inplace=True)
        df_ubicaciones.drop(['FECHA'] , axis=1 , inplace=True)
        df2= df_ubicaciones
        df0 = pd.concat([df0, df2], axis=1)
        df0 = df0.fillna(0)
    return df0

  
def poblacion_ubicacion( ubicacion , url):
    import pandas as pd
    df_poblacion = pd.read_csv( url )
    df_poblacion.set_index(df_poblacion[ubicacion], inplace=True)
    df_poblacion.drop([ubicacion] , axis=1 , inplace=True)
    
    return df_poblacion

def df_ubicacion_muertes_promedio( df2 , df3):
    for i in df2.columns:
        df2[i] = df2[i].rolling(7).mean()/df3.at[i,'POBLACION']*1000000
    return df2
    
def df_muertos_ultimo_dia( df2_p ,ubicacion ):
    df_b = df2_p.iloc[[-2]]
    df_b = df_b.T
    df_b['Muertes'] = df_b.iloc[: , -1]
    df_b.sort_values( by=['Muertes'] ,ascending=False , inplace=True)
   
    return df_b

def grafica_tendencia_diaria( df2_p ):
    
    if len(df2_p.columns) == 1:
        x = df2_p.columns
        df0= df2_p
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df0.index, y= df0[x[0]], mode= 'lines', marker_color ='red' , name= x[0] ))
        fig.update_layout( title=' ' , template='plotly_white',  yaxis_title="Muertes al dia ",  xaxis_title="Fecha", )  
        return fig
    
    if len(df2_p.columns) == 2:
        x = df2_p.columns
        df0= df2_p
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df0.index, y= df0[x[0]], mode= 'lines', marker_color ='red' , name= x[0] ))
        fig.add_trace(go.Scatter(x=df0.index, y= df0[x[1]],  mode= 'lines', marker_color ='grey' ,  name= x[1] ))
        fig.update_layout( title=' ' , template='plotly_white',  yaxis_title="Muertes ",  xaxis_title="Fecha", )  
        return fig
    
    
    
    if len(df2_p.columns) == 3:
        x = df2_p.columns
        df0= df2_p
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df0.index, y= df0[x[0]], mode= 'lines', marker_color ='red' , name= x[0] ))
        fig.add_trace(go.Scatter(x=df0.index, y= df0[x[1]],  mode= 'lines', marker_color ='grey' ,  name= x[1] ))
        fig.add_trace(go.Scatter(x=df0.index, y= df0[x[2]],  mode= 'lines', marker_color ='green' ,  name= x[2] ))
        fig.update_layout( title=' ' , template='plotly_white',  yaxis_title="Muertes al dia ",  xaxis_title="Fecha", )  
        return fig
    
    
    
    if len(df2_p.columns) == 4:
        x = df2_p.columns
        df0= df2_p
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df0.index, y= df0[x[0]], mode= 'lines', marker_color ='red' , name= x[0] ))
        fig.add_trace(go.Scatter(x=df0.index, y= df0[x[1]],  mode= 'lines', marker_color ='grey' ,  name= x[1] ))
        fig.add_trace(go.Scatter(x=df0.index, y= df0[x[2]],  mode= 'lines', marker_color ='green' ,  name= x[2] ))
        fig.add_trace(go.Scatter(x=df0.index, y= df0[x[3]],   mode= 'lines', marker_color ='black' , name= x[3] ))
        fig.update_layout( title=' ' , template='plotly_white',  yaxis_title="Muertes al dia ",  xaxis_title="Fecha", )  
        return fig
    
    if len(df2_p.columns) == 5:
        x = df2_p.columns
        df0= df2_p
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df0.index, y= df0[x[0]], mode= 'lines', marker_color ='red' , name= x[0] ))
        fig.add_trace(go.Scatter(x=df0.index, y= df0[x[1]],  mode= 'lines', marker_color ='grey' ,  name= x[1] ))
        fig.add_trace(go.Scatter(x=df0.index, y= df0[x[2]],  mode= 'lines', marker_color ='green' ,  name= x[2] ))
        fig.add_trace(go.Scatter(x=df0.index, y= df0[x[3]],   mode= 'lines', marker_color ='black' , name= x[3] ))
        fig.add_trace(go.Scatter(x=df0.index, y= df0[x[4]],  mode= 'lines', marker_color ='pink' , name= x[4] ))
        fig.update_layout( title=' ' , template='plotly_white',  yaxis_title="Muertes ",  xaxis_title="Fecha", )  
        return fig
    
    
    if len(df2_p.columns) == 6:
        x = df2_p.columns
        df0= df2_p
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df0.index, y= df0[x[0]], mode= 'lines', marker_color ='red' , name= x[0] ))
        fig.add_trace(go.Scatter(x=df0.index, y= df0[x[1]],  mode= 'lines', marker_color ='grey' ,  name= x[1] ))
        fig.add_trace(go.Scatter(x=df0.index, y= df0[x[2]],  mode= 'lines', marker_color ='green' ,  name= x[2] ))
        fig.add_trace(go.Scatter(x=df0.index, y= df0[x[3]],   mode= 'lines', marker_color ='black' , name= x[3] ))
        fig.add_trace(go.Scatter(x=df0.index, y= df0[x[4]],  mode= 'lines', marker_color ='pink' , name= x[4] ))
        fig.add_trace(go.Scatter(x=df0.index, y= df0[x[5]],  mode= 'lines', marker_color ='blue' , name= x[5] ))
        fig.update_layout( title=' ' , template='plotly_white',  yaxis_title="Muertes al dia ",  xaxis_title="Fecha", )  
        return fig 
    
    if len(df2_p.columns) == 7:
        x = df2_p.columns
        df0= df2_p
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df0.index, y= df0[x[0]], mode= 'lines', marker_color ='red' , name= x[0] ))
        fig.add_trace(go.Scatter(x=df0.index, y= df0[x[1]],  mode= 'lines', marker_color ='grey' ,  name= x[1] ))
        fig.add_trace(go.Scatter(x=df0.index, y= df0[x[2]],  mode= 'lines', marker_color ='green' ,  name= x[2] ))
        fig.add_trace(go.Scatter(x=df0.index, y= df0[x[3]],   mode= 'lines', marker_color ='black' , name= x[3] ))
        fig.add_trace(go.Scatter(x=df0.index, y= df0[x[4]],  mode= 'lines', marker_color ='pink' , name= x[4] ))
        fig.add_trace(go.Scatter(x=df0.index, y= df0[x[5]],  mode= 'lines', marker_color ='blue' , name= x[5] ))
        fig.add_trace(go.Scatter(x=df0.index, y= df0[x[6]],  mode= 'lines', marker_color ='red' , name= x[6] ))
        fig.update_layout( title=' ' , template='plotly_white',  yaxis_title="Muertes al dia ",  xaxis_title="Fecha", )  
        return fig     
    
    if len(df2_p.columns) == 8:
        x = df2_p.columns
        df0= df2_p
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df0.index, y= df0[x[0]], mode= 'lines', marker_color ='red' , name= x[0] ))
        fig.add_trace(go.Scatter(x=df0.index, y= df0[x[1]],  mode= 'lines', marker_color ='grey' ,  name= x[1] ))
        fig.add_trace(go.Scatter(x=df0.index, y= df0[x[2]],  mode= 'lines', marker_color ='green' ,  name= x[2] ))
        fig.add_trace(go.Scatter(x=df0.index, y= df0[x[3]],   mode= 'lines', marker_color ='black' , name= x[3] ))
        fig.add_trace(go.Scatter(x=df0.index, y= df0[x[4]],  mode= 'lines', marker_color ='pink' , name= x[4] ))
        fig.add_trace(go.Scatter(x=df0.index, y= df0[x[5]],  mode= 'lines', marker_color ='blue' , name= x[5] ))
        fig.add_trace(go.Scatter(x=df0.index, y= df0[x[6]],  mode= 'lines', marker_color ='green' , name= x[6] ))
        fig.add_trace(go.Scatter(x=df0.index, y= df0[x[7]],  mode= 'lines', marker_color ='gold' , name= x[7] ))
        fig.update_layout( title=' ' , template='plotly_white',  yaxis_title="Muertes al dia",  xaxis_title="Fecha",  )  
        return fig     
    
    
def grafica_bar( df_ultima_m , ubicacion):
    fig3 = px.bar(df_ultima_m, y= df_ultima_m.index , x='Muertes', orientation='h' , hover_data=['Muertes', 'Muertes'], color='Muertes',
            labels={'Muertes':'Fallecimientos registrados el 06-02-2021' , ubicacion : ubicacion }, width=1200, height=600 )
    
    return fig3        
            


# key "properties.NOMBDEP"
# ubicacion : DEPARTAMENTO , PROVINCIA 
#  url 


def grafica_maps( df_ultima_m ,ubicacion , url , key ):
    with open( url ) as response: 
        peru_geo = json.load(response)
    fig = px.choropleth(df_ultima_m , geojson= peru_geo, color="Muertes", locations= df_ultima_m.index , featureidkey= key ,  projection="mercator", range_color= (0,45),
                            labels = {'CASOS':"Casos", ubicacion : ubicacion } , width=800, height=800  )
    fig.update_geos(fitbounds="locations", visible=False  # ,  showcountries = True, 
                        , resolution=110 )
    fig.update_layout( margin={"r":0,"t":0,"l":0,"b":0},  title_text = 'Covid-19 en el Peru (Por Departamento)', )
            
    return fig