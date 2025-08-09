import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
from typing import Optional

# Cargar variables de entorno
load_dotenv()

# Configuración de la página
st.set_page_config(
    page_title="DocuChat - Sistema de Preguntas y Respuestas",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuración del backend
BACKEND_URL = f"http://{os.getenv('BACKEND_HOST', 'localhost')}:{os.getenv('BACKEND_PORT', '8000')}"

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left-color: #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left-color: #9c27b0;
    }
    .status-success {
        color: #4caf50;
        font-weight: bold;
    }
    .status-error {
        color: #f44336;
        font-weight: bold;
    }
    .status-info {
        color: #2196f3;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def check_backend_status() -> bool:
    """Verificar si el backend está funcionando"""
    try:
        response = requests.get(f"{BACKEND_URL}/", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_system_status():
    """Obtener el estado actual del sistema"""
    try:
        response = requests.get(f"{BACKEND_URL}/status", timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def upload_document(file):
    """Subir y procesar un documento"""
    try:
        files = {"file": (file.name, file.getvalue(), file.type)}
        response = requests.post(f"{BACKEND_URL}/process-document", files=files, timeout=30)
        
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, response.json().get("detail", "Error desconocido")
    except Exception as e:
        return None, str(e)

def ask_question(question: str):
    """Hacer una pregunta al sistema"""
    try:
        data = {"question": question}
        response = requests.post(f"{BACKEND_URL}/ask", json=data, timeout=30)
        
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, response.json().get("detail", "Error desconocido")
    except Exception as e:
        return None, str(e)

def clear_document():
    """Limpiar el documento actual"""
    try:
        response = requests.delete(f"{BACKEND_URL}/clear-document", timeout=10)
        if response.status_code == 200:
            return True, None
        else:
            return False, response.json().get("detail", "Error desconocido")
    except Exception as e:
        return False, str(e)

# Inicializar el historial de chat en session_state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Header principal
st.markdown('<h1 class="main-header">💬 DocuChat</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Sistema de Preguntas y Respuestas sobre Documentos Propios</p>', unsafe_allow_html=True)

# Sidebar para configuración y estado
with st.sidebar:
    st.header("🔧 Configuración")
    
    # Verificar estado del backend
    backend_status = check_backend_status()
    if backend_status:
        st.success("✅ Backend conectado")
    else:
        st.error("❌ Backend no disponible")
        st.info("Asegúrate de que el backend esté ejecutándose en:")
        st.code(f"{BACKEND_URL}")
    
    st.divider()
    
    # Estado del sistema
    st.header("📊 Estado del Sistema")
    if backend_status:
        status = get_system_status()
        if status:
            if status.get("document_loaded"):
                st.success("📄 Documento cargado")
                st.info(f"**Archivo:** {status.get('document_name')}")
                st.info(f"**Fragmentos:** {status.get('chunks_count')}")
                
                # Botón para limpiar documento
                if st.button("🗑️ Limpiar Documento", type="secondary"):
                    success, error = clear_document()
                    if success:
                        st.success("Documento limpiado exitosamente")
                        st.session_state.chat_history = []
                        st.rerun()
                    else:
                        st.error(f"Error: {error}")
            else:
                st.warning("📄 Sin documento cargado")
        else:
            st.error("❌ Error obteniendo estado")
    else:
        st.warning("⚠️ No se puede verificar el estado")

# Contenido principal
if not backend_status:
    st.error("🚫 **El backend no está disponible**")
    st.info("""
    Para usar DocuChat, necesitas iniciar el backend primero:
    
    1. Abre una terminal
    2. Navega al directorio `backend/`
    3. Ejecuta: `uvicorn main:app --reload`
    4. Asegúrate de tener configurada tu API key de OpenAI en el archivo `.env`
    """)
    
    st.code("""
    # En el directorio backend/
    pip install -r requirements.txt
    uvicorn main:app --reload
    """)
    
else:
    # Sección de carga de documentos
    st.header("📁 Cargar Documento")
    
    uploaded_file = st.file_uploader(
        "Selecciona un archivo PDF o TXT",
        type=['pdf', 'txt'],
        help="Solo se permiten archivos PDF (.pdf) y texto (.txt)"
    )
    
    if uploaded_file is not None:
        # Mostrar información del archivo
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"**Nombre:** {uploaded_file.name}")
        with col2:
            st.info(f"**Tamaño:** {uploaded_file.size} bytes")
        with col3:
            st.info(f"**Tipo:** {uploaded_file.type}")
        
        # Botón para procesar
        if st.button("🔄 Procesar Documento", type="primary"):
            with st.spinner("Procesando documento..."):
                result, error = upload_document(uploaded_file)
                
                if result:
                    st.success(f"✅ {result['message']}")
                    st.session_state.chat_history = []  # Limpiar historial
                    st.rerun()
                else:
                    st.error(f"❌ Error: {error}")
    
    st.divider()
    
    # Sección de chat
    st.header("💭 Chat con el Documento")
    
    # Verificar si hay un documento cargado
    status = get_system_status()
    if not status or not status.get("document_loaded"):
        st.warning("⚠️ **No hay ningún documento cargado**")
        st.info("Sube un documento arriba para comenzar a hacer preguntas.")
    else:
        # Mostrar historial de chat
        if st.session_state.chat_history:
            st.subheader("📝 Historial de Conversación")
            for i, (role, message, sources) in enumerate(st.session_state.chat_history):
                if role == "user":
                    st.markdown(f'<div class="chat-message user-message">', unsafe_allow_html=True)
                    st.markdown(f"**Tú:** {message}")
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-message assistant-message">', unsafe_allow_html=True)
                    st.markdown(f"**DocuChat:** {message}")
                    
                    # Mostrar fuentes si están disponibles
                    if sources:
                        with st.expander("📚 Ver fuentes utilizadas"):
                            for j, source in enumerate(sources, 1):
                                st.markdown(f"**Fuente {j}:** {source}")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
        
        # Input para nueva pregunta
        st.subheader("❓ Haz tu pregunta")
        question = st.text_area(
            "Escribe tu pregunta sobre el documento:",
            placeholder="Ej: ¿Cuál es el tema principal del documento?",
            height=100
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            ask_button = st.button("🚀 Enviar Pregunta", type="primary", disabled=not question.strip())
        
        with col2:
            if st.button("🗑️ Limpiar Chat", type="secondary"):
                st.session_state.chat_history = []
                st.rerun()
        
        # Procesar pregunta
        if ask_button and question.strip():
            with st.spinner("🤔 Pensando..."):
                result, error = ask_question(question.strip())
                
                if result:
                    # Agregar al historial
                    st.session_state.chat_history.append(("user", question.strip(), []))
                    st.session_state.chat_history.append(("assistant", result["answer"], result.get("sources", [])))
                    
                    st.success("✅ Respuesta generada")
                    st.rerun()
                else:
                    st.error(f"❌ Error: {error}")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.8rem;">
    <p>DocuChat v1.0 - Sistema de Preguntas y Respuestas sobre Documentos Propios</p>
    <p>Desarrollado con LangChain, FastAPI, Streamlit y OpenAI</p>
</div>
""", unsafe_allow_html=True)
