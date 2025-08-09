# 📋 Installation Guide - DocuChat

## Prerequisites

- **Python 3.9+** installed on your system
- **OpenAI account** with valid API key
- **Git** (optional, for cloning the repository)

## 🚀 Quick Installation

### 1. Configure Environment Variables

```bash
# Copy the environment variables template
cp env_template.txt .env

# Edit the .env file and add your OpenAI API key
nano .env  # or use your preferred editor
```

In the `.env` file, replace `your_openai_api_key_here` with your real OpenAI API key:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 2. Install Dependencies

#### Option A: Automatic configuration with Anaconda (Recommended)

```bash
# Configure virtual environments and install dependencies
./setup_environments.sh
```

#### Option B: Manual installation with Anaconda

```bash
# Create virtual environments
conda create -n docuchat-backend python=3.9 -y
conda create -n docuchat-frontend python=3.9 -y

# Install backend dependencies
conda activate docuchat-backend
cd backend
pip install -r requirements.txt

# Install frontend dependencies
conda activate docuchat-frontend
cd frontend
pip install -r requirements.txt
```

## 🏃‍♂️ Run the Project

### 1. Start the Backend

```bash
# Option A: Using the script
./start_backend.sh

# Option B: Manually
conda activate docuchat-backend
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at: http://localhost:8000
API Documentation: http://localhost:8000/docs

### 2. Start the Frontend

```bash
# Option A: Using the script
./start_frontend.sh

# Option B: Manually
conda activate docuchat-frontend
cd frontend
streamlit run app.py --server.port 8501
```

The frontend will be available at: http://localhost:8501

## 🔧 Advanced Configuration

### Available Environment Variables

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `BACKEND_HOST` | Backend host | localhost |
| `BACKEND_PORT` | Backend port | 8000 |
| `FRONTEND_PORT` | Frontend port | 8501 |
| `CHROMA_DB_PATH` | ChromaDB database path | ./chroma_db |

### OpenAI Models Used

- **Embeddings**: `text-embedding-3-small`
- **LLM**: `gpt-4o-mini`

To change these models, edit the `backend/main.py` file.

## 🐛 Troubleshooting

### Error: "OPENAI_API_KEY is not configured"

1. Verify that the `.env` file exists in the root directory
2. Make sure `OPENAI_API_KEY` is configured correctly
3. Restart the backend after changing environment variables

### Error: "Backend not available"

1. Verify that the backend is running at http://localhost:8000
2. Check the backend logs for errors
3. Make sure port 8000 is not occupied by another application

### Error: "Could not generate a response"

1. Verify that your OpenAI API key is valid
2. Check your OpenAI credit balance
3. Make sure the document was processed correctly

### Dependency errors

```bash
# Update pip
pip install --upgrade pip

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## 📁 Project Structure

```
DocuChat/
├── backend/                 # FastAPI server
│   ├── main.py             # Main backend logic
│   ├── requirements.txt    # Backend dependencies
│   └── __init__.py
├── frontend/               # Streamlit application
│   ├── app.py             # User interface
│   ├── requirements.txt   # Frontend dependencies
│   └── __init__.py
├── .env                   # Environment variables (create from env_template.txt)
├── env_template.txt       # Environment variables template
├── start_backend.sh       # Script to start backend
├── start_frontend.sh      # Script to start frontend
├── .gitignore            # Files to ignore by Git
├── README.md             # Main documentation
└── INSTALLATION.md       # This guide
```

## 🔒 Security

- **Never** upload your `.env` file to a public repository
- Keep your OpenAI API key secure
- In production, use system environment variables instead of `.env` files

## 📞 Support

If you encounter problems:

1. Check the error logs in the console
2. Verify that all dependencies are installed correctly
3. Make sure your OpenAI API key is valid
4. Consult the API documentation at http://localhost:8000/docs
