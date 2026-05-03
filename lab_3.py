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
         
    #GRAFICO
    vehiculos["RangoCategoria"] = pd.cut(
    vehiculos["Electric_Range"],
    bins=[0, 100, 250, vehiculos["Electric_Range"].max()],
    labels=["Bajo", "Medio", "Alto"]
    )

    conteo = vehiculos["RangoCategoria"].value_counts()

    st.write(conteo)

    fig, ax = plt.subplots()
    conteo.plot(kind="bar", ax=ax)
    ax.set_title("Vehículos por Rango")
    ax.set_xlabel("Categoría")
    ax.set_ylabel("Cantidad")
    st.pyplot(fig)    

    #ANALIZIS
    if "RangoCategoria" in vehiculos.columns:

        agrupado = vehiculos.groupby("RangoCategoria").agg({
        "Base_MSRP": "mean",
        "Model Year": "mean",
        "Electric_Range": "std"
    })

    st.subheader("Análisis Vehículos")
    st.dataframe(agrupado)

    # GUARDAR
    if st.button("Guardar Vehículos"):
        vehiculos.to_csv("vehiculos_modificado.csv", index=False)
        st.success("Archivo guardado")

# GIMNASIO

elif opcion == "Gimnasio":
    mostrar_info(gym, "Gimnasio")

    # FILTROS
    if "Calories_Burned" in gym.columns:
        calorias = st.slider(
        "Calorías mínimas",
        float(gym["Calories_Burned"].min()),
        float(gym["Calories_Burned"].max())
    )

    filtrado = gym[gym["Calories_Burned"] >= calorias]
    st.dataframe(filtrado)


    # Grasa
    if "Fat_Percentage" in gym.columns:
        grasa = st.slider(
        "Grasa máxima (%)",
        float(gym["Fat_Percentage"].min()),
        float(gym["Fat_Percentage"].max())
    )

    filtrado2 = gym[gym["Fat_Percentage"] <= grasa]
    st.dataframe(filtrado2)
    
# INGRESO DE DATOS
    st.subheader("Agregar nuevo registro")
    nueva_cal = st.number_input("Calorías", 0)
    if st.button("Agregar"):
        nuevo = {"Calories Burned": nueva_cal}
        gym.loc[len(gym)] = nuevo
        st.success("Dato agregado")

    # CATEGORÍA
    if "Calories Burned" in gym.columns:
        gym["Nivel"] = pd.cut(gym["Calories Burned"], bins=3, labels=["Bajo", "Medio", "Alto"])
        conteo = gym["Nivel"].value_counts()

        fig, ax = plt.subplots()
        conteo.plot(kind="bar", ax=ax)
        st.pyplot(fig)
    
    if st.button("Guardar Gym"):
        gym.to_csv("gym_modificado.csv", index=False)