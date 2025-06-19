from celery import Celery
from transformers import pipeline
#import torch
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Celery
app = Celery('tasks',
             broker=os.getenv('CELERY_BROKER_URL'),
             backend=os.getenv('CELERY_RESULT_BACKEND'))

# Configure Celery
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Kolkata',
    enable_utc=True,
)

# Initialize translator with CPU (Celery workers run on CPU)
device = -1
translator = pipeline("translation", model="Helsinki-NLP/opus-mt-bn-en", device=device)

@app.task
async def translate_text(text: str):
    """Translate text using transformers pipeline"""
    try:
        translation = translator(text)[0]['translation_text']
        return translation
    except Exception as e:
        return f"Translation error: {str(e)}"
