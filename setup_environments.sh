#!/bin/bash

echo "🔧 Configurando entornos virtuales de Anaconda para DocuChat..."

# Verificar si conda está disponible
if ! command -v conda &> /dev/null; then
    echo "❌ Error: Anaconda no está instalado o no está en el PATH"
    echo "Por favor, instala Anaconda o Miniconda primero"
    exit 1
fi

echo "✅ Anaconda detectado: $(conda --version)"

# Crear entorno virtual para el backend
echo "📦 Creando entorno virtual para el backend..."
if conda env list | grep -q "docuchat-backend"; then
    echo "⚠️  El entorno 'docuchat-backend' ya existe. ¿Deseas recrearlo? (y/N)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        conda env remove -n docuchat-backend -y
        conda create -n docuchat-backend python=3.9 -y
    else
        echo "✅ Usando entorno existente 'docuchat-backend'"
    fi
else
    conda create -n docuchat-backend python=3.9 -y
fi

# Crear entorno virtual para el frontend
echo "📦 Creando entorno virtual para el frontend..."
if conda env list | grep -q "docuchat-frontend"; then
    echo "⚠️  El entorno 'docuchat-frontend' ya existe. ¿Deseas recrearlo? (y/N)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        conda env remove -n docuchat-frontend -y
        conda create -n docuchat-frontend python=3.9 -y
    else
        echo "✅ Usando entorno existente 'docuchat-frontend'"
    fi
else
    conda create -n docuchat-frontend python=3.9 -y
fi

# Instalar dependencias del backend
echo "📥 Instalando dependencias del backend..."
conda activate docuchat-backend
cd backend
pip install -r requirements.txt
cd ..

# Instalar dependencias del frontend
echo "📥 Instalando dependencias del frontend..."
conda activate docuchat-frontend
cd frontend
pip install -r requirements.txt
cd ..

echo ""
echo "✅ ¡Configuración completada!"
echo ""
echo "📋 Para usar el proyecto:"
echo ""
echo "1. Configura tu API key de OpenAI:"
echo "   cp env_template.txt .env"
echo "   # Edita .env y agrega tu OPENAI_API_KEY"
echo ""
echo "2. Inicia el backend:"
echo "   conda activate docuchat-backend"
echo "   cd backend"
echo "   uvicorn main:app --reload"
echo ""
echo "3. En otra terminal, inicia el frontend:"
echo "   conda activate docuchat-frontend"
echo "   cd frontend"
echo "   streamlit run app.py"
echo ""
echo "🌐 Backend: http://localhost:8000"
echo "🎨 Frontend: http://localhost:8501"
