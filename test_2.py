import streamlit as st
import pandas as pd

# Función para cargar y preparar los datos desde Excel
def cargar_datos_excel(ruta):
    try:
        df = pd.read_excel(ruta, engine='openpyxl')
        df = df.dropna(subset=['item', 'animal'], how='any').reset_index(drop=True)
        return df
    except Exception as e:
        st.error(f"Error al cargar los datos desde Excel: {e}")
        return pd.DataFrame()

# Cargar el archivo Excel con preguntas
ruta_excel = './bd.xlsx'  # Asegúrate de ajustar esto a la ruta correcta
preguntas_df = cargar_datos_excel(ruta_excel)

# Inicializar el estado de sesión si es necesario
if 'preguntas_mostradas' not in st.session_state:
    st.session_state.update({
        'preguntas_mostradas': [],
        'puntos_animales': {},
        'test_finalizado': False,
        'test_iniciado': False,
        'respuesta_usuario': None,
        'ultimo_animal': None
    })

# Función para seleccionar la siguiente pregunta de manera equitativa
def seleccionar_siguiente_pregunta():
    if len(st.session_state['preguntas_mostradas']) >= len(preguntas_df):
        st.session_state['test_finalizado'] = True
        return None
    preguntas_disponibles = preguntas_df[~preguntas_df['id'].isin(st.session_state['preguntas_mostradas'])]
    siguiente_pregunta = preguntas_disponibles.sample(n=1).iloc[0]
    st.session_state['preguntas_mostradas'].append(siguiente_pregunta['id'])
    st.session_state['ultimo_animal'] = siguiente_pregunta['animal']
    return siguiente_pregunta

# Función para asignar puntos a los animales según la respuesta y el tipo de pregunta
def asignar_puntos(respuesta, pregunta):
    puntos = 0
    if pregunta['tipo'] == 1:
        if respuesta == 'Siempre':
            puntos = 2
        elif respuesta == 'A veces':
            puntos = 1
    elif pregunta['tipo'] == 2:
        if respuesta == 'Nunca':
            puntos = 2
        elif respuesta == 'Poco':
            puntos = 1

    animales = [pregunta['animal']]
    if not pd.isna(pregunta.get('animal 2', pd.NA)):
        animales.append(pregunta['animal 2'])

    for animal in animales:
        if animal not in st.session_state['puntos_animales']:
            st.session_state['puntos_animales'][animal] = 0
        st.session_state['puntos_animales'][animal] += puntos

    # Verificar si algún animal ha alcanzado un umbral de puntos para terminar el test
    comprobar_final_test()

# Comprobación del porcentaje de puntos de cada animal
def comprobar_final_test():
    total_puntos = sum(st.session_state['puntos_animales'].values())
    for puntos in st.session_state['puntos_animales'].values():
        if total_puntos > 0 and (puntos / total_puntos) > 0.75:  # Umbral del 75%
            st.session_state['test_finalizado'] = True
            break

# Interfaz de usuario para el test
if st.button("Comenzar el Test") and not st.session_state['test_iniciado']:
    st.session_state['test_iniciado'] = True
    pregunta_actual = seleccionar_siguiente_pregunta()

if st.session_state['test_iniciado'] and not st.session_state['test_finalizado']:
    if 'pregunta_actual' in locals() and pregunta_actual is not None:
        opciones_respuesta = ['Siempre', 'A veces', 'Poco', 'Nunca']
        respuesta_usuario = st.selectbox(pregunta_actual['item'], opciones_respuesta, key=pregunta_actual['id'])
        
        if st.button('Siguiente'):
            asignar_puntos(respuesta_usuario, pregunta_actual)
            pregunta_actual = seleccionar_siguiente_pregunta()

# Finalizar el test
if st.session_state['test_finalizado']:
    st.write("Has completado el test.")
    if st.session_state['puntos_animales']:
        animal_dominante = max(st.session_state['puntos_animales'], key=st.session_state['puntos_animales'].get)
        st.write(f"Tu animal dominante es: {animal_dominante}")
        # Mostrar la puntuación de cada animal para mayor claridad
        st.write("Puntuaciones por animal:")
        for animal, puntos in st.session_state['puntos_animales'].items():
            st.write(f"{animal}: {puntos}")
    else:
        st.write("No se han acumulado suficientes puntos para determinar un animal dominante.")


