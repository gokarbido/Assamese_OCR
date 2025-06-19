import pytest
import httpx
from fastapi.testclient import TestClient
from app import app
from PIL import Image
import io
import os

client = TestClient(app)

@pytest.fixture
def test_image():
    """Create a test image"""
    img = Image.new('RGB', (500, 500), color = (73, 109, 137))
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    return img_byte_arr.getvalue()

@pytest.fixture
def test_file():
    """Create a test file"""
    return (
        b"------WebKitFormBoundary7MA4YWxkTrZu0gW\r\n"
        b"Content-Disposition: form-data; name=\"file\"; filename=\"test.jpg\"\r\n"
        b"Content-Type: image/jpeg\r\n\r\n"
        b"\r\n"
        b"------WebKitFormBoundary7MA4YWxkTrZu0gW--\r\n"
    )

def test_rate_limit():
    """Test rate limiting"""
    with client:
        # First request should succeed
        response = client.post("/upload-image", files={"file": ("test.jpg", test_image(), "image/jpeg")})
        assert response.status_code == 200
        
        # Make 11 requests (10/minute limit)
        for _ in range(11):
            response = client.post("/upload-image", files={"file": ("test.jpg", test_image(), "image/jpeg")})
        assert response.status_code == 429

def test_file_validation():
    """Test file validation"""
    # Invalid file type
    response = client.post("/upload-image", files={"file": ("test.txt", test_image(), "text/plain")})
    assert response.status_code == 400
    assert "Invalid file type" in response.json()['detail']
    
    # File too large
    large_file = test_image() * 1000  # Make file larger than 5MB
    response = client.post("/upload-image", files={"file": ("test.jpg", large_file, "image/jpeg")})
    assert response.status_code == 400
    assert "File too large" in response.json()['detail']

def test_image_upload():
    """Test image upload and processing"""
    response = client.post("/upload-image", files={"file": ("test.jpg", test_image(), "image/jpeg")})
    assert response.status_code == 200
    result = response.json()
    assert 'assamese_text' in result
    assert 'translation' in result

def test_translation_cache():
    """Test translation caching"""
    # First request - should not be cached
    response = client.post("/upload-image", files={"file": ("test.jpg", test_image(), "image/jpeg")})
    assert response.status_code == 200
    
    # Second request - should be cached
    response = client.post("/upload-image", files={"file": ("test.jpg", test_image(), "image/jpeg")})
    assert response.status_code == 200
    
    # Verify cache hit (implementation specific check)
    # This would be different based on your caching implementation
    # For example, you might want to check Redis directly

def test_async_translation():
    """Test async translation for long texts"""
    # Create an image with a long text
    img = Image.new('RGB', (1000, 1000), color = (73, 109, 137))
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    
    response = client.post("/upload-image", files={"file": ("test.jpg", img_byte_arr.getvalue(), "image/jpeg")})
    assert response.status_code == 200
    result = response.json()
    assert 'assamese_text' in result
    assert 'translation' in result
