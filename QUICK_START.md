# 🚀 Quick Start - DocuChat

## Recommended Workflow

### 1. Initial Setup (One time only)

```bash
# 1. Configure environment variables
cp env_template.txt .env
# Edit .env and add your OPENAI_API_KEY

# 2. Create virtual environments and install dependencies
./setup_environments.sh
```

### 2. Run the Project

#### Terminal 1 - Backend
```bash
./start_backend.sh
```

#### Terminal 2 - Frontend
```bash
./start_frontend.sh
```

### 3. Use the Application

1. Open http://localhost:8501 in your browser
2. Upload a PDF or TXT document
3. Ask questions about the content

## 📋 Manual Commands (Alternative)

If you prefer to do it manually:

### Configure Environments
```bash
# Create environments
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

### Run Services
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

## 🔧 Environment Management

### View available environments
```bash
conda env list
```

### Activate environment
```bash
conda activate docuchat-backend    # For backend
conda activate docuchat-frontend   # For frontend
```

### Deactivate environment
```bash
conda deactivate
```

### Remove environment (if you need to recreate it)
```bash
conda env remove -n docuchat-backend
conda env remove -n docuchat-frontend
```

## 🌐 Important URLs

- **Frontend**: http://localhost:8501
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## ⚠️ Important Notes

1. **Always activate the virtual environment** before running services
2. **Keep both services running** (backend and frontend)
3. **Configure your OpenAI API key** in the `.env` file
4. **Use separate terminals** for backend and frontend
