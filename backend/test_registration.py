import requests
import time

print("Testing backend registration endpoint...")

# Test data - make sure department exists
test_user = {
    "name": "Test User",
    "email": "test123@example.com",  # Use different email in case user already exists
    "password": "TestPassword123!",
    "confirm_password": "TestPassword123!",
    "role": "student",
    "department_id": "dept-001"  # This should match your database
}

try:
    print("Sending POST request to registration endpoint...")
    start_time = time.time()
    
    response = requests.post(
        "http://localhost:8000/api/v1/auth/register",
        json=test_user,
        timeout=30  # Use same timeout as frontend
    )
    
    end_time = time.time()
    
    print(f"⏱️  Response time: {end_time - start_time:.2f} seconds")
    print(f"📊 Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Registration successful!")
        print(f"📝 Response: {response.json()}")
    else:
        print("❌ Registration failed!")
        print(f"📝 Error response: {response.text}")
    
except requests.exceptions.Timeout:
    print("❌ Request timed out after 30 seconds")
except requests.exceptions.ConnectionError:
    print("❌ Could not connect to backend")
except Exception as e:
    print(f"❌ Error: {e}")
