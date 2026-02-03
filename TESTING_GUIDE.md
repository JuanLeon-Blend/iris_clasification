# 🧪 Guía Completa de Pruebas - API de Clasificación Iris

Esta guía te ayudará a probar todos los endpoints de la API de clasificación de Iris paso a paso.

## 📋 Prerrequisitos

1. **API ejecutándose**:
   ```bash
   source venv/bin/activate
   python main.py
   ```
   
2. **Verificar que la API esté activa**:
   - URL local: `http://localhost:8000`
   - En Cloud9: `http://tu-instancia-cloud9.amazonaws.com:8000`

## 🔧 Métodos de Prueba

### Opción 1: Usando cURL (Terminal)
### Opción 2: Usando el script de prueba
### Opción 3: Usando navegador web
### Opción 4: Usando Postman/Insomnia

---

## 🚀 Pruebas de Endpoints

### 1. **GET /** - Información General

**Descripción**: Obtiene información básica de la API

#### Con cURL:
```bash
curl -X GET "http://localhost:8000/"
```

#### Con navegador:
```
http://localhost:8000/
```

#### Respuesta esperada:
```json
{
  "message": "API de Clasificación de Iris",
  "status": "activo",
  "modelo_cargado": true,
  "endpoints": {
    "prediccion": "/predict",
    "salud": "/health",
    "info": "/info"
  }
}
```

---

### 2. **GET /health** - Estado de Salud

**Descripción**: Verifica si la API y el modelo están funcionando correctamente

#### Con cURL:
```bash
curl -X GET "http://localhost:8000/health"
```

#### Con navegador:
```
http://localhost:8000/health
```

#### Respuesta esperada:
```json
{
  "status": "healthy",
  "modelo_disponible": true
}
```

---

### 3. **GET /info** - Información del Modelo

**Descripción**: Obtiene información sobre las características del modelo y las clases

#### Con cURL:
```bash
curl -X GET "http://localhost:8000/info"
```

#### Con navegador:
```
http://localhost:8000/info
```

#### Respuesta esperada:
```json
{
  "caracteristicas": [
    "sepal length (cm)",
    "sepal width (cm)",
    "petal length (cm)",
    "petal width (cm)"
  ],
  "clases": ["setosa", "versicolor", "virginica"],
  "descripcion": {
    "sepal_length": "Longitud del sépalo (cm)",
    "sepal_width": "Ancho del sépalo (cm)",
    "petal_length": "Longitud del pétalo (cm)",
    "petal_width": "Ancho del pétalo (cm)"
  }
}
```

---

### 4. **POST /predict** - Predicción Individual

**Descripción**: Clasifica una sola muestra de flor Iris

#### Con cURL:

**Ejemplo 1 - Iris Setosa:**
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

**Ejemplo 2 - Iris Versicolor:**
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "sepal_length": 7.0,
       "sepal_width": 3.2,
       "petal_length": 4.7,
       "petal_width": 1.4
     }'
```

**Ejemplo 3 - Iris Virginica:**
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "sepal_length": 6.3,
       "sepal_width": 3.3,
       "petal_length": 6.0,
       "petal_width": 2.5
     }'
```

#### Respuesta esperada (Setosa):
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

---

### 5. **POST /predict/batch** - Predicción por Lotes

**Descripción**: Clasifica múltiples muestras de flores Iris en una sola petición

#### Con cURL:
```bash
curl -X POST "http://localhost:8000/predict/batch" \
     -H "Content-Type: application/json" \
     -d '[
       {
         "sepal_length": 5.1,
         "sepal_width": 3.5,
         "petal_length": 1.4,
         "petal_width": 0.2
       },
       {
         "sepal_length": 7.0,
         "sepal_width": 3.2,
         "petal_length": 4.7,
         "petal_width": 1.4
       },
       {
         "sepal_length": 6.3,
         "sepal_width": 3.3,
         "petal_length": 6.0,
         "petal_width": 2.5
       }
     ]'
```

#### Respuesta esperada:
```json
{
  "predictions": [
    {
      "prediction": "setosa",
      "probability": 1.0,
      "all_probabilities": {
        "setosa": 1.0,
        "versicolor": 0.0,
        "virginica": 0.0
      }
    },
    {
      "prediction": "versicolor",
      "probability": 0.9,
      "all_probabilities": {
        "setosa": 0.0,
        "versicolor": 0.9,
        "virginica": 0.1
      }
    },
    {
      "prediction": "virginica",
      "probability": 1.0,
      "all_probabilities": {
        "setosa": 0.0,
        "versicolor": 0.0,
        "virginica": 1.0
      }
    }
  ]
}
```

