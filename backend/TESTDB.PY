import pymysql
conn = pymysql.connect(
    host="localhost",
    port=3306,
    user="academic_user",
    password="260307",
    database="academic_repo_db"
)
print("Connected!")
conn.close()