# 📋 Guía de Instalación - DocuChat

## Requisitos Previos

- **Python 3.9+** instalado en tu sistema
- **Cuenta de OpenAI** con API key válida
- **Git** (opcional, para clonar el repositorio)

## 🚀 Instalación Rápida

### 1. Configurar Variables de Entorno

```bash
# Copiar el template de variables de entorno
cp env_template.txt .env

# Editar el archivo .env y agregar tu API key de OpenAI
nano .env  # o usar tu editor preferido
```

En el archivo `.env`, reemplaza `your_openai_api_key_here` con tu API key real de OpenAI:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 2. Instalar Dependencias

#### Opción A: Configuración automática con Anaconda (Recomendado)

```bash
# Configurar entornos virtuales y instalar dependencias
./setup_environments.sh
```

#### Opción B: Instalación manual con Anaconda

```bash
# Crear entornos virtuales
conda create -n docuchat-backend python=3.9 -y
conda create -n docuchat-frontend python=3.9 -y

# Instalar dependencias del backend
conda activate docuchat-backend
cd backend
pip install -r requirements.txt

# Instalar dependencias del frontend
conda activate docuchat-frontend
cd frontend
pip install -r requirements.txt
```

## 🏃‍♂️ Ejecutar el Proyecto

### 1. Iniciar el Backend

```bash
# Opción A: Usando el script
./start_backend.sh

# Opción B: Manualmente
conda activate docuchat-backend
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

El backend estará disponible en: http://localhost:8000
Documentación de la API: http://localhost:8000/docs

### 2. Iniciar el Frontend

```bash
# Opción A: Usando el script
./start_frontend.sh

# Opción B: Manualmente
conda activate docuchat-frontend
cd frontend
streamlit run app.py --server.port 8501
```

El frontend estará disponible en: http://localhost:8501

## 🔧 Configuración Avanzada

### Variables de Entorno Disponibles

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `OPENAI_API_KEY` | Tu API key de OpenAI | Requerido |
| `BACKEND_HOST` | Host del backend | localhost |
| `BACKEND_PORT` | Puerto del backend | 8000 |
| `FRONTEND_PORT` | Puerto del frontend | 8501 |
| `CHROMA_DB_PATH` | Ruta de la base de datos ChromaDB | ./chroma_db |

### Modelos de OpenAI Utilizados

- **Embeddings**: `text-embedding-3-small`
- **LLM**: `gpt-4o-mini`

Para cambiar estos modelos, edita el archivo `backend/main.py`.

## 🐛 Solución de Problemas

### Error: "OPENAI_API_KEY no está configurada"

1. Verifica que el archivo `.env` existe en el directorio raíz
2. Asegúrate de que `OPENAI_API_KEY` esté configurada correctamente
3. Reinicia el backend después de cambiar las variables de entorno

### Error: "Backend no disponible"

1. Verifica que el backend esté ejecutándose en http://localhost:8000
2. Revisa los logs del backend para errores
3. Asegúrate de que el puerto 8000 no esté ocupado por otra aplicación

### Error: "No se pudo generar una respuesta"

1. Verifica que tu API key de OpenAI sea válida
2. Revisa tu saldo de créditos en OpenAI
3. Asegúrate de que el documento se haya procesado correctamente

### Error de dependencias

```bash
# Actualizar pip
pip install --upgrade pip

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

## 📁 Estructura del Proyecto

```
DocuChat/
├── backend/                 # Servidor FastAPI
│   ├── main.py             # Lógica principal del backend
│   ├── requirements.txt    # Dependencias del backend
│   └── __init__.py
├── frontend/               # Aplicación Streamlit
│   ├── app.py             # Interfaz de usuario
│   ├── requirements.txt   # Dependencias del frontend
│   └── __init__.py
├── .env                   # Variables de entorno (crear desde env_template.txt)
├── env_template.txt       # Template de variables de entorno
├── start_backend.sh       # Script para iniciar backend
├── start_frontend.sh      # Script para iniciar frontend
├── .gitignore            # Archivos a ignorar por Git
├── README.md             # Documentación principal
└── INSTALLATION.md       # Esta guía
```

## 🔒 Seguridad

- **Nunca** subas tu archivo `.env` a un repositorio público
- Mantén tu API key de OpenAI segura
- En producción, usa variables de entorno del sistema en lugar de archivos `.env`

## 📞 Soporte

Si encuentras problemas:

1. Revisa los logs de error en la consola
2. Verifica que todas las dependencias estén instaladas correctamente
3. Asegúrate de que tu API key de OpenAI sea válida
4. Consulta la documentación de la API en http://localhost:8000/docs