---

## 🤖 Usando el Script de Prueba Automático

Ejecuta todas las pruebas de una vez:

```bash
# Asegúrate de que la API esté ejecutándose
python test_api.py
```

---

## 🌐 Documentación Interactiva

FastAPI genera automáticamente documentación interactiva:

### Swagger UI:
```
http://localhost:8000/docs
```

### ReDoc:
```
http://localhost:8000/redoc
```

En estas interfaces puedes:
- Ver todos los endpoints
- Probar las APIs directamente
- Ver esquemas de datos
- Descargar especificaciones OpenAPI

---

## 📊 Casos de Prueba Recomendados

### Casos Válidos:

**Setosa típica:**
```json
{
  "sepal_length": 5.0,
  "sepal_width": 3.6,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

**Versicolor típica:**
```json
{
  "sepal_length": 6.0,
  "sepal_width": 2.7,
  "petal_length": 4.0,
  "petal_width": 1.3
}
```

**Virginica típica:**
```json
{
  "sepal_length": 6.5,
  "sepal_width": 3.0,
  "petal_length": 5.5,
  "petal_width": 2.0
}
```

### Casos Límite:

**Valores muy pequeños:**
```json
{
  "sepal_length": 0.1,
  "sepal_width": 0.1,
  "petal_length": 0.1,
  "petal_width": 0.1
}
```

**Valores muy grandes:**
```json
{
  "sepal_length": 10.0,
  "sepal_width": 10.0,
  "petal_length": 10.0,
  "petal_width": 10.0
}
```

### Casos de Error:

**Datos faltantes:**
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "sepal_length": 5.1,
       "sepal_width": 3.5
     }'
```

**Tipos de datos incorrectos:**
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "sepal_length": "texto",
       "sepal_width": 3.5,
       "petal_length": 1.4,
       "petal_width": 0.2
     }'
```

---

## 🔍 Verificación de Resultados

### ✅ Indicadores de Éxito:

1. **Status Code 200** para todas las peticiones válidas
2. **Modelo cargado** = `true` en `/health`
3. **Predicciones coherentes** con las características de entrada
4. **Probabilidades suman 1.0** en las respuestas

### ❌ Posibles Errores:

- **Status 503**: Modelo no disponible (ejecutar `train_model.py`)
- **Status 422**: Datos de entrada inválidos
- **Status 400**: Error en el procesamiento
- **Connection refused**: API no está ejecutándose

---

## 🛠️ Solución de Problemas

### Problema: "Modelo no disponible"
```bash
# Entrenar el modelo
python train_model.py

# Reiniciar la API
python main.py
```

### Problema: "Connection refused"
```bash
# Verificar que la API esté ejecutándose
ps aux | grep python

# Iniciar la API
python main.py
```

### Problema: Puerto ocupado
```bash
# Usar otro puerto
uvicorn main:app --host 0.0.0.0 --port 8001

# O matar el proceso que usa el puerto 8000
lsof -ti:8000 | xargs kill -9
```

---

## 📈 Métricas de Rendimiento

Para medir el rendimiento de la API:

```bash
# Instalar herramientas de benchmark
pip install httpx

# Crear script de benchmark
python -c "
import httpx
import time
import asyncio

async def benchmark():
    async with httpx.AsyncClient() as client:
        start = time.time()
        tasks = []
        for i in range(100):
            task = client.post('http://localhost:8000/predict', 
                             json={'sepal_length': 5.1, 'sepal_width': 3.5, 
                                   'petal_length': 1.4, 'petal_width': 0.2})
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks)
        end = time.time()
        
        print(f'100 requests in {end-start:.2f} seconds')
        print(f'Average: {(end-start)/100*1000:.2f}ms per request')

asyncio.run(benchmark())
"
```

---

## 🎯 Checklist de Pruebas

- [ ] GET / - Información general
- [ ] GET /health - Estado de salud
- [ ] GET /info - Información del modelo
- [ ] POST /predict - Predicción Setosa
- [ ] POST /predict - Predicción Versicolor  
- [ ] POST /predict - Predicción Virginica
- [ ] POST /predict/batch - Predicción por lotes
- [ ] Casos de error (datos faltantes)
- [ ] Casos de error (tipos incorrectos)
- [ ] Documentación Swagger (/docs)
- [ ] Documentación ReDoc (/redoc)

¡Con esta guía puedes probar completamente tu API de clasificación de Iris! 🌸