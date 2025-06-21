#!/usr/bin/env python3
"""
Quick test script to verify the Academic Repository System is working
Run this after starting the system to ensure everything is connected properly
"""

import requests
import mysql.connector
import sys
import time
from datetime import datetime

def test_mysql_connection():
    """Test MySQL database connection"""
    print("🗄️  Testing MySQL connection...")
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # Default for XAMPP, adjust if needed
            database='academic_repository'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM documents")
        doc_count = cursor.fetchone()[0]
        
        connection.close()
        print(f"   ✅ MySQL connected successfully!")
        print(f"   📊 Found {user_count} users and {doc_count} documents in database")
        return True
    except Exception as e:
        print(f"   ❌ MySQL connection failed: {e}")
        return False

def test_backend_api():
    """Test FastAPI backend"""
    print("🔧 Testing Backend API...")
    try:
        # Test health endpoint
        response = requests.get("http://127.0.0.1:8000/", timeout=5)
        if response.status_code == 200:
            print("   ✅ Backend API is responding!")
            
            # Test auth endpoint
            auth_response = requests.post(
                "http://127.0.0.1:8000/api/v1/auth/login",
                json={
                    "email": "admin@university.edu",
                    "password": "password123"
                },
                timeout=5
            )
            
            if auth_response.status_code == 200:
                print("   ✅ Authentication is working!")
                token = auth_response.json().get("access_token")
                
                # Test protected endpoint
                headers = {"Authorization": f"Bearer {token}"}
                dashboard_response = requests.get(
                    "http://127.0.0.1:8000/api/v1/dashboard/stats",
                    headers=headers,
                    timeout=5
                )
                
                if dashboard_response.status_code == 200:
                    stats = dashboard_response.json()
                    print(f"   ✅ Dashboard API working! Total documents: {stats.get('total_documents', 'N/A')}")
                    return True
                else:
                    print(f"   ⚠️  Dashboard endpoint issue: {dashboard_response.status_code}")
                    return False
            else:
                print(f"   ❌ Authentication failed: {auth_response.status_code}")
                return False
        else:
            print(f"   ❌ Backend not responding: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to backend - is it running on port 8000?")
        return False
    except Exception as e:
        print(f"   ❌ Backend test failed: {e}")
        return False

def test_frontend():
    """Test React frontend"""
    print("🌐 Testing Frontend...")
    try:
        response = requests.get("http://localhost:5173", timeout=5)
        if response.status_code == 200:
            print("   ✅ Frontend is accessible!")
            return True
        else:
            print(f"   ❌ Frontend returned status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to frontend - is it running on port 5173?")
        return False
    except Exception as e:
        print(f"   ❌ Frontend test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 Academic Repository System - Quick Test")
    print("=" * 60)
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run tests
    mysql_ok = test_mysql_connection()
    print()
    
    backend_ok = test_backend_api()
    print()
    
    frontend_ok = test_frontend()
    print()
    
    # Summary
    print("=" * 60)
    print("📋 Test Summary:")
    print("=" * 60)
    
    all_tests_passed = mysql_ok and backend_ok and frontend_ok
    
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED! System is ready for demonstration!")
        print()
        print("🚀 Quick Start URLs:")
        print("   • Frontend App: http://localhost:5173")
        print("   • Backend API Docs: http://localhost:8000/docs")
        print("   • Database: localhost:3306 (MySQL)")
        print()
        print("👥 Test Accounts:")
        print("   • Admin: admin@university.edu / password123")
        print("   • Supervisor: supervisor1@university.edu / password123")
        print("   • Student: alice.johnson@student.edu / password123")
        print()
        print("✨ Your system is ready for friends to test!")
    else:
        print("❌ Some tests failed. Please check:")
        if not mysql_ok:
            print("   • MySQL server might not be running")
            print("   • Check database credentials in backend/.env")
        if not backend_ok:
            print("   • Backend might not be started")
            print("   • Run: cd backend && uvicorn main:app --reload")
        if not frontend_ok:
            print("   • Frontend might not be started")  
            print("   • Run: cd frontend && npm run dev")
        
        print("\n💡 See QUICK_START_FOR_FRIENDS.md for troubleshooting")
    
    print("=" * 60)
    return 0 if all_tests_passed else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted by user")
        sys.exit(1)
