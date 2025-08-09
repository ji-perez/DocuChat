import os
import tempfile
from typing import List, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import chromadb
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.schema import Document

# Cargar variables de entorno
load_dotenv()

# Verificar que la API key esté configurada
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY no está configurada en las variables de entorno")

app = FastAPI(
    title="DocuChat API",
    description="API para sistema de preguntas y respuestas sobre documentos",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variables globales para el estado del sistema
vector_store: Optional[Chroma] = None
qa_chain: Optional[RetrievalQA] = None
current_document_name: Optional[str] = None

# Modelos Pydantic para las peticiones y respuestas
class QuestionRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    answer: str
    sources: List[str] = []

class DocumentProcessResponse(BaseModel):
    message: str
    document_name: str
    chunks_processed: int

class SystemStatusResponse(BaseModel):
    document_loaded: bool
    document_name: Optional[str] = None
    chunks_count: Optional[int] = None

def get_file_loader(file_path: str, file_extension: str):
    """Obtiene el loader apropiado según la extensión del archivo"""
    if file_extension.lower() == '.pdf':
        return PyPDFLoader(file_path)
    elif file_extension.lower() == '.txt':
        return TextLoader(file_path, encoding='utf-8')
    else:
        raise ValueError(f"Formato de archivo no soportado: {file_extension}")

def process_document(file_path: str, file_extension: str) -> int:
    """Procesa un documento y retorna el número de chunks creados"""
    global vector_store, qa_chain, current_document_name
    
    # Cargar el documento
    loader = get_file_loader(file_path, file_extension)
    documents = loader.load()
    
    # Dividir en chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)
    
    # Crear embeddings y almacenar en ChromaDB
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Crear o actualizar la base de datos vectorial
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=os.getenv("CHROMA_DB_PATH", "./chroma_db")
    )
    
    # Crear la cadena de QA
    llm = OpenAI(
        model="gpt-4o-mini",
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True
    )
    
    # Actualizar el nombre del documento actual
    current_document_name = os.path.basename(file_path)
    
    return len(chunks)

@app.get("/")
async def root():
    """Endpoint raíz para verificar que la API está funcionando"""
    return {"message": "DocuChat API está funcionando correctamente"}

@app.get("/status", response_model=SystemStatusResponse)
async def get_status():
    """Obtener el estado actual del sistema"""
    global vector_store, current_document_name
    
    if vector_store is None:
        return SystemStatusResponse(document_loaded=False)
    
    # Obtener el número de documentos en la base de datos
    collection = vector_store._collection
    count = collection.count()
    
    return SystemStatusResponse(
        document_loaded=True,
        document_name=current_document_name,
        chunks_count=count
    )

@app.post("/process-document", response_model=DocumentProcessResponse)
async def process_document_endpoint(file: UploadFile = File(...)):
    """Procesar un documento subido por el usuario"""
    global current_document_name
    
    # Verificar el tipo de archivo
    if not file.filename:
        raise HTTPException(status_code=400, detail="Nombre de archivo no proporcionado")
    
    file_extension = os.path.splitext(file.filename)[1]
    if file_extension.lower() not in ['.pdf', '.txt']:
        raise HTTPException(
            status_code=400, 
            detail="Solo se permiten archivos PDF (.pdf) y texto (.txt)"
        )
    
    try:
        # Guardar el archivo temporalmente
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Procesar el documento
        chunks_count = process_document(temp_file_path, file_extension)
        
        # Limpiar el archivo temporal
        os.unlink(temp_file_path)
        
        return DocumentProcessResponse(
            message=f"Documento procesado exitosamente. {chunks_count} fragmentos creados.",
            document_name=file.filename,
            chunks_processed=chunks_count
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando documento: {str(e)}")

@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """Hacer una pregunta sobre el documento cargado"""
    global qa_chain, vector_store
    
    if qa_chain is None or vector_store is None:
        raise HTTPException(
            status_code=400, 
            detail="No hay ningún documento cargado. Por favor, sube un documento primero."
        )
    
    try:
        # Obtener la respuesta usando la cadena de QA
        result = qa_chain({"query": request.question})
        
        # Extraer la respuesta y las fuentes
        answer = result.get("result", "No se pudo generar una respuesta.")
        source_documents = result.get("source_documents", [])
        
        # Extraer información de las fuentes
        sources = []
        for doc in source_documents:
            if hasattr(doc, 'page_content'):
                # Tomar los primeros 100 caracteres como preview
                preview = doc.page_content[:100] + "..." if len(doc.page_content) > 100 else doc.page_content
                sources.append(preview)
        
        return QuestionResponse(answer=answer, sources=sources)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando respuesta: {str(e)}")

@app.delete("/clear-document")
async def clear_document():
    """Limpiar el documento actual y resetear el sistema"""
    global vector_store, qa_chain, current_document_name
    
    vector_store = None
    qa_chain = None
    current_document_name = None
    
    # Limpiar la base de datos ChromaDB
    try:
        import shutil
        chroma_path = os.getenv("CHROMA_DB_PATH", "./chroma_db")
        if os.path.exists(chroma_path):
            shutil.rmtree(chroma_path)
    except Exception as e:
        print(f"Error limpiando ChromaDB: {e}")
    
    return {"message": "Documento limpiado exitosamente"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("BACKEND_HOST", "localhost"),
        port=int(os.getenv("BACKEND_PORT", 8000)),
        reload=True
    )
