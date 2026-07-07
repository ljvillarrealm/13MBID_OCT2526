from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pandas as pd
import joblib
from typing import Dict

app = FastAPI(
    title="Modelo de Predicción de Mora en Créditos",
    description="Una API para predecir la probabilidad de mora en créditos utilizando un modelo de machine learning",
    version="1.0.0"
)



class PredictionRequest(BaseModel):
    duracion_credito: int = Field(..., description="Credito - Duracion del credito")
    situacion_vivienda: str = Field(..., description="Cliente - Situacion de la viviente")
    ingresos: int = Field(..., description="Cliente - Ingresos")
    objetivo_credito: str = Field(..., description="Cliente - Objetivo del credito")
    pct_ingreso: float = Field(..., description="Cliente - Porcentaje de ingreso")
    tasa_interes: float = Field(..., description="Credito - Tasa de interes")
    estado_credito: int = Field(..., description="Credito - Estado del credito")
    antiguedad_cliente: float = Field(..., description="Cliente - Antiguedad")
    estado_civil: str = Field(..., description="Cliente - Estado civil")
    estado_cliente: str = Field(..., description="Cliente - Estado")
    genero: str = Field(..., description="Cliente - Genero")
    limite_credito_tc: float = Field(..., description="Credito - Limite de credito")
    nivel_educativo: str = Field(..., description="Cliente - Nivel educativo")
    personas_a_cargo: float = Field(..., description="Cliente - Personas a cargo")
    capacidad_pago: float = Field(..., description="Cliente - Capacidad de pago")
    ratio_endeudamiento: float = Field(..., description="Cliente - ratio de endeudamiento")
    operaciones_mensuales: float = Field(..., description="Cliente - Operaciones mensuales")
    gasto_transaccion_promedio: float = Field(..., description="Cliente - Gasto promedio por transaccion")
    presion_financiera: float = Field(..., description="Ciente - Presion financiera")
    antiguedad_relativa: float = Field(..., description="Asesor - Antiguedad relativa")

    class Config:
        json_schema_extra = {
            "duracion_credito": 2,
            "situacion_vivienda": "PROPIA",
            "ingresos": 9600,
            "objetivo_credito": "EDUCACIÓN",
            "pct_ingreso": 0.1,
            "tasa_interes": 11.14,
            "estado_credito": 0,
            "antiguedad_cliente": 39.0,
            "estado_civil": "CASADO",
            "estado_cliente": "ACTIVO",
            "genero": "M",
            "limite_credito_tc": 12691.0,
            "nivel_educativo": "SECUNDARIO_COMPLETO",
            "personas_a_cargo": 3.0,
            "capacidad_pago": 0.104167,
            "ratio_endeudamiento": 0.09434,
            "operaciones_mensuales": 3.5,
            "gasto_transaccion_promedio": 27.238095,
            "presion_financiera": 7.619167,
            "antiguedad_relativa": 0.238095,
        }

class PredictionResponse(BaseModel):
    prediction: str
    probability: Dict[str, float]
    class_labels: Dict[str, str]
    model_info: Dict[str, str]


# Cargar el modelo entrenado
MODEL_PATH = "models/prod_model.pkl"

try:
    model = joblib.load(MODEL_PATH)
    print("Modelo cargado exitosamente.")
except FileNotFoundError:
    print(f"Error: No se encontró el modelo en la ruta {MODEL_PATH}. Asegúrate de que el modelo esté en la ruta designada.")
    model = None
except Exception as e:
    print(f"Error al cargar el modelo: {e}")
    model = None


@app.get("/")
def read_root():
    return {
        "message": "Bienvenido a la API de Predicción de Mora en Créditos",
        "endpoints": {
            "/predict": "POST - Realiza una predicción de mora en créditos",
            "/docs": "GET - Documentación interactiva de la API",
            "/health": "GET - Verificar estado del API"   
        }
    }

@app.get("/health")
def health_check():
    if model is not None:
        return {"status": "ok", "message": "La API esta online y funcionando correctamente."}
    else:
        return {"status": "error", "message": "El modelo no esta cargado. Verifica el estado del modelo."}

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="El modelo no esta disponible. Intenta nuevamente mas tarde")
    
    try:
        # Convertir la solicitud a un dataframe
        input_data = pd.DataFrame([request.dict()])
        
        # Realizar la prediccion
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0]
        
        # Mapear las etiquetas de clase a descripciones legibles
        class_labels = model.named_steps['model'].classes_
        probability_dict = {str(class_labels[i]): float(probability[i]) for i in range(len(class_labels))}
        model_info = {
            "model_version": "1.0.0",
            "model_type": "HistGradientBoostingClassifier",
        }

        return PredictionResponse(
        prediction=str(prediction),
        probability=probability_dict,
        class_labels={
            "0": "No entra en mora (N)",
            "1": "Entra en mora (Y)"
        },
        model_info=model_info
    )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al realizar la predicción: {e}")


