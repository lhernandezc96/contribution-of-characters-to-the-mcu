import streamlit as st
import funciones as EDA
import texto as t
import warnings

# Ignorar todos los warnings
warnings.filterwarnings("ignore")


def main():
    st.title("EDA: Tiempo en pantalla de los personajes del MCU")
    st.image('src/data/Endgame_poster.jpg', use_column_width=True)
    st.markdown(t.texto_markdown_1)

    # Crear checkboxes en el sidebar
    fase_1 = st.sidebar.checkbox('Fase 1',value=True)
    fase_2 = st.sidebar.checkbox('Fase 2',value=True)
    fase_3 = st.sidebar.checkbox('Fase 3',value=True)
    fase_4 = st.sidebar.checkbox('Fase 4',value=True)

    # Crear una lista con los números de las fases marcadas
    fases_marcadas = [0]
    if fase_1:
        fases_marcadas.append(1)
    if fase_2:
        fases_marcadas.append(2)
    if fase_3:
        fases_marcadas.append(3)
    if fase_4:
        fases_marcadas.append(4)

   
    # Widget de desplegable para seleccionar la opción
    opcion_serie = st.sidebar.selectbox("¿Quieres que se tengan en cuenta las series?", ['Sí','No'])
    if opcion_serie == 'Sí':
        no_serie = False
    else:
        no_serie = True      

    datos = EDA.matriz_datos (no_serie, fases_marcadas)

    # Widget para ingresar un número
    n2 = st.number_input("Ingrese un número", value=10,key=2)
    figura4 = EDA.generar_grafico_barras_df(n2,no_serie,fases_marcadas)
    # Muestra la figura con st.plotly_chart
    if figura4:
        st.plotly_chart(figura4,use_container_width=True,use_container_heigth=True)
        #st.plotly_chart(figura3)

    # Widget para ingresar un número
    n = st.number_input("Ingrese un número", value=15,key=1)
    figura3 = EDA.generar_grafico_barras_num_apariciones(n,fases_marcadas,no_serie)

    # Muestra la figura con st.plotly_chart
    if figura3:
        st.plotly_chart(figura3,use_container_width=True,use_container_heigth=True)
        #st.plotly_chart(figura3)

    # Widget de desplegable para seleccionar la opción
    opcion_seleccionada2 = st.selectbox("Selecciona una opción", list(datos.index))

    # Lógica para llamar a la función de representación del gráfico según la opción seleccionada
    figura2 = EDA.generar_grafico_peliculas_del_char(opcion_seleccionada2,fases_marcadas,no_serie) 

    # Muestra la figura con st.plotly_chart
    if figura2:
        #st.plotly_chart(figura2,use_container_width=True,use_container_heigth=True)
        st.plotly_chart(figura2)

    # Widget de desplegable para seleccionar la opción
    opcion_seleccionada = st.selectbox("Selecciona una opción", list(datos.columns))

    # Lógica para llamar a la función de representación del gráfico según la opción seleccionada
    figura = EDA.grafico_pie_t_pantalla(opcion_seleccionada) 

    # Muestra la figura con st.plotly_chart
    if figura:
        st.plotly_chart(figura)
        
    st.image('src/data/marvel-mcu-gif.gif', use_column_width=True)
    st.markdown(t.texto_markdown_2)
    
    


if __name__ == "__main__":
    main()

