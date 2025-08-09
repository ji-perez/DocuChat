# **Project: Document Q&A System 💬**

Version: 1.0  
Date: 2025-08-07  
Name: DocuChat

## **1\. Project Description**

### **What is it about?**

This project consists of developing a web application that allows users to upload their own documents (such as PDF or text files) and maintain a conversation with them. Essentially, it's a specialized "chatbot" that uses the content of a specific document as its only source of knowledge to answer questions.

### **Main Objective**

The goal is to build a functional and decoupled **Retrieval-Augmented Generation (RAG)** system. This will allow users to extract information and obtain accurate answers to complex questions about their documents without having to read them completely, leveraging the power of Large Language Models (LLMs).

### **Key Features**

* **Document Upload**: The user interface will allow the user to select and upload a document (initially, .pdf and .txt).  
* **Document Processing**: The system will process the uploaded document, divide it into manageable fragments, and create vector representations (embeddings) of each fragment.  
* **Q&A Interface**: A chat area where the user can write a question.  
* **Answer Generation**: The system will search for the most relevant fragments of the document to answer the user's question and use an LLM to generate a coherent and contextualized response.

---

## **2\. Technologies Used**

The project will be divided into two main components: a backend for AI logic and a frontend for user interaction.

### **Backend (Logic API)**

* **Python 3.9+**: The base programming language for all development.  
* **LangChain**: The main framework for orchestrating all AI logic components. It will be used to load documents (DocumentLoaders), split them (TextSplitters), interact with the embedding model and LLM, and build the retrieval chain (RetrievalQA).  
* **FastAPI**: A high-performance web framework for building the REST API. It will be responsible for exposing LangChain logic through HTTP endpoints, managing frontend requests.  
* **OpenAI**: Its API will be used to access two key services:  
  * **Embedding Models** (text-embedding-3-small): To convert text fragments into numerical vectors.  
  * **Language Model (LLM)** (gpt-3.5-turbo or gpt-4o): The brain that will generate responses in natural language.  
* **ChromaDB**: An open-source vector database. It will store the vectors of text fragments and allow efficient semantic similarity searches.  
* **Uvicorn**: An ASGI (Asynchronous Server Gateway Interface) server that will be used to run the FastAPI application.
* **Anaconda**: Virtual environment generation and management will be done with Anaconda.

### **Frontend (User Interface)**

* **Streamlit**: A Python framework that allows creating interactive web applications with very little code. Ideal for building the user interface quickly and easily.  
* **Requests**: A standard Python library for making HTTP requests. Streamlit will use it to communicate with the FastAPI backend.

---

## **3\. System Architecture**

We will adopt a decoupled **client-server architecture**, which provides us with scalability and modularity.

[Client-server architecture diagram image](https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcRfljlOrd8cDb5ShcecLetBMKDNiDVc21MOiBfDtfGEI1sowEuXk69puLw05wrWSphYjcR1G7qwP50eQq9933sh53SmatFWyyqRvuhQjJWFG45Ee4A)

* **Backend (Server)**: It's a **FastAPI** application that acts as the artificial intelligence engine. Its only responsibility is to receive a question, process it through the LangChain flow, and return a response. It knows nothing about how the user interface looks. It contains the LLM, vector database, and all RAG logic.  
* **Frontend (Client)**: It's a **Streamlit** application that runs in the user's browser (or on a web server). Its responsibility is to render the graphical interface, capture user input (the question), and display the response. It performs no AI processing; it simply communicates with the backend through its API.

### **Communication Flow:**

1. The user writes a question in the Streamlit interface and clicks "Send".  
2. The Streamlit script packages the question into a JSON payload.  
3. Streamlit sends a POST request to the /ask endpoint of the FastAPI backend.  
4. FastAPI receives the request, extracts the question, and passes it to the LangChain RetrievalQA chain.  
5. LangChain:  
   a. Converts the user's question into a vector.  
   b. Searches in ChromaDB for text fragments whose vectors are most similar to the question vector.  
   c. Sends the retrieved fragments and the original question to the OpenAI LLM.  
6. The LLM generates a response based on the provided context.  
7. FastAPI receives the LLM response and returns it to the frontend in JSON format.  
8. Streamlit receives the response, processes it, and displays it in the interface for the user to read.

---

## **4\. Development Plan (Step by Step)**

### **Step 1: Environment Setup**

1. **Create a project directory**: langchain\_qa\_project/.  
2. Inside, create two subdirectories: backend/ and frontend/.  
3. **Create a virtual environment (using Anaconda) for the backend and another for the frontend**:  
4. **Install all dependencies**:  
   Bash  
   pip install "fastapi\[all\]" uvicorn langchain langchain-openai langchain-chroma pypdf streamlit requests python-dotenv

5. **Get OpenAI API Key**: Create an account on the OpenAI platform, generate an API key, and save it in a .env file in the project root to keep it secure.

### **Step 2: Backend Development (in backend/)**

1. **Create the main file**: main.py.  
2. **Implement LangChain logic**: Create a function or class that handles:  
   * Loading a document from a file path.  
   * Splitting it into chunks using RecursiveCharacterTextSplitter.  
   * Creating embeddings for each chunk using OpenAIEmbeddings.  
   * Storing chunks and their embeddings in **ChromaDB**.  
   * Initializing a RetrievalQA chain.  
3. **Create the API with FastAPI**:  
   * Import FastAPI and pydantic to define request and response models.  
   * Create a POST /process-document endpoint that receives a file path, processes it, and saves it to the vector database.  
   * Create a POST /ask endpoint that receives a question and uses the RetrievalQA chain to generate and return a response.  
4. **Test the backend in isolation**: Use tools like FastAPI's automatic documentation (/docs) or curl to send requests and verify it works correctly.

### **Step 3: Frontend Development (in frontend/)**

1. **Create the main file**: app.py.  
2. **Design the interface with Streamlit**:  
   * Add a title and description.  
   * Use st.file\_uploader to allow the user to upload a PDF or TXT file.  
   * Once the file is uploaded, call the /process-document endpoint of the backend to process it. Show a success message.  
   * Add a text field (st.text\_input) for the user's question and a button (st.button).  
3. **Connect with the Backend**:  
   * When the button is pressed, use the requests library to send the question to the /ask endpoint of the backend.  
   * Show a spinner (st.spinner) while waiting for the response.  
   * Display the received response in the interface using st.write or st.success.  
   * Add error handling in case the backend is not available.

### **Step 4: Integration and Testing**

1. **Run both services simultaneously**:  
   * In one terminal, start the backend: cd backend && uvicorn main:app \--reload  
   * In another terminal, start the frontend: cd frontend && streamlit run app.py  
2. **Perform end-to-end testing**:  
   * Open the Streamlit app in the browser.  
   * Upload a document.  
   * Ask several questions (simple, complex, about specific details).  
   * Verify that the responses are coherent and based on the document content.

### **Step 5 (Optional): Docker Containerization**

1. **Create a Dockerfile for the backend**.  
2. **Create a Dockerfile for the frontend**.  
3. **Create a docker-compose.yml file** to orchestrate and run both containers with a single command (docker-compose up), facilitating project deployment and portability.