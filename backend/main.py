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

# Load environment variables
load_dotenv()

# Verify that the API key is configured
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY is not set in the environment variables")

app = FastAPI(
    title="DocuChat API",
    description="API for document Q&A system",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for system state
vector_store: Optional[Chroma] = None
qa_chain: Optional[RetrievalQA] = None
current_document_name: Optional[str] = None

# Pydantic models for requests and responses
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
    """Gets the appropriate loader based on the file extension"""
    if file_extension.lower() == '.pdf':
        return PyPDFLoader(file_path)
    elif file_extension.lower() == '.txt':
        return TextLoader(file_path, encoding='utf-8')
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

def process_document(file_path: str, file_extension: str) -> int:
    """Processes a document and returns the number of chunks created"""
    global vector_store, qa_chain, current_document_name
    
    # Upload the document
    loader = get_file_loader(file_path, file_extension)
    documents = loader.load()
    
    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)
    
    # Create embeddings and store in ChromaDB
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create or update the vector database
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=os.getenv("CHROMA_DB_PATH", "./chroma_db")
    )
    
    # Create the QA chain
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
    
    # Update the current document name
    current_document_name = os.path.basename(file_path)
    
    return len(chunks)

@app.get("/")
async def root():
    """Root endpoint to verify the API is working"""
    return {"message": "DocuChat API is working correctly"}

@app.get("/status", response_model=SystemStatusResponse)
async def get_status():
    """Get the current system status"""
    global vector_store, current_document_name
    
    if vector_store is None:
        return SystemStatusResponse(document_loaded=False)
    
    # Get the number of documents in the database
    collection = vector_store._collection
    count = collection.count()
    
    return SystemStatusResponse(
        document_loaded=True,
        document_name=current_document_name,
        chunks_count=count
    )

@app.post("/process-document", response_model=DocumentProcessResponse)
async def process_document_endpoint(file: UploadFile = File(...)):
    """Process a document uploaded by the user"""
    global current_document_name
    
    # Verify the file type
    if not file.filename:
        raise HTTPException(status_code=400, detail="Nombre de archivo no proporcionado")
    
    file_extension = os.path.splitext(file.filename)[1]
    if file_extension.lower() not in ['.pdf', '.txt']:
        raise HTTPException(
            status_code=400, 
            detail="Solo se permiten archivos PDF (.pdf) y texto (.txt)"
        )
    
    try:
        # Save the temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Process the document
        chunks_count = process_document(temp_file_path, file_extension)
        
        # Clean up the temporary file
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
    """Ask a question about the loaded document"""
    global qa_chain, vector_store
    
    if qa_chain is None or vector_store is None:
        raise HTTPException(
            status_code=400, 
            detail="No hay ningún documento cargado. Por favor, sube un documento primero."
        )
    
    try:
        # Get the response using the QA chain
        result = qa_chain({"query": request.question})
        
        # Extract the answer and the sources
        answer = result.get("result", "No se pudo generar una respuesta.")
        source_documents = result.get("source_documents", [])
        
        # Extract information from the sources
        sources = []
        for doc in source_documents:
            if hasattr(doc, 'page_content'):
                # Take the first 100 characters as preview
                preview = doc.page_content[:100] + "..." if len(doc.page_content) > 100 else doc.page_content
                sources.append(preview)
        
        return QuestionResponse(answer=answer, sources=sources)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando respuesta: {str(e)}")

@app.delete("/clear-document")
async def clear_document():
    """Clean the current document and reset the system"""
    global vector_store, qa_chain, current_document_name
    
    vector_store = None
    qa_chain = None
    current_document_name = None
    
    # Clean the ChromaDB database
    try:
        import shutil
        chroma_path = os.getenv("CHROMA_DB_PATH", "./chroma_db")
        if os.path.exists(chroma_path):
            shutil.rmtree(chroma_path)
    except Exception as e:
        print(f"Error cleaning ChromaDB: {e}")
    
    return {"message": "Document cleaned successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("BACKEND_HOST", "localhost"),
        port=int(os.getenv("BACKEND_PORT", 8000)),
        reload=True
    )
