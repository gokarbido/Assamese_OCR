# Assamese Text Translation Dashboard

A web application to extract Assamese text from images and translate it into English.

## Features
- **Image Upload:** Drag-and-drop or browse to upload JPG/PNG images (max 5MB)
- **OCR:** Extracts Assamese text from images using Tesseract (Bengali script)
- **Translation:** Translates extracted text to English using Hugging Face Transformers
- **Result Display:** Shows both Assamese and English text, with copy-to-clipboard buttons
- **Dark/Light Mode:** Toggle between dark and light themes
- **State Management:** Uses Pinia for frontend state
- **Rate Limiting:** Backend limits to 10 requests/minute
- **Caching:** Redis caching for translations to prevent duplicate API calls
- **Image Optimization:** Automatic image compression to maintain quality while reducing size
- **Async Processing:** Long text translations processed asynchronously using Celery
- **Testing:** Comprehensive test suite with both frontend (Vitest) and backend (Pytest) tests

---

## Tech Stack
- **Frontend:** Vue 3 (Composition API), Pinia, Axios, Vite, Tailwind CSS
- **Backend:** FastAPI, pytesseract, transformers, slowapi, Redis, Celery
- **Testing:** Vitest (frontend), Pytest (backend)

---

## Setup Instructions

### 1. Backend
#### Prerequisites
- Python 3.10+
- Tesseract OCR installed with Bengali language pack (`ben`)
- Redis server
- Celery

#### Install Tesseract & Bengali Language Pack
- **Windows:**
  1. Download and install [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
  2. Download `ben.traineddata` from [tessdata_best](https://github.com/tesseract-ocr/tessdata_best) or [tessdata](https://github.com/tesseract-ocr/tessdata)
  3. Place it in your Tesseract `tessdata` directory (e.g., `C:\Program Files\Tesseract-OCR\tessdata`)
  4. Run `tesseract --list-langs` to confirm `ben` is listed

- **Linux:**
  1. sudo apt update
  2. sudo apt install tesseract-ocr  
  
#### Install Python Dependencies
```
cd backend
pip install -r requirements.txt
```

#### Install Redis in WSL 2
1. Open WSL 2 terminal
2. Update package list:
```
sudo apt update
```
3. Install Redis:
```
sudo apt install redis-server
```
4. Start Redis server:
```
sudo service redis-server start
```
5. Verify Redis is running:
```
redis-cli ping
```
You should see `PONG` if Redis is running successfully

#### Start Celery Worker
```
celery -A tasks worker --loglevel=info
```

#### Run Backend
```
uvicorn app:app --reload
```
- The API will be available at `http://localhost:8000/upload-image`

---

### 2. Frontend
#### Prerequisites
- Node.js 18+

#### Install Dependencies
```
cd frontend
npm install
```

#### Run Frontend
```
npm run dev
```
- The app will be available at `http://localhost:5173`

#### Run Tests
```
# Backend tests
pytest

# Frontend tests
npm run test:unit
```

---

## Usage
1. Open the frontend in your browser
2. Upload an image containing Assamese text
3. View the extracted text and English translation
4. Use the copy buttons as needed
5. Toggle dark/light mode from the top-right

---

## Troubleshooting
- **OCR not working?** Ensure Tesseract is installed and `ben` language pack is present
- **CORS issues?** The backend allows all origins by default, but you can restrict in `app.py`
- **API errors?** Check backend logs for details

---

## License
MIT 
