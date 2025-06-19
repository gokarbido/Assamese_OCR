from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import pytesseract
from PIL import Image
import io
from transformers import pipeline
import torch
import os
from dotenv import load_dotenv
import redis
from tasks import translate_text
import hashlib
import json
import time
#import easyocr
import numpy as np

load_dotenv()

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, lambda request, exc: JSONResponse(status_code=429, content={"error": "Rate limit exceeded"}))

# Initialize Redis client
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=int(os.getenv('REDIS_DB', 0)),
    password=os.getenv('REDIS_PASSWORD', None)
)

# Initialize translator with device selection
try:
    # Try to use GPU if available and CUDA is properly configured
    if torch.cuda.is_available():
        device = 0
        print("CUDA is available. Using GPU for translation.")
    else:
        device = -1
        print("CUDA is not available. Using CPU for translation.")
    
    # Set environment variables to help with CUDA initialization
    os.environ['CUDA_LAUNCH_BLOCKING'] = '1'
    os.environ['CUDA_VISIBLE_DEVICES'] = '0' if device == 0 else ''
    
    # Initialize translator with error handling
    translator = pipeline("translation", model="Helsinki-NLP/opus-mt-bn-en", device=device)
    print(f"Translator initialized successfully on device: {device}")
except Exception as e:
    print(f"Error initializing translator: {str(e)}")
    # Fallback to CPU if initialization fails
    device = -1
    translator = pipeline("translation", model="Helsinki-NLP/opus-mt-bn-en", device=device)
    print("Falling back to CPU for translation.")

# File validation constants
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', 5))
CACHE_TTL = int(os.getenv('CACHE_TTL', 3600))  # 1 hour

# Initialize EasyOCR reader globally
# try:
#     easyocr_reader = easyocr.Reader(['as'], gpu=False)
#     print("EasyOCR reader initialized successfully.")
# except Exception as e:
#     print(f"Error initializing EasyOCR reader: {e}")
#     easyocr_reader = None

async def get_cached_translation(text: str):
    """Get translation from Redis cache"""
    if not text:
        return None
    
    cache_key = f"translation:{hashlib.md5(text.encode()).hexdigest()}"
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    return None

async def set_cached_translation(text: str, translation: str):
    """Set translation in Redis cache"""
    if not text or not translation:
        return
    
    cache_key = f"translation:{hashlib.md5(text.encode()).hexdigest()}"
    redis_client.setex(cache_key, CACHE_TTL, json.dumps({
        "text": text,
        "translation": translation,
        "timestamp": time.time()
    }))

def compress_image(image: Image.Image) -> Image.Image:
    """Compress image while maintaining quality"""
    width, height = image.size
    max_size = 1920  # Maximum dimension
    
    if max(width, height) > max_size:
        ratio = max_size / max(width, height)
        new_size = (int(width * ratio), int(height * ratio))
        image = image.resize(new_size, Image.Resampling.LANCZOS)
    
    # Save to BytesIO and optimize
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG', quality=85, optimize=True)
    buffer.seek(0)
    
    # Load back into PIL
    return Image.open(buffer)

def validate_file(file: UploadFile, content: bytes):
    ext = file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPG/PNG allowed.")
    if len(content) > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large (max 5MB).")

@app.post("/upload-image")
@limiter.limit(os.getenv('RATE_LIMIT', '10/minute'))
async def upload_image(request: Request, file: UploadFile = File(...)):
    content = await file.read()
    validate_file(file, content)
    
    try:
        # Load and compress image
        image = Image.open(io.BytesIO(content)).convert("RGB")
        image = compress_image(image)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image: {str(e)}")
    
    # OCR using pytesseract (Bengali script for Assamese)
    custom_config = r'--oem 1 --psm 6'
    assamese_text = pytesseract.image_to_string(image, lang="ben", config=custom_config).strip()
    
    # Check cache first
    cached_result = await get_cached_translation(assamese_text)
    if cached_result:
        return {"assamese_text": assamese_text, "translation": cached_result['translation']}
    
    # Translation
    translation = ""
    if assamese_text:
        try:
            # Use Celery for long texts
            if len(assamese_text) > 1000:  # Threshold for async processing
                translation = await translate_text.delay(assamese_text).get(timeout=30)
            else:
                translation = translator(assamese_text)[0]['translation_text']
                
            # Cache the result
            await set_cached_translation(assamese_text, translation)
            
        except Exception as e:
            print(f"Translation error: {str(e)}")
            translation = f"Translation error: {str(e)}"
    
    return {"assamese_text": assamese_text, "translation": translation}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)    