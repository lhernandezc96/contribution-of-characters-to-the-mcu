from collections import OrderedDict
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
from EDA import char_movie_matrix, movie_lengths




def matriz_datos (no_serie, fases):
    columnas_seleccionadas = char_movie_matrix.columns[char_movie_matrix.loc['Fase'] .isin(fases)]
    data_f = char_movie_matrix[columnas_seleccionadas]
    if no_serie:
        # Filtrar las columnas excluyendo las que tienen False en la fila 'Serie'
        columnas_a_excluir = data_f.columns[data_f.loc['Serie'] == False]
        # Crear un nuevo DataFrame sin las columnas seleccionadas
        data = data_f[columnas_a_excluir]
    else:
        data = data_f
    data = data[(data != 0).any(axis=1)]
    # Calcular la suma de cada fila y añadir una nueva columna llamada 'Suma'
    data['Suma'] = data.sum(axis=1)

    # Ordenar el DataFrame por la columna 'Suma' en orden descendente
    data = data.sort_values(by='Suma', ascending=False)
    data = data.drop(data.columns[-1], axis=1)

    return data
    

def generar_grafico_barras_df(cantidad, no_serie, fases):
	
    data = matriz_datos (no_serie, fases)
    
    data['Total de tiempo en pantalla'] = data.loc[:,:].sum(axis=1, skipna=True)
    data = data.sort_values(by='Total de tiempo en pantalla', ascending=False)
    data = data[data['Total de tiempo en pantalla'] != 0]
    data = data.head(cantidad)
    nombres_filas = data.index
    valores_ultima_columna = data.iloc[:, -1]

    # Crear un DataFrame con los datos
    df = pd.DataFrame({'Personaje': nombres_filas, 'Tiempo total en pantalla': valores_ultima_columna})

    # Crear el gráfico de barras con Plotly Express
    fig = px.bar(
        df,
        x='Personaje',
        y='Tiempo total en pantalla',
        title='Tiempo total en pantalla de los personajes',
        labels={'Personaje': 'Personaje', 'Tiempo total en pantalla': 'Tiempo total en pantalla'},
        color_discrete_sequence=['rgb(179, 39, 14)'],  # Especifica el color de las barras
        hover_data={'Personaje': True, 'Tiempo total en pantalla': True},  # Incluye datos adicionales para mostrar en el hover
    )

    # Personalizar el tamaño del texto del título
    fig.update_layout(title=dict(text='Tiempo total en pantalla de los personajes', font=dict(size=24)))

    # Personalizar el formato del hovertemplate
    fig.update_traces(
        hovertemplate='Personaje: %{x}<br>Tiempo total en pantalla: %{y}'
    )

    # Ajustar diseño del gráfico
    fig.update_layout(height=500, width=900)

    # Devolver el objeto de figura (Figure) en lugar de mostrarlo
    return fig

def apariciones_pj(no_serie,fases):
    data = matriz_datos (no_serie, fases)

    apariciones_pj = OrderedDict()

    for pj in data.index[0:-1]:
        # Filtrar las columnas que no son cero ni son de tipo string
        columnas_no_cero = data.loc[pj, (data.loc[pj] != 0) & (data.loc[pj].apply(isinstance, args=(float,)))].index.tolist()
        # Excluir la última columna ('Serie') si existe
        apariciones_pj[pj] = columnas_no_cero

    return apariciones_pj



