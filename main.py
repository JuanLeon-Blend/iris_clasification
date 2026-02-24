from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
from typing import List
import mlflow
import mlflow.sklearn

# ============================================
# Configuración MLflow
# ============================================
MLFLOW_TRACKING_URI = "http://ec2-100-31-158-242.compute-1.amazonaws.com:5000"
RUN_ID = "cf7b240498d24f1ebf2402e61ea1f4fe"
TARGET_NAMES = ["setosa", "versicolor", "virginica"]

# Crear la aplicación FastAPI
app = FastAPI(
    title="Titanic Classification API - MLflow",
    description="API que sirve el mejor modelo desde MLflow (random-forest-Juan)",
    version="2.0.0"
)

# Modelo de datos para la predicción (Titanic - features de Juan)
class TitanicFeatures(BaseModel):
    Pclass: int
    Sex: int          # 0=female, 1=male
    Age: float
    Fare: float
    Title: int        # 0=Master, 1=Miss, 2=Mr, 3=Mrs, 4=Rare

class PredictionResponse(BaseModel):
    prediction: int
    survived: str
    probability: float
    all_probabilities: dict

# Variable global para el modelo
model = None
run_info = None

@app.on_event("startup")
async def load_model():
    global model, run_info
    try:
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        
        # Cargar modelo desde MLflow usando el run_id
        model_uri = f"runs:/{RUN_ID}/model"
        model = mlflow.sklearn.load_model(model_uri)
        
        # Obtener info del run
        client = mlflow.tracking.MlflowClient()
        run = client.get_run(RUN_ID)
        run_info = {
            "run_id": RUN_ID,
            "run_name": run.data.tags.get("mlflow.runName", "unknown"),
            "author": run.data.tags.get("author", "unknown"),
            "accuracy": run.data.metrics.get("test_accuracy", 0),
            "feature_strategy": run.data.tags.get("feature_strategy", "unknown"),
        }
        
        print(f"Modelo cargado desde MLflow: {run_info['run_name']}")
        print(f"Run ID: {RUN_ID}")
        print(f"Accuracy: {run_info['accuracy']}")
    except Exception as e:
        print(f"Error cargando modelo desde MLflow: {e}")

@app.get("/")
async def root():
    return {
        "message": "API Titanic - Modelo servido desde MLflow",
        "status": "activo",
        "modelo_cargado": model is not None,
        "mlflow_server": MLFLOW_TRACKING_URI,
        "run_id": RUN_ID,
        "run_info": run_info,
        "endpoints": {
            "prediccion": "/predict",
            "salud": "/health",
            "info": "/info",
            "batch": "/predict/batch"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "modelo_disponible": model is not None,
        "mlflow_connected": model is not None
    }

@app.get("/info")
async def model_info_endpoint():
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible")
    
    return {
        "run_id": RUN_ID,
        "run_info": run_info,
        "mlflow_uri": MLFLOW_TRACKING_URI,
        "features": ["Pclass", "Sex", "Age", "Fare", "Title"],
        "target": "Survived (0=No, 1=Sí)",
        "descripcion_features": {
            "Pclass": "Clase del pasajero (1, 2, 3)",
            "Sex": "Sexo (0=female, 1=male)",
            "Age": "Edad en años",
            "Fare": "Tarifa pagada",
            "Title": "Título (0=Master, 1=Miss, 2=Mr, 3=Mrs, 4=Rare)"
        }
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(features: TitanicFeatures):
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible")
    
    try:
        feature_array = np.array([[
            features.Pclass,
            features.Sex,
            features.Age,
            features.Fare,
            features.Title
        ]])
        
        prediction = int(model.predict(feature_array)[0])
        probabilities = model.predict_proba(feature_array)[0]
        
        return PredictionResponse(
            prediction=prediction,
            survived="Sí" if prediction == 1 else "No",
            probability=float(probabilities[prediction]),
            all_probabilities={
                "No sobrevivió (0)": float(probabilities[0]),
                "Sobrevivió (1)": float(probabilities[1])
            }
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en predicción: {str(e)}")

@app.post("/predict/batch")
async def predict_batch(features_list: List[TitanicFeatures]):
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible")
    
    try:
        results = []
        for features in features_list:
            feature_array = np.array([[
                features.Pclass,
                features.Sex,
                features.Age,
                features.Fare,
                features.Title
            ]])
            
            prediction = int(model.predict(feature_array)[0])
            probabilities = model.predict_proba(feature_array)[0]
            
            results.append({
                "prediction": prediction,
                "survived": "Sí" if prediction == 1 else "No",
                "probability": float(probabilities[prediction]),
                "all_probabilities": {
                    "No sobrevivió (0)": float(probabilities[0]),
                    "Sobrevivió (1)": float(probabilities[1])
                }
            })
        
        return {"predictions": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en predicción: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)