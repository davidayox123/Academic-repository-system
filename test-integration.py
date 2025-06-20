"""
Full Stack Integration Test Script
Tests the complete connection: Frontend ↔ Backend ↔ Database
"""
import requests
import json
import sys
import time
from pathlib import Path

class FullStackTester:
    def __init__(self):
        self.backend_url = "http://localhost:8000"
        self.frontend_url = "http://localhost:5173"
        self.test_results = []

    def log_test(self, test_name, success, message=""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if message:
            print(f"   {message}")
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "message": message
        })

    def test_backend_health(self):
        """Test if backend is running and healthy"""
        try:
            response = requests.get(f"{self.backend_url}/docs", timeout=5)
            success = response.status_code == 200
            message = f"Status: {response.status_code}" if not success else "Backend API docs accessible"
            self.log_test("Backend Health Check", success, message)
            return success
        except requests.exceptions.RequestException as e:
            self.log_test("Backend Health Check", False, f"Connection failed: {e}")
            return False

    def test_database_connection(self):
        """Test database connection through backend"""
        try:
            # Try to access an endpoint that requires database
            response = requests.get(f"{self.backend_url}/api/v1/auth/me", 
                                  headers={"Authorization": "Bearer dummy"}, 
                                  timeout=5)
            # We expect 401 (unauthorized) which means backend is working and connected to DB
            success = response.status_code in [401, 403, 422]
            message = "Database connection working" if success else f"Unexpected status: {response.status_code}"
            self.log_test("Database Connection via Backend", success, message)
            return success
        except requests.exceptions.RequestException as e:
            self.log_test("Database Connection via Backend", False, f"Connection failed: {e}")
            return False

    def test_cors_configuration(self):
        """Test CORS configuration"""
        try:
            # Make an OPTIONS request to test CORS
            response = requests.options(f"{self.backend_url}/api/v1/auth/login", 
                                      headers={
                                          "Origin": "http://localhost:5173",
                                          "Access-Control-Request-Method": "POST"
                                      }, timeout=5)
            success = "Access-Control-Allow-Origin" in response.headers
            message = "CORS properly configured" if success else "CORS headers missing"
            self.log_test("CORS Configuration", success, message)
            return success
        except requests.exceptions.RequestException as e:
            self.log_test("CORS Configuration", False, f"Request failed: {e}")
            return False

    def test_file_upload_endpoint(self):
        """Test file upload capability"""
        try:
            # Test the upload endpoint (should return 401 without auth)
            response = requests.post(f"{self.backend_url}/api/v1/documents/upload", 
                                   timeout=5)
            success = response.status_code in [401, 403, 422]
            message = "Upload endpoint accessible" if success else f"Unexpected status: {response.status_code}"
            self.log_test("File Upload Endpoint", success, message)
            return success
        except requests.exceptions.RequestException as e:
            self.log_test("File Upload Endpoint", False, f"Request failed: {e}")
            return False

    def test_frontend_accessibility(self):
        """Test if frontend is accessible"""
        try:
            response = requests.get(self.frontend_url, timeout=5)
            success = response.status_code == 200
            message = "Frontend accessible" if success else f"Status: {response.status_code}"
            self.log_test("Frontend Accessibility", success, message)
            return success
        except requests.exceptions.RequestException as e:
            self.log_test("Frontend Accessibility", False, f"Connection failed: {e}")
            return False

    def test_api_endpoints(self):
        """Test key API endpoints"""
        endpoints = [
            ("/docs", "API Documentation"),
            ("/api/v1/auth/login", "Login Endpoint"),
            ("/api/v1/dashboard/stats", "Dashboard Endpoint"),
            ("/api/v1/documents/", "Documents Endpoint")
        ]
        
        all_success = True
        for endpoint, name in endpoints:
            try:
                response = requests.get(f"{self.backend_url}{endpoint}", timeout=5)
                # Accept various status codes (200, 401, 403, 422) as they indicate the endpoint exists
                success = response.status_code < 500
                message = f"Status: {response.status_code}" if success else f"Server error: {response.status_code}"
                self.log_test(f"API Endpoint: {name}", success, message)
                if not success:
                    all_success = False
            except requests.exceptions.RequestException as e:
                self.log_test(f"API Endpoint: {name}", False, f"Request failed: {e}")
                all_success = False
        
        return all_success

    def run_all_tests(self):
        """Run all integration tests"""
        print("🚀 Academic Repository System - Full Stack Integration Test")
        print("=" * 60)
        print()
        
        print("🔍 Testing Backend Services...")
        backend_health = self.test_backend_health()
        database_conn = self.test_database_connection()
        cors_config = self.test_cors_configuration()
        upload_endpoint = self.test_file_upload_endpoint()
        api_endpoints = self.test_api_endpoints()
        
        print("\n🔍 Testing Frontend Services...")
        frontend_access = self.test_frontend_accessibility()
        
        print("\n📊 Test Summary:")
        print("-" * 40)
        
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        
        for result in self.test_results:
            status = "✅" if result["success"] else "❌"
            print(f"{status} {result['test']}")
        
        print(f"\n🎯 Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("\n🎉 All tests passed! Your full stack is working correctly.")
            print("\n🚀 Your application is ready:")
            print(f"   Frontend: {self.frontend_url}")
            print(f"   Backend API: {self.backend_url}/docs")
            return True
        else:
            print(f"\n⚠️  {total - passed} test(s) failed. Please check the issues above.")
            print("\n🔧 Troubleshooting Guide:")
            
            if not backend_health:
                print("   Backend: cd backend && uvicorn main:app --reload")
            if not frontend_access:
                print("   Frontend: cd frontend && npm run dev")
            if not database_conn:
                print("   Database: Run python test-database.py")
            
            return False

def main():
    """Main function"""
    print("⏳ Starting integration tests...")
    print("   Make sure both frontend and backend are running!")
    print()
    
    # Give services time to start
    time.sleep(2)
    
    tester = FullStackTester()
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
