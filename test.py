import streamlit as st
import pandas as pd

# Cargar el archivo Excel con preguntas
preguntas_df = pd.read_csv('bd.csv')
preguntas_df = preguntas_df.sample(frac=1).reset_index(drop=True)  # Desordenar preguntas

# Definir los animales y las posibles respuestas
animales = preguntas_df['animal'].unique()
respuestas = ['Siempre', 'A veces', 'Poco', 'Nunca']

# Inicializar el contador de puntos para cada animal
puntos_animales = {animal: 0 for animal in animales}

# Interfaz de usuario para preguntas
for index, row in preguntas_df.iterrows():
    respuesta_usuario = st.radio(row['item'], respuestas)

    # Lógica de puntuación basada en el tipo de pregunta
    puntos = 0
    if row['tipo'] == 1:
        if respuesta_usuario == 'Siempre':
            puntos = 2
        elif respuesta_usuario == 'A veces':
            puntos = 1
    elif row['tipo'] == 2:
        if respuesta_usuario == 'Nunca':
            puntos = 2
        elif respuesta_usuario == 'Poco':
            puntos = 1

    # Sumar los puntos al animal correspondiente
    puntos_animales[row['animal']] += puntos

# Mostrar el animal con la puntuación más alta al final del test
if st.button('Finalizar Test'):
    animal_dominante = max(puntos_animales, key=puntos_animales.get)
    st.write(f"Tu animal es: {animal_dominante}")