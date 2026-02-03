import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

def train_iris_model():
    """Entrena el modelo de clasificación de Iris"""
    
    # Cargar dataset de Iris
    iris = load_iris()
    X, y = iris.data, iris.target
    
    # Dividir en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Crear y entrenar el modelo
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluar el modelo
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"Precisión del modelo: {accuracy:.4f}")
    print("\nReporte de clasificación:")
    print(classification_report(y_test, y_pred, target_names=iris.target_names))
    
    # Crear directorio para modelos si no existe
    os.makedirs('models', exist_ok=True)
    
    # Guardar el modelo
    joblib.dump(model, 'models/iris_model.pkl')
    
    # Guardar nombres de características y clases
    model_info = {
        'feature_names': iris.feature_names,
        'target_names': iris.target_names.tolist()
    }
    joblib.dump(model_info, 'models/model_info.pkl')
    
    print("Modelo guardado exitosamente en 'models/iris_model.pkl'")
    return model, model_info

if __name__ == "__main__":
    train_iris_model()