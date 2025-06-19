# Setup Instructions

## Prerequisites

### Backend Dependencies
1. **Tesseract OCR**:
   ```bash
   # Install Tesseract and Bengali language pack
   sudo apt-get update
   sudo apt-get install tesseract-ocr tesseract-ocr-ben
   ```

2. **Redis** (for caching):
   ```bash
   # Install Redis
   sudo apt-get install redis-server
   ```

3. **Celery** (for async processing):
   ```bash
   # Install Celery
   pip install celery
   ```

### Frontend Dependencies
1. **Node.js** (version 16+):
   ```bash
   # Install Node.js
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
   sudo apt-get install -y nodejs
   ```

2. **Vue CLI**:
   ```bash
   npm install -g @vue/cli
   ```

## Model Rationale

### OCR Model
- **Tesseract OCR**: Chosen for its:
  - High accuracy with Bengali script
  - Custom-trained model support
  - Open-source and well-maintained
  - Good performance on Assamese/Bengali text

### Translation Model
- **Hugging Face Transformers**: Selected because:
  - Large, pre-trained models available
  - Good performance on Indian languages
  - Easy integration with Python
  - Active community and frequent updates
  - Supports multiple translation directions

## Docker Setup

### Build Containers
```bash
# Build backend
docker build -t assamese-ocr-backend -f backend/Dockerfile .

# Build frontend
docker build -t assamese-ocr-frontend -f frontend/Dockerfile .
```

### Run Containers
```bash
# Run Redis
docker run -d --name redis redis

# Run backend
docker run -d --name assamese-ocr-backend -p 8000:8000 assamese-ocr-backend

# Run frontend
docker run -d --name assamese-ocr-frontend -p 8080:80 assamese-ocr-frontend
```

## Project Structure
```
assamese-ocr/
├── backend/              # FastAPI server
│   ├── app.py           # Main application
│   ├── requirements.txt # Python dependencies
│   └── tasks.py         # Celery tasks
│  
├── frontend/            # Vue.js application
│   ├── src/
│   │   ├── components/  # Vue components
│   │   └── main.js      # App entry point
│   ├── package.json     # Node dependencies
│   └── Dockerfile       # Frontend container
├── docker-compose.yml   # Manage multi-container
└── docs/               # Documentation
    └── setup.md        # Setup instructions
```
