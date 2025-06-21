import pymysql
import time

print("Testing database connection...")
start_time = time.time()

try:
    conn = pymysql.connect(
        host="localhost",
        port=3306,  # or 3306 if using local MySQL
        user="academic_user",
        password="260307",
        database="academic_repo_db",
        connect_timeout=5
    )
    
    # Test a simple query
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    
    end_time = time.time()
    print(f"✅ Database connection successful in {end_time - start_time:.2f} seconds")
    print(f"Query result: {result}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    end_time = time.time()
    print(f"❌ Database connection failed after {end_time - start_time:.2f} seconds")
    print(f"Error: {e}")
