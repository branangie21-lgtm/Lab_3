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

vehiculos = pd.read_csv("Electric_Vehicle_Population-2.csv")
gym = pd.read_csv("GymExerciseTracking.csv")
juegos = pd.read_csv("steam_store_data_2024.csv")
netflix = pd.read_csv("netflix_titles.csv")