# **Proyecto: Sistema de Preguntas y Respuestas sobre Documentos Propios 💬**

Versión: 1.0  
Fecha: 2025-08-07  
Nombre: DocuChat

## **1\. Descripción del Proyecto**

### **¿De qué trata?**

Este proyecto consiste en el desarrollo de una aplicación web que permite a los usuarios cargar sus propios documentos (como archivos PDF o de texto) y mantener una conversación con ellos. En esencia, se trata de un "chatbot" especializado que utiliza el contenido de un documento específico como su única fuente de conocimiento para responder preguntas.

### **Objetivo Principal**

El objetivo es construir un sistema de **Retrieval-Augmented Generation (RAG)** funcional y desacoplado. Esto permitirá a los usuarios extraer información y obtener respuestas precisas a preguntas complejas sobre sus documentos sin necesidad de leerlos por completo, aprovechando el poder de los Grandes Modelos de Lenguaje (LLMs).

### **Funcionalidades Clave**

* **Carga de Documentos**: La interfaz de usuario permitirá al usuario seleccionar y subir un documento (inicialmente, .pdf y .txt).  
* **Procesamiento de Documentos**: El sistema procesará el documento cargado, lo dividirá en fragmentos manejables y creará representaciones vectoriales (embeddings) de cada fragmento.  
* **Interfaz de Preguntas y Respuestas**: Un área de chat donde el usuario puede escribir una pregunta.  
* **Generación de Respuestas**: El sistema buscará los fragmentos más relevantes del documento para responder a la pregunta del usuario y utilizará un LLM para generar una respuesta coherente y contextualizada.

---

## **2\. Tecnologías Utilizadas**

El proyecto se dividirá en dos componentes principales: un backend para la lógica de IA y un frontend para la interacción con el usuario.

### **Backend (API de Lógica)**

* **Python 3.9+**: El lenguaje de programación base para todo el desarrollo.  
* **LangChain**: El framework principal para orquestar todos los componentes de la lógica de IA. Se usará para cargar documentos (DocumentLoaders), dividirlos (TextSplitters), interactuar con el modelo de embeddings y el LLM, y construir la cadena de recuperación (RetrievalQA).  
* **FastAPI**: Un framework web de alto rendimiento para construir el API REST. Será el encargado de exponer la lógica de LangChain a través de endpoints HTTP, gestionando las peticiones del frontend.  
* **OpenAI**: Se utilizará su API para acceder a dos servicios clave:  
  * **Modelos de Embeddings** (text-embedding-3-small): Para convertir los fragmentos de texto en vectores numéricos.  
  * **Modelo de Lenguaje (LLM)** (gpt-3.5-turbo o gpt-4o): El cerebro que generará las respuestas en lenguaje natural.  
* **ChromaDB**: Una base de datos vectorial de código abierto. Almacenará los vectores de los fragmentos de texto y permitirá realizar búsquedas de similitud semántica de manera eficiente.  
* **Uvicorn**: Un servidor ASGI (Asynchronous Server Gateway Interface) que se usará para ejecutar la aplicación FastAPI.
* **Anaconda**: La generación y gestión de los ambientes virtuales se hara con Anaconda.

### **Frontend (Interfaz de Usuario)**

* **Streamlit**: Un framework de Python que permite crear aplicaciones web interactivas con muy poco código. Ideal para construir la interfaz de usuario de forma rápida y sencilla.  
* **Requests**: Una librería de Python estándar para realizar peticiones HTTP. Streamlit la usará para comunicarse con el backend de FastAPI.

---

## **3\. Arquitectura del Sistema**

Adoptaremos una **arquitectura cliente-servidor** desacoplada, lo que nos brinda escalabilidad y modularidad.

[Imagen de a client-server architecture diagram](https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcRfljlOrd8cDb5ShcecLetBMKDNiDVc21MOiBfDtfGEI1sowEuXk69puLw05wrWSphYjcR1G7qwP50eQq9933sh53SmatFWyyqRvuhQjJWFG45Ee4A)

* **Backend (Servidor)**: Es una aplicación **FastAPI** que actúa como el motor de la inteligencia artificial. Su única responsabilidad es recibir una pregunta, procesarla a través del flujo de LangChain y devolver una respuesta. No sabe nada sobre cómo se ve la interfaz de usuario. Contiene el LLM, la base de datos de vectores y toda la lógica de RAG.  
* **Frontend (Cliente)**: Es una aplicación **Streamlit** que se ejecuta en el navegador del usuario (o en un servidor web). Su responsabilidad es renderizar la interfaz gráfica, capturar la entrada del usuario (la pregunta) y mostrar la respuesta. No realiza ningún procesamiento de IA; simplemente se comunica con el backend a través de su API.

