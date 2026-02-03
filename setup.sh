#!/bin/bash

echo "🌸 Configurando proyecto de clasificación Iris..."

# Crear entorno virtual
echo "Creando entorno virtual..."
python3 -m venv venv

# Activar entorno virtual
echo "Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Entrenar el modelo
echo "Entrenando modelo de Iris..."
python train_model.py

echo "✅ Configuración completada!"
echo ""
echo "Para ejecutar la API:"
echo "1. source venv/bin/activate"
echo "2. python main.py"
echo ""
echo "O usar uvicorn directamente:"
echo "uvicorn main:app --host 0.0.0.0 --port 8000 --reload"