from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# Creamos la aplicación FastAPI. "app" es el objeto que va a manejar todas las rutas/endpoints
app = FastAPI(title="API Predicción de Diabetes")

# Cargamos el modelo entrenado UNA SOLA VEZ, cuando arranca el servidor
# (no lo cargamos dentro de cada request, sería muy lento volver a leer el archivo cada vez)
modelo = joblib.load("models/modelo_diabetes.pkl")


# Pydantic define la "forma" que tienen que tener los datos que llegan por JSON.
# Si alguien manda un dato faltante o con el tipo incorrecto, FastAPI rechaza la
# petición automáticamente, sin que tengamos que validar nada a mano.
class DatosPaciente(BaseModel):
    Pregnancies: int
    Glucose: float
    BloodPressure: float
    SkinThickness: float
    Insulin: float
    BMI: float
    DiabetesPedigreeFunction: float
    Age: int


@app.get("/")
def inicio():
    return {"mensaje": "API de predicción de diabetes funcionando correctamente"}


@app.post("/predict")
def predecir(datos: DatosPaciente):
    # datos llega ya validado por Pydantic (FastAPI se encarga de eso solo).
    # Lo convertimos a DataFrame porque así fue entrenado el modelo (con columnas con nombre,
    # no con una simple lista de números)
    datos_df = pd.DataFrame([datos.model_dump()])
    # .model_dump() convierte el objeto Pydantic a un diccionario
    # pd.DataFrame([...]) lo envuelve en una fila de DataFrame con las columnas correctas

    prediccion = modelo.predict(datos_df)[0]
    # .predict() siempre devuelve un array (porque podría predecir varias filas a la vez),
    # por eso tomamos el [0] para quedarnos con el único resultado de esta fila

    probabilidad = modelo.predict_proba(datos_df)[0][1]
    # predict_proba devuelve la probabilidad de cada clase [prob_clase_0, prob_clase_1]
    # Tomamos [1] porque es la probabilidad de "Diabetes" (clase 1)

    return {
        "prediccion": int(prediccion),  # 0 = no diabetes, 1 = diabetes
        "resultado": "Diabetes" if prediccion == 1 else "No Diabetes",
        "probabilidad": round(float(probabilidad), 4)
    }