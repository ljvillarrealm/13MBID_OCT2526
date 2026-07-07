# 13MBID – Actividades Prácticas 1 y 2 - Implementación de metodología híbrida para proyecto de predicción de mora crediticia

![barra escudo viu](/.project_resources/barra_escudo_viu.png)

*Master Universitario en Big Data y Ciencia de Datos  
Universidad Internacional de Valencia*  
**13MBID - Metodologías de Gestión de Proyectos de Big Data**  

Actividad Práctica 1  

Prof: Dr. Horacio Kuna  
Alumno: Leonardo Villarreal (💜 DATA)  
Edición Octubre 25-26  

## Descripción del proyecto

Una entidad financiera desea obtener conocimiento a partir de su base histórica de créditos para predecir la probabilidad de que un nuevo crédito entre en mora. Partiendo de un MVP previo, este repositorio lleva ese modelo desde la experimentación en libretas hasta un producto de datos operable en producción, aplicando prácticas de DataOps y MLOps sobre la estructura metodológica de CRISP-DM y una gestión ágil con Scrum (GitHub Projects).

El trabajo se divide en dos iteraciones:

* Actividad Práctica 1 - Comprensión del negocio y de los datos, y preparación de los datos: versionado con DVC, exploración y control de calidad automatizado, e integración de un dataset enriquecido.
* Actividad Práctica 2 - Modelado, evaluación y despliegue: comparación de técnicas con registro en MLflow, optimización de hiperparámetros, testing del modelo y exposición del producto vía API y Web App.

## Enlaces del proyecto

| Recurso | Enlace |
| -- | -- |
| Repositorio | https://github.com/ljvillarrealm/13MBID_OCT2526 |
| Gestión de tareas (GitHub Projects) | https://github.com/users/ljvillarrealm/projects/3/views/1 |
| API de predicción (Render) | https://one3mbid-oct2526-api-si7i.onrender.com |
| Web App de consulta (Streamlit) | https://ljvillarrealm-13mbid-oct2526-webapp-vextra.streamlit.app/| 

## Estructura del repositorio

* config/ - archivos de configuración del entorno a replicar vía miniconda/conda, pip o uv.
* data/ - datos del proyecto, versionados con DVC:
* raw/ - datos en su estado original (datos_creditos.csv, datos_tarjetas.csv).
* processed/ - datos transformados durante el preprocesamiento (datos_integrados.csv), usados para entrenamiento y visualizaciones.
* notebooks/ - libretas de experimentación (visualización, procesamiento y modelado).
* src/ - scripts reproducibles que reemplazan a las libretas en el pipeline (visualización, perfilado, procesamiento, entrenamiento).
* test/ - validaciones automatizadas de calidad de datos y de modelo (PyTest).
* app/ - aplicación web (Streamlit) y API (FastAPI) para el consumo del modelo por usuarios finales y otros sistemas.
* models/ - modelo productivo (prod_model.pkl) y preprocesador (prod_preprocessor.pkl), versionados como salidas del pipeline.
* metrics/ - métricas del modelo (train_metrics.json) para comparar versiones a lo largo del tiempo.
* docs/output/ - reportes generados (perfilado, calidad de datos, verificación de integración) e imágenes del análisis.
* examples/ - ejemplos de uso del template.

## Herramientas utilizadas

| Area | Herramientas |
| -- | -- |
| Gestión ágil y control de versiones | GitHub, GitHub Projects |
| Versionado de datos y pipelines | DVC |
| Calidad de datos | Pandera, Great Expectations, PyTest, ydata-profiling |
| Modelado y experimentación | scikit-learn, MLflowDespliegueFastAPI, Streamlit, Render |

## Pipeline reproducible (DVC)

El flujo completo (visualización → perfilado → control de calidad → integración → entrenamiento → testing del modelo) está encadenado en un pipeline de DVC, donde cada etapa declara sus dependencias y salidas. Se ejecuta de punta a punta con:

``` bash
bashdvc repro      # reproduce todas las etapas del pipeline
dvc push       # sincroniza datos y artefactos con el remote configurado
```

Los experimentos de modelado (técnica, parámetros y métricas de cada ejecución) quedan registrados con MLflow, permitiendo auditar y reproducir la elección del modelo final.

## Modelo y resultados

Se evaluaron cinco técnicas (Regresión Logística, LinearSVC, KNN, Árbol de Decisión y HistGradientBoosting) bajo un esquema reproducible con submuestreo para atender el desbalance de clases (clase de mora cercano a 17 %), validación cruzada de 5 folds y un conjunto de test independiente. El mejor desempeño global lo obtuvo HistGradientBoosting, que tras optimización de hiperparámetros (RandomizedSearchCV + GridSearchCV) alcanzó ROC AUC 0.9534 y recall 0.9153 sobre la clase de mora, superando el umbral de efectividad del 80 % requerido por el negocio.

## Instrucciones de replicación

Para replicar este repositorio en una instancia local:

1. Clonar el repositorio con git clone.
2. Replicar el entorno con alguna de las opciones listadas en el archivo de entornos.
3. Ejecutar la libreta de verificación para comprobar la instalación.
4. Descargar los datos y artefactos versionados con dvc pull.
5. (Opcional) Reproducir el pipeline completo con dvc repro.

### Levantar los servicios en local

``` bash
# MLFlow
mlflow ui

# API de predicción (FastAPI)
fastapi run .\app\api.py 

# Web App de consulta (Streamlit)
streamlit run .\app\ui_vEXTRA.py # o ui.py según la versión deseada
```

* ui_vEXTRA.py - Permite ingresar los datos originales del cliente (edad, ingresos, etc.); los atributos derivados que requiere el modelo se calculan internamente antes de consultar la API.
* ui.py - Permite ingresar los datos tal y como requiere el modelo.

## Declaración sobre uso de IA

Este trabajo se realizó con apoyo de herramientas de IA para el diseño crítico de la solución, autocompletado de código y mejora de redacción. Toda acción asistida por IA fue supervisada, revisada y validada por el autor, quien asume la responsabilidad final sobre las decisiones técnicas y metodológicas, y sobre la veracidad de lo documentado.
