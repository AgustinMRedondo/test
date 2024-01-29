import streamlit as st
import pandas as pd

# Cargar el archivo CSV con preguntas
preguntas_df = pd.read_csv('bd.csv')
preguntas_df = preguntas_df.sample(frac=1).reset_index(drop=True)  # Desordenar preguntas

# Inicializar el estado de sesión si es necesario
if 'indice_actual' not in st.session_state:
    st.session_state.indice_actual = 0
    st.session_state.puntos_animales = {animal: 0 for animal in preguntas_df['animal'].unique()}
    st.session_state.test_finalizado = False
    st.session_state.test_iniciado = False

# Botón para comenzar el test
if not st.session_state.test_iniciado:
    if st.button("Comenzar el Test"):
        st.session_state.test_iniciado = True

# Mostrar la pregunta actual si el test está iniciado y no ha finalizado
if st.session_state.test_iniciado and not st.session_state.test_finalizado:
    indice_actual = st.session_state.indice_actual
    pregunta_actual = preguntas_df.iloc[indice_actual]

    # Mostrar la pregunta actual
    st.write(pregunta_actual['item'])

    # Formulario para la selección de respuesta
    with st.form(key='mi_formulario'):
        opciones_respuesta = ['Siempre', 'A veces', 'Poco', 'Nunca']
        respuesta_seleccionada = st.selectbox("Selecciona una respuesta:", opciones_respuesta, index=None)

        # Botón para procesar la respuesta confirmada y avanzar a la siguiente pregunta
        submit_button = st.form_submit_button(label='Siguiente')

    if submit_button:
        animal_actual = pregunta_actual['animal']

        # Lógica de puntuación basada en la respuesta seleccionada
        puntos = 0
        if pregunta_actual['tipo'] == 1:
            if respuesta_seleccionada == 'Siempre':
                puntos += 2
            elif respuesta_seleccionada == 'A veces':
                puntos += 1
        elif pregunta_actual['tipo'] == 2:
            if respuesta_seleccionada == 'Nunca':
                puntos += 2
            elif respuesta_seleccionada == 'Poco':
                puntos += 1

        # Sumar los puntos al animal correspondiente
        st.session_state.puntos_animales[animal_actual] += puntos

        # Sumar los puntos al animal correspondiente
        st.session_state.puntos_animales[animal_actual] += puntos

        # Comprobar si el test debe finalizar
        total_puntos = sum(st.session_state.puntos_animales.values())
        if indice_actual >= 9 or (indice_actual > 4 and any(puntos > 0.75 * total_puntos for puntos in st.session_state.puntos_animales.values())):
            st.session_state.test_finalizado = True
        else:
            # Avanzar a la siguiente pregunta si el test no ha finalizado
            st.session_state.indice_actual += 1

# Mostrar el resultado al final del test
if st.session_state.test_finalizado:
    st.write("Has completado el test")

    # Mostrar el animal con la puntuación más alta al final del test
    animal_dominante = max(st.session_state.puntos_animales, key=st.session_state.puntos_animales.get)
    st.write(f"Tu animal dominante es: {animal_dominante}")

    # Mostrar una tabla con los puntos de cada animal
    puntos_df = pd.DataFrame.from_dict(st.session_state.puntos_animales, orient='index', columns=['Puntos'])
    st.table(puntos_df)

