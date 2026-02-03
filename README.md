# 🌸 API de Clasificación de Iris

API REST desarrollada con FastAPI para clasificar especies de flores Iris usando Machine Learning.

## 🚀 Configuración Rápida

### En AWS Cloud9

```bash
# Clonar el repositorio
git clone <tu-repositorio-url>
cd iris-classification-api

# Ejecutar configuración automática
./setup.sh
```

### Configuración Manual

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Entrenar el modelo
python train_model.py

# Ejecutar la API
python main.py
```

## 🔧 Uso de la API

### Iniciar el servidor

```bash
# Opción 1: Ejecutar directamente
python main.py

# Opción 2: Con uvicorn (recomendado para desarrollo)
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Endpoints Disponibles

- **GET /** - Información general de la API
- **GET /health** - Estado de salud de la API
- **GET /info** - Información del modelo y características
- **POST /predict** - Clasificar una muestra
- **POST /predict/batch** - Clasificar múltiples muestras

### Ejemplo de Predicción

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "sepal_length": 5.1,
       "sepal_width": 3.5,
       "petal_length": 1.4,
       "petal_width": 0.2
     }'
```

Respuesta:
```json
{
  "prediction": "setosa",
  "probability": 1.0,
  "all_probabilities": {
    "setosa": 1.0,
    "versicolor": 0.0,
    "virginica": 0.0
  }
}
```

## 📁 Estructura del Proyecto

```
iris-classification-api/
├── main.py              # API FastAPI
├── train_model.py       # Script de entrenamiento
├── requirements.txt     # Dependencias
├── setup.sh            # Script de configuración
├── README.md           # Documentación
├── models/             # Modelos entrenados
│   ├── iris_model.pkl
│   └── model_info.pkl
└── venv/               # Entorno virtual
```

## 🌐 Despliegue en AWS Cloud9

### Configuración del Entorno

1. **Abrir Cloud9** y crear un nuevo entorno
2. **Clonar el repositorio**:
   ```bash
   git clone <tu-repositorio-url>
   cd iris-classification-api
   ```

3. **Ejecutar configuración**:
   ```bash
   ./setup.sh
   ```

4. **Iniciar la API**:
   ```bash
   source venv/bin/activate
   python main.py
   ```

### Acceso Externo en Cloud9

Para permitir acceso externo en Cloud9:

1. **Configurar Security Group** del entorno Cloud9
2. **Abrir puerto 8000** en las reglas de entrada
3. **Ejecutar con host 0.0.0.0**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

## 📊 Características del Modelo

El modelo utiliza las siguientes características de las flores Iris:

- **sepal_length**: Longitud del sépalo (cm)
- **sepal_width**: Ancho del sépalo (cm)
- **petal_length**: Longitud del pétalo (cm)
- **petal_width**: Ancho del pétalo (cm)

**Clases predichas**:
- setosa
- versicolor
- virginica

## 🔄 Workflow Git

```bash
# Subir cambios
git add .
git commit -m "Actualización del modelo"
git push origin main

# Descargar cambios en Cloud9
git pull origin main
./setup.sh  # Si hay nuevas dependencias
```

## 🛠️ Desarrollo

### Actualizar el Modelo

```bash
# Modificar train_model.py según necesidades
python train_model.py

# Reiniciar la API para cargar el nuevo modelo
```

### Agregar Nuevas Características

1. Modificar `train_model.py` para el nuevo modelo
2. Actualizar `IrisFeatures` en `main.py`
3. Reentrenar y reiniciar la API

## 📝 Notas

- El modelo se entrena automáticamente con el dataset de Iris de scikit-learn
- Los modelos se guardan en la carpeta `models/`
- La API incluye validación de datos con Pydantic
- Configurado para funcionar en Cloud9 con host 0.0.0.0