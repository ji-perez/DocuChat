#!/bin/bash

echo "🎨 Iniciando DocuChat Frontend..."

# Verificar si estamos en el directorio correcto
if [ ! -f "frontend/app.py" ]; then
    echo "❌ Error: No se encontró el archivo frontend/app.py"
    echo "Asegúrate de ejecutar este script desde el directorio raíz del proyecto"
    exit 1
fi

# Navegar al directorio frontend
cd frontend

# Verificar si el entorno de Anaconda existe
if ! conda env list | grep -q "docuchat-frontend"; then
    echo "❌ Error: El entorno 'docuchat-frontend' no existe"
    echo "Ejecuta primero: ./setup_environments.sh"
    exit 1
fi

echo "🔧 Activando entorno virtual de Anaconda..."
conda activate docuchat-frontend

echo "🌐 Iniciando aplicación frontend en http://localhost:8501"
echo ""
echo "Asegúrate de que el backend esté ejecutándose en http://localhost:8000"
echo "Presiona Ctrl+C para detener la aplicación"
echo ""

# Iniciar Streamlit
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