### **Flujo de Comunicación:**

1. El usuario escribe una pregunta en la interfaz de Streamlit y pulsa "Enviar".  
2. El script de Streamlit empaqueta la pregunta en una carga útil JSON.  
3. Streamlit envía una petición POST al endpoint /ask del backend de FastAPI.  
4. FastAPI recibe la petición, extrae la pregunta y la pasa a la cadena RetrievalQA de LangChain.  
5. LangChain:  
   a. Convierte la pregunta del usuario en un vector.  
   b. Busca en ChromaDB los fragmentos de texto cuyos vectores son más similares al vector de la pregunta.  
   c. Envía los fragmentos recuperados y la pregunta original al LLM de OpenAI.  
6. El LLM genera una respuesta basada en el contexto proporcionado.  
7. FastAPI recibe la respuesta del LLM y la devuelve al frontend en formato JSON.  
8. Streamlit recibe la respuesta, la procesa y la muestra en la interfaz para que el usuario la lea.

---

## **4\. Plan de Desarrollo (Paso a Paso)**

### **Paso 1: Configuración del Entorno**

1. **Crear un directorio para el proyecto**: langchain\_qa\_project/.  
2. Dentro, crear dos subdirectorios: backend/ y frontend/.  
3. **Crear un entorno virtual (usando Anaconda) de Python para el backend y otro para el frontend**:  
4. **Instalar todas las dependencias**:  
   Bash  
   pip install "fastapi\[all\]" uvicorn langchain langchain-openai langchain-chroma pypdf streamlit requests python-dotenv

5. **Obtener API Key de OpenAI**: Crear una cuenta en la plataforma de OpenAI, generar una clave de API y guardarla en un archivo .env en la raíz del proyecto para mantenerla segura.

### **Paso 2: Desarrollo del Backend (en backend/)**

1. **Crear el archivo principal**: main.py.  
2. **Implementar la lógica de LangChain**: Crear una función o clase que se encargue de:  
   * Cargar un documento desde una ruta de archivo.  
   * Dividirlo en trozos (chunks) usando RecursiveCharacterTextSplitter.  
   * Crear los embeddings para cada trozo usando OpenAIEmbeddings.  
   * Almacenar los trozos y sus embeddings en **ChromaDB**.  
   * Inicializar una cadena RetrievalQA.  
3. **Crear el API con FastAPI**:  
   * Importar FastAPI y pydantic para definir los modelos de petición y respuesta.  
   * Crear un endpoint POST /process-document que reciba la ruta de un archivo, lo procese y lo guarde en la base de datos vectorial.  
   * Crear un endpoint POST /ask que reciba una pregunta (question) y use la cadena RetrievalQA para generar y devolver una respuesta.  
4. **Probar el backend de forma aislada**: Usar herramientas como la documentación automática de FastAPI (/docs) o curl para enviar peticiones y verificar que funciona correctamente.

### **Paso 3: Desarrollo del Frontend (en frontend/)**

1. **Crear el archivo principal**: app.py.  
2. **Diseñar la interfaz con Streamlit**:  
   * Añadir un título y una descripción.  
   * Usar st.file\_uploader para permitir al usuario subir un archivo PDF o TXT.  
   * Una vez subido el archivo, llamar al endpoint /process-document del backend para que lo procese. Mostrar un mensaje de éxito.  
   * Añadir un campo de texto (st.text\_input) para la pregunta del usuario y un botón (st.button).  
3. **Conectar con el Backend**:  
   * Cuando se presione el botón, usar la librería requests para enviar la pregunta al endpoint /ask del backend.  
   * Mostrar un spinner (st.spinner) mientras se espera la respuesta.  
   * Mostrar la respuesta recibida en la interfaz usando st.write o st.success.  
   * Añadir manejo de errores por si el backend no está disponible.

### **Paso 4: Integración y Pruebas**

1. **Ejecutar ambos servicios simultáneamente**:  
   * En un terminal, iniciar el backend: cd backend && uvicorn main:app \--reload  
   * En otro terminal, iniciar el frontend: cd frontend && streamlit run app.py  
2. **Realizar pruebas de extremo a extremo**:  
   * Abrir la app de Streamlit en el navegador.  
   * Subir un documento.  
   * Hacer varias preguntas (simples, complejas, sobre detalles específicos).  
   * Verificar que las respuestas son coherentes y se basan en el contenido del documento.

### **Paso 5 (Opcional): Contenerización con Docker**

1. **Crear un Dockerfile para el backend**.  
2. **Crear un Dockerfile para el frontend**.  
3. **Crear un archivo docker-compose.yml** para orquestar y ejecutar ambos contenedores con un solo comando (docker-compose up), facilitando el despliegue y la portabilidad del proyecto.