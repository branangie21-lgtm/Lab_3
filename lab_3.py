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

    #GRAFICO
    gym["NivelFrecuencia"] = pd.cut(
    gym["Workout_Frequency (days/week)"],
    bins=[0, 3, 5, 7],
    labels=["Baja", "Moderada", "Alta"]
    )

    conteo = gym["NivelFrecuencia"].value_counts()

    st.write(conteo)

    fig, ax = plt.subplots()
    conteo.plot(kind="bar", ax=ax)
    ax.set_title("Frecuencia de Entrenamiento")
    ax.set_xlabel("Nivel")
    ax.set_ylabel("Cantidad")
    st.pyplot(fig)
    #ANALIZIS
    agrupado = gym.groupby("NivelFrecuencia").agg({
    "Session_Duration (hours)": "mean",
    "Experience_Level": "mean",
    "BMI": "std"
    })

    st.subheader("Análisis Gimnasio")
    st.dataframe(agrupado)
#VIDEOJUEGOS
elif opcion == "Videojuegos":
    mostrar_info(juegos, "Videojuegos")
    juegos["price"] = juegos["price"].replace('[\$,]', '', regex=True)
    juegos["price"] =  pd.to_numeric(juegos["price"],errors = 'coerce')

    #FILTROS
    if "price" in juegos.columns:
        precio = st.slider ("Precio máximo", float (juegos["price"].min()), float (juegos["price"].max()))
        filtrado = juegos[juegos["price"]<= precio]
        st.dataframe(filtrado)

    juegos ["salePercentage"]= juegos["salePercentage"].replace('%', '', regex=True)
    juegos["salePercentage"] = pd.to_numeric(juegos["salePercentage"], errors='coerce')
    if "salePercentage"in juegos.columns:
        
      descuento = st.slider(
        "Descuento mínimo (%)",
        float(juegos["salePercentage"].min()),
        float(juegos["salePercentage"].max())
    )  
    
    filtrado_desc = juegos[juegos["salePercentage"] >= descuento]
    st.dataframe(filtrado_desc)
    #INGRESO DE DATOS
    nombre = st.text_input("Nombre")
    precio = st.number_input("Precio", 0.0)

    if st.button("Agregar"):
        nuevo = {col: None for col in juegos.columns}  # crea todas las columnas

        if "name" in juegos.columns:
            nuevo["name"] = nombre

        if "price" in juegos.columns:
         nuevo["price"] = precio

        nuevo_df = pd.DataFrame([nuevo])

        juegos = pd.concat([juegos, nuevo_df], ignore_index=True)

        st.success("Juego agregado correctamente")
    # CATEGORÍA
    if "price" in juegos.columns:
        juegos["Categoria_Precio"] = pd.cut(juegos["price"], bins=3, labels=["Bajo", "Medio", "Alto"])
        conteo = juegos["Categoria_Precio"].value_counts()

        fig, ax = plt.subplots()
        conteo.plot(kind="bar", ax=ax)
        st.pyplot(fig)

    if st.button("Guardar Juegos"):
        juegos.to_csv("juegos_modificado.csv", index=False)
    #GRAFICO
    juegos["price"] = pd.to_numeric(juegos["price"], errors = "coerce")
    juegos["salePercentage"] = juegos["salePercentage"].replace('%', '', regex=True)
    juegos["salePercentage"] = pd.to_numeric(juegos["salePercentage"], errors="coerce")
    juegos["GamaJuego"] = pd.cut(
    juegos["price"], 
    bins=[0, 10, 24, juegos["price"].max()],
    labels=["Baja", "Media", "Alta"]
    )
    conteo = juegos["GamaJuego"].value_counts()

    st.write(conteo)

    fig, ax = plt.subplots()
    conteo.plot(kind="bar", ax=ax)
    ax.set_title("Gama de Videojuegos")
    ax.set_xlabel("Categoría")
    ax.set_ylabel("Cantidad")
    st.pyplot(fig)

    #Analizis
    agrupado = juegos.groupby("GamaJuego").agg({
    "price": "mean",
    "salePercentage": "mean"
    })

    agrupado["Desv_Precio"] = juegos.groupby("GamaJuego")["price"].std()

    st.subheader("Análisis Videojuegos")
    st.dataframe(agrupado)
# NETFLIX

elif opcion == "Netflix":

    # FILTRO
    mostrar_info(netflix, "Netflix")
    peliculas = netflix[netflix["type"] == "Movie"]
    peliculas["duration"] = peliculas["duration"].str.replace(" min", "")
    peliculas["duration"] = pd.to_numeric(peliculas["duration"], errors="coerce")
    duracion = st.slider(
    "Duración mínima (minutos)",
    int(peliculas["duration"].min()),
    int(peliculas["duration"].max())
)

    filtrado = peliculas[peliculas["duration"] >= duracion]

    st.dataframe(filtrado)
    
    if "release_year" in netflix.columns:
        año = st.slider("Año", int(netflix["release_year"].min()), int(netflix["release_year"].max()))
        filtrado = netflix[netflix["release_year"] == año]
        st.dataframe(filtrado)
    # CATEGORÍA
    if "type" in netflix.columns:
        conteo = netflix["type"].value_counts()

        fig, ax = plt.subplots()
        conteo.plot(kind="bar", ax=ax)
        st.pyplot(fig)

    if st.button("Guardar Netflix"):
        netflix.to_csv("netflix_modificado.csv", index=False)
    #GRAFICO
    def clasificar(x):
        if x in ["G", "TV-Y", "TV-G", "TV-Y7", "TV-Y7-FV"]:
            return "Niños"
        elif x in ["PG", "TV-PG"]:
            return "Adolescentes"
        elif x in ["PG-13", "TV-14"]:
         return "Adultos Jóvenes"
        elif x in ["R", "TV-MA", "NC-17"]:
            return "Adultos"
        else:
            return "Otro"

    netflix["TipoAudiencia"] = netflix["rating"].apply(clasificar)

    conteo = netflix["TipoAudiencia"].value_counts()

    st.write(conteo)

    fig, ax = plt.subplots()
    conteo.plot(kind="bar", ax=ax)
    ax.set_title("Audiencia en Netflix")
    ax.set_xlabel("Categoría")
    ax.set_ylabel("Cantidad")
    st.pyplot(fig)  
    #ANALIZIS
    tipo_comun = netflix.groupby("TipoAudiencia")["type"].agg(lambda x: x.mode()[0])


    peliculas = netflix[netflix["type"] == "Movie"].copy()
    peliculas["duration"] = peliculas["duration"].str.replace(" min", "")
    peliculas["duration"] = pd.to_numeric(peliculas["duration"], errors="coerce")

    duracion_prom = peliculas.groupby("TipoAudiencia")["duration"].mean()

    st.subheader("Tipo más común")
    st.dataframe(tipo_comun)

    st.subheader("Duración promedio")
    st.dataframe(duracion_prom)