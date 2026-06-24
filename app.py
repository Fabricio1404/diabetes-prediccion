import streamlit as st
import requests

# Configuración general de la página (título de la pestaña del navegador, ícono, layout)
st.set_page_config(page_title="Predicción de Diabetes", page_icon="", layout="centered")

# URL de tu API de FastAPI, que tiene que estar corriendo en otra terminal
URL_API = "http://127.0.0.1:8000/predict"

st.title("Predicción de Diabetes en Pacientes")
st.write("Ingresá los datos clínicos de la paciente para predecir si tiene diabetes.")

# st.form agrupa todos los inputs para que no se recargue la página con cada cambio,
# solo se ejecuta todo junto cuando se aprieta el botón de submit
with st.form("formulario_paciente"):
    col1, col2 = st.columns(2)  # Dos columnas, para que el formulario no quede tan largo

    with col1:
        pregnancies = st.number_input("Cantidad de embarazos", min_value=0, max_value=20, value=1)
        glucose = st.number_input("Glucosa", min_value=0.0, max_value=300.0, value=120.0)
        blood_pressure = st.number_input("Presión sanguínea", min_value=0.0, max_value=200.0, value=70.0)
        skin_thickness = st.number_input("Espesor de piel", min_value=0.0, max_value=100.0, value=20.0)

    with col2:
        insulin = st.number_input("Insulina", min_value=0.0, max_value=900.0, value=80.0)
        bmi = st.number_input("BMI (índice de masa corporal)", min_value=0.0, max_value=70.0, value=25.0)
        dpf = st.number_input("Función de pedigrí de diabetes", min_value=0.0, max_value=3.0, value=0.5)
        age = st.number_input("Edad", min_value=1, max_value=120, value=30)

    enviado = st.form_submit_button("Predecir")  # El botón que dispara el envío del formulario


# Esto se ejecuta SOLO cuando se aprieta el botón "Predecir"
if enviado:
    # Armamos el diccionario con los mismos nombres de campo que espera la API (DatosPaciente)
    datos = {
        "Pregnancies": pregnancies,
        "Glucose": glucose,
        "BloodPressure": blood_pressure,
        "SkinThickness": skin_thickness,
        "Insulin": insulin,
        "BMI": bmi,
        "DiabetesPedigreeFunction": dpf,
        "Age": age
    }

    try:
        # Le mandamos los datos a la API de FastAPI por POST, esperando como máximo 5 segundos
        respuesta = requests.post(URL_API, json=datos, timeout=5)

        if respuesta.status_code == 200:
            resultado = respuesta.json()  # Convertimos la respuesta JSON a diccionario de Python

            if resultado["prediccion"] == 1:
                st.error(f"Resultado: **{resultado['resultado']}**")
            else:
                st.success(f"Resultado: **{resultado['resultado']}**")

            st.metric("Probabilidad de diabetes", f"{resultado['probabilidad'] * 100:.2f}%")
        else:
            st.error(f"Error en la API: {respuesta.status_code}")

    except requests.exceptions.ConnectionError:
        # Este error aparece si el backend (uvicorn) no está corriendo
        st.error("No se pudo conectar con la API. Verificá que el backend (uvicorn) esté corriendo.")


# --- Sección de estadísticas del modelo (requisito de la consigna) ---
st.divider()
st.subheader("Rendimiento del modelo")
st.write("Métricas obtenidas en el conjunto de test (Árbol de Decisión con Pre-Poda):")

col_a, col_b, col_c = st.columns(3)
col_a.metric("Accuracy", "87.01%")
col_b.metric("Recall", "79.63%")
col_c.metric("Modelo", "Árbol Pre-Poda")

st.caption(
    "Se priorizó el Recall sobre el Accuracy general, porque en un contexto médico "
    "es más grave no detectar un caso real de diabetes que generar una falsa alarma."
)