def generar_grafico_barras_num_apariciones(cantidad, fases, no_serie=False):
	
    ordenado_por_longitud = OrderedDict(sorted(apariciones_pj(no_serie,fases).items(), key=lambda x: len(x[1]), reverse=True))
    claves = list(ordenado_por_longitud.keys())[:cantidad]
    longitudes = [len(ordenado_por_longitud[clave]) for clave in claves]
	
    df = pd.DataFrame({'Personaje': claves, 'Apariciones': longitudes})

    # Crear el gráfico de barras con Plotly Express
    fig = px.bar(
        df,
        x='Personaje',
        y='Apariciones',
		title='Nº total de apariciones de los personajes',
        labels={'Personaje': 'Personaje', 'Apariciones': 'Apariciones'},
        color_discrete_sequence=['rgb(179, 39, 14)'],  # Especifica el color de las barras
        hover_data={'Personaje': True, 'Apariciones': True},  # Incluye datos adicionales para mostrar en el hover
    )

    # Personalizar el tamaño del texto del título
    fig.update_layout(title=dict(text='Nº total de apariciones de los personajes', font=dict(size=24)))

    # Personalizar el formato del hovertemplate
    fig.update_traces(
        hovertemplate='Personaje: %{x}<br>Nº de apariciones: %{y}'
    )

    # Ajustar diseño del gráfico
    fig.update_layout(height=500, width=900)

    # Devolver el objeto de figura (Figure) en lugar de mostrarlo
    return fig



def generar_grafico_peliculas_del_char(char,fases, no_serie=False):
    columnas_seleccionadas = char_movie_matrix.columns[char_movie_matrix.loc['Fase'] .isin(fases)]
    data_f = char_movie_matrix[columnas_seleccionadas]
	
    peliculas = {}
    for peli in apariciones_pj(no_serie,fases)[char]:
        peliculas[peli] = data_f.loc[char][peli]

    # Crear un DataFrame con los datos
    df = pd.DataFrame(list(peliculas.items()), columns=['Pelicula', 'Tiempo en pantalla'])
    # Calcular la suma de la columna 'Numeros'
    suma_total = df['Tiempo en pantalla'].sum()

    # Crear el gráfico de barras con Plotly Express
    fig = px.bar(df,
                 x='Pelicula',
                 y='Tiempo en pantalla',
                 title=char + ' (' + str(suma_total) + ' minutos en total)',
                 color_discrete_sequence=['rgb(179, 39, 14)'],
                 labels={'Pelicula': 'Peliculas', 'Tiempo en pantalla': 'Tiempo en pantalla'},
				 hover_data={'Pelicula': True, 'Tiempo en pantalla': True},  # Incluye datos adicionales para mostrar en el hover
    )
    fig.update_traces(
        hovertemplate='Pelicula: %{x}<br>Tiempo en pantalla: %{y} mins'
    )
    # Ajustar diseño del gráfico
    fig.update_layout(height=400, width=800)
    # Devolver el objeto de figura (Figure) en lugar de mostrarlo
    return fig




def grafico_pie_t_pantalla (pelicula):    
    df = char_movie_matrix[char_movie_matrix[pelicula] != 0]
    df[pelicula] = pd.to_numeric(df[pelicula], errors='coerce')
    pie1 = df[pelicula]
    pie1_list = list(pie1.values)
    pie1_list = [round(each,2) for each in pie1_list]
    labels = df.index
	
    # Identificar las 5 mayores porciones
    top5_indices = df[pelicula].nlargest(5).index

# Crear la lista de etiquetas personalizadas
    custom_labels = [name if name in top5_indices else '' for name in labels]

    # Figure
    fig = make_subplots(rows=1, cols=1, specs=[[{'type': 'pie'}]])

    # Generar una paleta de colores de rojo a rosa basada en el número de divisiones
    num_divisiones = len(labels)
    colores = plt.cm.Reds(np.linspace(0, 1, num_divisiones))

    # Convertir la paleta de colores a formato RGBA
    colores_rgba = list(reversed(px.colors.sequential.Reds))
    

    fig.add_trace(
        go.Pie(
            labels=labels,
            values=pie1_list,
            textinfo='text+value',
            hoverinfo="label+value",
            marker=dict(colors=colores_rgba),
            hole=0.3,
			text=custom_labels,
        ),
        row=1, col=1
        
    )

    fig.update_layout(
        title=dict(text="Tiempo en pantalla en " + pelicula + ' (' + movie_lengths[pelicula] +')',font=dict(size=24)),
        annotations=[
            {
                "font": {"size": 20},
                "showarrow": False,
                "text": pelicula,
                "x": 0.5,
                "y": 1.07,
            }
        ],
        height=700,  # Ajusta la altura del gráfico
        width=900,   # Ajusta el ancho del gráfico
    )

    return fig