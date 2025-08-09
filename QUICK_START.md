# 🚀 Inicio Rápido - DocuChat

## Flujo de Trabajo Recomendado

### 1. Configuración Inicial (Solo una vez)

```bash
# 1. Configurar variables de entorno
cp env_template.txt .env
# Editar .env y agregar tu OPENAI_API_KEY

# 2. Crear entornos virtuales e instalar dependencias
./setup_environments.sh
```

### 2. Ejecutar el Proyecto

#### Terminal 1 - Backend
```bash
./start_backend.sh
```

#### Terminal 2 - Frontend
```bash
./start_frontend.sh
```

### 3. Usar la Aplicación

1. Abrir http://localhost:8501 en tu navegador
2. Subir un documento PDF o TXT
3. Hacer preguntas sobre el contenido

## 📋 Comandos Manuales (Alternativa)

Si prefieres hacerlo manualmente:

### Configurar Entornos
```bash
# Crear entornos
conda create -n docuchat-backend python=3.9 -y
conda create -n docuchat-frontend python=3.9 -y

# Instalar dependencias backend
conda activate docuchat-backend
cd backend
pip install -r requirements.txt

# Instalar dependencias frontend
conda activate docuchat-frontend
cd frontend
pip install -r requirements.txt
```

### Ejecutar Servicios
```bash
# Terminal 1 - Backend
conda activate docuchat-backend
cd backend
uvicorn main:app --reload

# Terminal 2 - Frontend
conda activate docuchat-frontend
cd frontend
streamlit run app.py
```

## 🔧 Gestión de Entornos

### Ver entornos disponibles
```bash
conda env list
```

### Activar entorno
```bash
conda activate docuchat-backend    # Para backend
conda activate docuchat-frontend   # Para frontend
```

### Desactivar entorno
```bash
conda deactivate
```

### Eliminar entorno (si necesitas recrearlo)
```bash
conda env remove -n docuchat-backend
conda env remove -n docuchat-frontend
```

## 🌐 URLs Importantes

- **Frontend**: http://localhost:8501
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## ⚠️ Notas Importantes

1. **Siempre activa el entorno virtual** antes de ejecutar los servicios
2. **Mantén ambos servicios ejecutándose** (backend y frontend)
3. **Configura tu API key de OpenAI** en el archivo `.env`
4. **Usa terminales separadas** para backend y frontend
