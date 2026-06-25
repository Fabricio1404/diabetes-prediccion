# Predicción de Diabetes en Pacientes

Trabajo Práctico Final - Taller de Lenguajes de Programación III (Python para Ciencia de Datos)
Instituto Politécnico Formosa (IPF)

## Descripción del proyecto
Sistema de Machine Learning diseñado para predecir si una paciente presenta diabetes o no, basado en variables clínicas (glucosa, insulina, IMC, edad, entre otras). El proyecto abarca el ciclo de vida completo de Ciencia de Datos, desde el EDA hasta el despliegue de una API funcional.

## Equipo de Trabajo y Roles
Este proyecto fue desarrollado de manera integral por el grupo, con una distribución de tareas en el análisis y ejecución técnica:

* **Giuricich Facundo:** Responsable de la carga de datos y exploración inicial.
* **Augusto Fabricio:** Responsable del preprocesamiento, limpieza de nulos y estandarización.
* **Galban Leo:** Responsable de la selección de modelos, entrenamiento, evaluación y exportación del modelo final.

*(El desarrollo de la API y la interfaz fue un trabajo colaborativo final para el despliegue del producto).*

## Dataset
**Pima Indians Diabetes Database** (Kaggle)
- 768 filas, 9 columnas.
- Variable objetivo: `Outcome` (0 = sano, 1 = diabético).

## Stack tecnológico
| Componente | Tecnología |
|---|---|
| Análisis y modelado | Python, Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn |
| Exportación del modelo | Joblib |
| Backend / API | FastAPI, Uvicorn, Pydantic |
| Frontend | Streamlit |
