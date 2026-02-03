from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import os
from typing import List

# Crear la aplicación FastAPI
app = FastAPI(
    title="Iris Classification API",
    description="API para clasificar flores Iris usando Machine Learning",
    version="1.0.0"
)

# Modelo de datos para la predicción
class IrisFeatures(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

class PredictionResponse(BaseModel):
    prediction: str
    probability: float
    all_probabilities: dict

# Cargar el modelo al iniciar la aplicación
model = None
model_info = None

@app.on_event("startup")
async def load_model():
    global model, model_info
    try:
        if os.path.exists('models/iris_model.pkl'):
            model = joblib.load('models/iris_model.pkl')
            model_info = joblib.load('models/model_info.pkl')
            print("Modelo cargado exitosamente")
        else:
            print("Modelo no encontrado. Ejecuta train_model.py primero.")
    except Exception as e:
        print(f"Error cargando el modelo: {e}")

@app.get("/")
async def root():
    """Endpoint raíz con información de la API"""
    return {
        "message": "API de Clasificación de Iris",
        "status": "activo",
        "modelo_cargado": model is not None,
        "endpoints": {
            "prediccion": "/predict",
            "salud": "/health",
            "info": "/info"
        }
    }

@app.get("/health")
async def health_check():
    """Verificar el estado de la API"""
    return {
        "status": "healthy",
        "modelo_disponible": model is not None
    }

@app.get("/info")
async def model_info_endpoint():
    """Información sobre el modelo y características"""
    if model_info is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible")
    
    return {
        "caracteristicas": model_info['feature_names'],
        "clases": model_info['target_names'],
        "descripcion": {
            "sepal_length": "Longitud del sépalo (cm)",
            "sepal_width": "Ancho del sépalo (cm)", 
            "petal_length": "Longitud del pétalo (cm)",
            "petal_width": "Ancho del pétalo (cm)"
        }
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict_iris(features: IrisFeatures):
    """Predecir la especie de Iris basada en las características"""
    
    if model is None or model_info is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible")
    
    try:
        # Convertir características a array numpy
        feature_array = np.array([[
            features.sepal_length,
            features.sepal_width,
            features.petal_length,
            features.petal_width
        ]])
        
        # Hacer predicción
        prediction = model.predict(feature_array)[0]
        probabilities = model.predict_proba(feature_array)[0]
        
        # Obtener nombre de la clase predicha
        predicted_class = model_info['target_names'][prediction]
        
        # Crear diccionario de probabilidades
        prob_dict = {
            model_info['target_names'][i]: float(prob) 
            for i, prob in enumerate(probabilities)
        }
        
        return PredictionResponse(
            prediction=predicted_class,
            probability=float(probabilities[prediction]),
            all_probabilities=prob_dict
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en la predicción: {str(e)}")

@app.post("/predict/batch")
async def predict_batch(features_list: List[IrisFeatures]):
    """Predecir múltiples muestras de Iris"""
    
    if model is None or model_info is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible")
    
    try:
        results = []
        for features in features_list:
            feature_array = np.array([[
                features.sepal_length,
                features.sepal_width,
                features.petal_length,
                features.petal_width
            ]])
            
            prediction = model.predict(feature_array)[0]
            probabilities = model.predict_proba(feature_array)[0]
            predicted_class = model_info['target_names'][prediction]
            
            prob_dict = {
                model_info['target_names'][i]: float(prob) 
                for i, prob in enumerate(probabilities)
            }
            
            results.append({
                "prediction": predicted_class,
                "probability": float(probabilities[prediction]),
                "all_probabilities": prob_dict
            })
        
        return {"predictions": results}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en la predicción: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)