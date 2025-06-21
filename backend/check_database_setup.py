import pymysql

print("Checking if departments exist in database...")

try:
    conn = pymysql.connect(
        host="localhost",
        port=3306,
        user="academic_user",
        password="260307",
        database="academic_repo_db"
    )
    
    cursor = conn.cursor()
    
    # Check if departments table exists
    cursor.execute("SHOW TABLES LIKE 'departments'")
    dept_table = cursor.fetchone()
    
    if dept_table:
        print("✅ Departments table exists")
        
        # Check departments
        cursor.execute("SELECT id, name FROM departments LIMIT 10")
        departments = cursor.fetchall()
        
        if departments:
            print(f"📊 Found {len(departments)} departments:")
            for dept_id, name in departments:
                print(f"  - {dept_id}: {name}")
        else:
            print("❌ No departments found in table")
    else:
        print("❌ Departments table does not exist")
    
    # Check if users table exists
    cursor.execute("SHOW TABLES LIKE 'users'")
    users_table = cursor.fetchone()
    
    if users_table:
        print("✅ Users table exists")
    else:
        print("❌ Users table does not exist")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Database check failed: {e}")
    import traceback
    traceback.print_exc()
