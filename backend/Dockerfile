FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-ben \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create directory for models but don't copy them during build
# RUN mkdir -p /root/.cache/huggingface/hub

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install uvicorn
# RUN pip install "vine<5.0.0"

# RUN pip install --no-cache-dir PyYAML==6.0

RUN pip install sentencepiece

# RUN pip install typing-extensions==4.3.0

RUN pip install opencv-python-headless

#RUN pip install easyocr

# Copy application code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Don't copy model files during build - they will be mounted at runtime

# Copy rest of application code
COPY . .

# Expose port
EXPOSE 8000

# Default command: run FastAPI with uvicorn
#CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
#CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port=8000"]


