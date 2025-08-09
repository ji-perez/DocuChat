#!/bin/bash

echo "🚀 Iniciando DocuChat Backend..."

# Verificar si estamos en el directorio correcto
if [ ! -f "backend/main.py" ]; then
    echo "❌ Error: No se encontró el archivo backend/main.py"
    echo "Asegúrate de ejecutar este script desde el directorio raíz del proyecto"
    exit 1
fi

# Verificar si existe el archivo .env
if [ ! -f ".env" ]; then
    echo "⚠️  Advertencia: No se encontró el archivo .env"
    echo "Copia env_template.txt a .env y configura tu API key de OpenAI"
    echo "cp env_template.txt .env"
    echo ""
    echo "Luego edita .env y agrega tu OPENAI_API_KEY"
    exit 1
fi

# Navegar al directorio backend
cd backend

# Verificar si el entorno de Anaconda existe
if ! conda env list | grep -q "docuchat-backend"; then
    echo "❌ Error: El entorno 'docuchat-backend' no existe"
    echo "Ejecuta primero: ./setup_environments.sh"
    exit 1
fi

echo "🔧 Activando entorno virtual de Anaconda..."
conda activate docuchat-backend

echo "🌐 Iniciando servidor backend en http://localhost:8000"
echo "📚 Documentación de la API: http://localhost:8000/docs"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""

# Iniciar el servidor
uvicorn main:app --reload --host 0.0.0.0 --port 8000
