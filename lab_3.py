#Universidad del Valle de Guatemala
#Facultad de Ingeniería
#Departamento de Ciencias de la Computación
# CC2005 – Algoritmos y Programación Básica
#Laboratorio 3: Exploración y Análisis de Múltiples Conjuntos de Datos
#Angie Bran 26851 y Tomas Leonzo 26382
# 02/05/2026

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
st.header("Universidad del Valle de Guatemala")
st.subheader("CC2005 – Algoritmos y Programación Básica")
st.title(" Laboratorio 3 - Conjunto de Datos")

vehiculos = pd.read_csv("Electric_Vehicle_Population.csv")
gym = pd.read_csv("GymExerciseTracking.csv")
juegos = pd.read_csv("steam_store_data_2024.csv")
netflix = pd.read_csv("netflix_titles.csv")
opcion = st.sidebar.selectbox(
    "Selecciona dataset",
    ["Vehículos", "Gimnasio", "Videojuegos", "Netflix"]
)
def mostrar_info(df, nombre):
    st.subheader(f"Dataset: {nombre}")
    st.write("Dimensiones:", df.shape)
    st.write("Columnas:", df.columns.tolist())
    st.dataframe(df.head(6))
    st.write("Estadísticas:")
    st.write(df.describe())
    
    #VEHICULOS
if opcion == "Vehículos":
    mostrar_info(vehiculos, "Vehículos")

    # FILTROS
    st.subheader("Filtros")
    if "Model Year" in vehiculos.columns:
        año = st.slider("Filtrar por año", int(vehiculos["Model Year"].min()), int(vehiculos["Model Year"].max()))
        filtrado = vehiculos[vehiculos["Model Year"] == año]
        st.dataframe(filtrado)
    if "Base_MSRP" in vehiculos.columns:

        vehiculos["Base_MSRP"] = pd.to_numeric(vehiculos["Base_MSRP"], errors="coerce")

        precio = st.slider(
        "Precio máximo",
        int(vehiculos["Base_MSRP"].min()),
        int(vehiculos["Base_MSRP"].max())
    )
        
        filtrado_precio = vehiculos[vehiculos["Base_MSRP"] <= precio]

    st.write("Vehículos filtrados por precio:")
    st.dataframe(filtrado_precio)
# CATEGORIZACIÓN
    if "Electric_Range" in vehiculos.columns:
        def categoria_rango(x):
            if x < 100:
                return "Bajo"
            elif x < 300:
                return "Medio"
            else:
                return "Alto"

        vehiculos["Categoria_Rango"] = vehiculos["Electric_Range"].apply(categoria_rango)

        conteo = vehiculos["Categoria_Rango"].value_counts()

        st.subheader("Gráfica")
        fig, ax = plt.subplots()
        conteo.plot(kind="bar", ax=ax)
        st.pyplot(fig)