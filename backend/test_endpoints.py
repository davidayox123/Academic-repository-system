import requests
import time

print("Testing backend endpoints step by step...")

# Test 1: Basic health check
print("\n1. Testing health endpoint...")
try:
    response = requests.get("http://localhost:8000/health", timeout=5)
    print(f"✅ Health check: {response.status_code} - {response.text}")
except Exception as e:
    print(f"❌ Health check failed: {e}")

# Test 2: Test CORS endpoint
print("\n2. Testing CORS endpoint...")
try:
    response = requests.get("http://localhost:8000/test-cors", timeout=5)
    print(f"✅ CORS test: {response.status_code} - {response.text}")
except Exception as e:
    print(f"❌ CORS test failed: {e}")

# Test 3: Test root endpoint
print("\n3. Testing root endpoint...")
try:
    response = requests.get("http://localhost:8000/", timeout=5)
    print(f"✅ Root endpoint: {response.status_code} - {response.text}")
except Exception as e:
    print(f"❌ Root endpoint failed: {e}")

# Test 4: Test auth endpoints base
print("\n4. Testing auth base path...")
try:
    response = requests.get("http://localhost:8000/api/v1/auth/", timeout=5)
    print(f"📝 Auth base: {response.status_code} - {response.text}")
except Exception as e:
    print(f"❌ Auth base failed: {e}")

print("\n" + "="*50)
print("If any of these fail, the backend is not properly running.")
