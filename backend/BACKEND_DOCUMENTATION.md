# DocuChat Backend Documentation

## Table of Contents
1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Dependencies](#dependencies)
4. [Core Components](#core-components)
5. [Data Models](#data-models)
6. [Core Functions](#core-functions)
7. [API Endpoints](#api-endpoints)
8. [Configuration](#configuration)
9. [Error Handling](#error-handling)
10. [Performance Considerations](#performance-considerations)
11. [Security Features](#security-features)
12. [Development and Deployment](#development-and-deployment)
13. [Database Schema](#database-schema)

## Overview

The DocuChat backend is a FastAPI-based REST API that provides document processing and question-answering capabilities using LangChain, OpenAI embeddings, and ChromaDB for vector storage. The system allows users to upload documents (PDF and TXT), process them into searchable chunks, and ask questions about the content.

## Project Structure

```
backend/
├── __init__.py          # Package initialization file
├── main.py             # Main FastAPI application
├── requirements.txt    # Python dependencies
└── chroma_db/         # ChromaDB storage directory
    └── chroma.sqlite3 # Vector database file
```

## Dependencies

The backend relies on the following key dependencies:

- **FastAPI**: Web framework for building APIs
- **LangChain**: Framework for building LLM applications
- **OpenAI**: For embeddings and language model interactions
- **ChromaDB**: Vector database for storing document embeddings
- **PyPDF**: PDF document processing
- **Pydantic**: Data validation and serialization

### Complete Dependencies List
```
fastapi[all]==0.104.1
uvicorn[standard]==0.24.0
langchain
langchain-openai
langchain-chroma
langchain-community
pypdf==3.17.1
python-dotenv==1.0.0
pydantic
chromadb
openai
```

## Core Components

### 1. FastAPI Application Configuration

```python
app = FastAPI(
    title="DocuChat API",
    description="API for document Q&A system",
    version="1.0.0"
)
```

The application is configured with:
- **CORS Middleware**: Allows cross-origin requests (configured for development with `allow_origins=["*"]`)
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Version Control**: API versioning for future compatibility

### 2. Global State Management

The application maintains global state for:
- `vector_store`: ChromaDB vector store instance
- `qa_chain`: LangChain QA chain for question answering
- `current_document_name`: Name of the currently loaded document

## Data Models

### Pydantic Models for API Communication

#### QuestionRequest
```python
class QuestionRequest(BaseModel):
    question: str
```
- **Purpose**: Validates incoming question requests
- **Fields**: `question` - The user's question text

#### QuestionResponse
```python
class QuestionResponse(BaseModel):
    answer: str
    sources: List[str] = []
```
- **Purpose**: Structures the response to questions
- **Fields**: 
  - `answer` - Generated answer from the LLM
  - `sources` - List of source document chunks used

#### DocumentProcessResponse
```python
class DocumentProcessResponse(BaseModel):
    message: str
    document_name: str
    chunks_processed: int
```
- **Purpose**: Confirms document processing completion
- **Fields**:
  - `message` - Success/error message
  - `document_name` - Name of processed document
  - `chunks_processed` - Number of text chunks created

#### SystemStatusResponse
```python
class SystemStatusResponse(BaseModel):
    document_loaded: bool
    document_name: Optional[str] = None
    chunks_count: Optional[int] = None
```
- **Purpose**: Reports current system state
- **Fields**:
  - `document_loaded` - Whether a document is currently loaded
  - `document_name` - Name of loaded document (if any)
  - `chunks_count` - Number of chunks in the vector store

## Core Functions

### 1. Document Processing Functions

#### get_file_loader()
```python
def get_file_loader(file_path: str, file_extension: str)
```
- **Purpose**: Factory function that returns the appropriate document loader
- **Parameters**:
  - `file_path`: Path to the document file
  - `file_extension`: File extension (.pdf or .txt)
- **Returns**: LangChain document loader instance
- **Supported Formats**: PDF (PyPDFLoader), TXT (TextLoader)

#### process_document()
```python
def process_document(file_path: str, file_extension: str) -> int
```
- **Purpose**: Main document processing pipeline
- **Process Flow**:
  1. Loads document using appropriate loader
  2. Splits text into chunks using RecursiveCharacterTextSplitter
  3. Creates OpenAI embeddings (text-embedding-3-small model)
  4. Stores embeddings in ChromaDB
  5. Initializes QA chain with GPT-4o-mini model
- **Configuration**:
  - Chunk size: 1000 characters
  - Chunk overlap: 200 characters
  - Retrieval: Top 3 most relevant chunks
- **Returns**: Number of chunks created

## API Endpoints

### 1. Health Check
```python
@app.get("/")
async def root()
```
- **Purpose**: Verifies API is running
- **Response**: Simple status message
- **Use Case**: Health monitoring and testing

### 2. System Status
```python
@app.get("/status", response_model=SystemStatusResponse)
async def get_status()
```
- **Purpose**: Reports current system state
- **Response**: Document loading status and metadata
- **Use Case**: Frontend can check if document is loaded before allowing questions

### 3. Document Processing
```python
@app.post("/process-document", response_model=DocumentProcessResponse)
async def process_document_endpoint(file: UploadFile = File(...))
```
- **Purpose**: Upload and process documents
- **Process**:
  1. Validates file type (.pdf or .txt)
  2. Saves to temporary file
  3. Processes document through pipeline
  4. Cleans up temporary file
- **Error Handling**: Returns HTTP 400 for unsupported formats, 500 for processing errors
- **Response**: Processing confirmation with chunk count

### 4. Question Answering
```python
@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest)
```
- **Purpose**: Answer questions about loaded documents
- **Process**:
  1. Validates document is loaded
  2. Uses QA chain to generate answer
  3. Extracts source document chunks
  4. Returns answer with source previews
- **Error Handling**: Returns HTTP 400 if no document loaded, 500 for processing errors
- **Response**: Answer with source document snippets

### 5. Document Cleanup
```python
@app.delete("/clear-document")
async def clear_document()
```
- **Purpose**: Reset system state and clear loaded document
- **Process**:
  1. Clears global variables
  2. Removes ChromaDB directory
  3. Resets system to initial state
- **Use Case**: Allows users to switch documents or start fresh

## Configuration

### Environment Variables

The application uses the following environment variables:

- `OPENAI_API_KEY`: Required OpenAI API key for embeddings and LLM
- `CHROMA_DB_PATH`: ChromaDB storage directory (default: "./chroma_db")
- `BACKEND_HOST`: Server host (default: "localhost")
- `BACKEND_PORT`: Server port (default: 8000)

### CORS Configuration
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Error Handling

The application implements comprehensive error handling:

1. **Input Validation**: Pydantic models validate all requests
2. **File Type Validation**: Only PDF and TXT files accepted
3. **State Validation**: Ensures documents are loaded before questions
4. **Exception Handling**: Catches and returns appropriate HTTP status codes
5. **Resource Cleanup**: Temporary files are properly cleaned up

### HTTP Status Codes
- `200`: Success
- `400`: Bad Request (invalid file type, no document loaded)
- `500`: Internal Server Error (processing errors)

## Performance Considerations

1. **Asynchronous Operations**: All endpoints use async/await for non-blocking I/O
2. **Vector Search**: Uses efficient similarity search in ChromaDB
3. **Chunking Strategy**: Optimized chunk size and overlap for retrieval
4. **Memory Management**: Temporary files are cleaned up immediately after processing
5. **Embedding Model**: Uses "text-embedding-3-small" for optimal performance/cost ratio

## Security Features

1. **CORS Configuration**: Configurable cross-origin resource sharing
2. **Input Sanitization**: File type validation prevents malicious uploads
3. **Environment Variables**: Sensitive data stored in environment variables
4. **Error Message Sanitization**: Internal errors are not exposed to clients
5. **File Upload Limits**: Temporary file handling prevents disk space attacks

## Development and Deployment

### Local Development
The application can be run using:
```bash
python main.py
```

This starts a Uvicorn server with:
- Hot reload enabled for development
- Configurable host and port
- Auto-generated API documentation at `/docs`

### Production Considerations
- Set specific CORS origins instead of `["*"]`
- Use environment-specific configuration
- Implement proper logging and monitoring
- Consider using a production ASGI server like Gunicorn

## Database Schema

### ChromaDB Structure
The ChromaDB database stores:
- **Document Embeddings**: 1536-dimensional vectors from OpenAI
- **Document Metadata**: Source information, page numbers, chunk indices
- **Collection Management**: Organized document storage and retrieval

### Vector Search Configuration
- **Search Strategy**: Similarity search with top-k retrieval
- **Retrieval Count**: Top 3 most relevant chunks per question
- **Persistence**: Local SQLite storage with automatic persistence

## API Documentation

### Interactive Documentation
FastAPI automatically generates interactive API documentation:
- **Swagger UI**: Available at `/docs`
- **ReDoc**: Available at `/redoc`
- **OpenAPI Schema**: Available at `/openapi.json`

### Example Usage

#### Process a Document
```bash
curl -X POST "http://localhost:8000/process-document" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@document.pdf"
```

#### Ask a Question
```bash
curl -X POST "http://localhost:8000/ask" \
     -H "accept: application/json" \
     -H "Content-Type: application/json" \
     -d '{"question": "What is the main topic of this document?"}'
```

#### Check System Status
```bash
curl -X GET "http://localhost:8000/status" \
     -H "accept: application/json"
```

## Troubleshooting

### Common Issues

1. **Missing OpenAI API Key**: Ensure `OPENAI_API_KEY` is set in environment
2. **Unsupported File Format**: Only PDF and TXT files are supported
3. **No Document Loaded**: Upload a document before asking questions
4. **ChromaDB Errors**: Check disk space and permissions for `./chroma_db` directory

### Debug Information
- Check application logs for detailed error messages
- Verify environment variables are properly set
- Ensure all dependencies are installed correctly

---

*This documentation covers the complete backend implementation of the DocuChat system. For additional support or questions, refer to the project's main README or create an issue in the project repository.*