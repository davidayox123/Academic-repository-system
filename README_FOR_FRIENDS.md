# 🎓 Academic Repository System
### Database Management System Course Project

**A complete research document management system with role-based access control, review workflows, and audit trails.**

---

## 🚀 Quick Start (For Friends)

### **Option 1: Super Easy (Just Double-Click!)**
1. Double-click `start-for-friends.bat`
2. Follow the prompts (enter MySQL password when asked)
3. Wait for both servers to start
4. Go to http://localhost:5173

### **Option 2: Manual Setup**
1. **Setup Database:**
   ```bash
   mysql -u root -p < database/simple_schema.sql
   mysql -u root -p < database/sample_data.sql
   ```

2. **Start Backend:**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

3. **Start Frontend:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

### **Option 3: Test Everything is Working**
```bash
python test-system.py
```

---

## 🎭 Test Accounts

| Role | Email | Password | What They Can Do |
|------|-------|----------|------------------|
| **Admin** | admin@university.edu | password123 | Everything - manage users, view all docs |
| **Supervisor** | supervisor1@university.edu | password123 | Review & approve documents |
| **Student** | alice.johnson@student.edu | password123 | Upload documents, view own docs |
| **Staff** | staff1@university.edu | password123 | Upload docs, view department docs |

---

## 🎯 Things to Try

### **Document Workflow Demo:**
1. **Login as Student** → Upload a research paper
2. **Login as Supervisor** → Review and approve the paper
3. **Login as Anyone** → Search and download approved papers

### **Role-Based Access:**
- Notice different dashboard views for each role
- Try accessing admin features as a student (it won't work!)
- See how supervisors can only review docs from their department

### **Advanced Features:**
- **Search & Filter:** Find documents by title, author, department, year
- **Audit Trail:** See who did what and when in the system
- **Dashboard Analytics:** View charts and statistics
- **Real-time Updates:** Watch document status change live

---

## 🌐 Access URLs

- **🏠 Main Application:** http://localhost:5173
- **📊 API Documentation:** http://localhost:8000/docs  
- **🗄️ Database:** localhost:3306 (MySQL Workbench)

---

## 💡 For Database Course Presentation

### **What Makes This Special:**
- ✅ **Proper Database Design:** Normalized tables, foreign keys, constraints
- ✅ **Business Rules:** Implemented through triggers and application logic
- ✅ **Role-Based Security:** Different users see different features
- ✅ **Audit Trail:** Complete tracking of all system activities
- ✅ **Modern Tech Stack:** React + FastAPI + MySQL

### **Key Demo Points:**
1. **Show the Database Schema** (MySQL Workbench)
2. **Demonstrate Role-Based Access** (login as different users)
3. **Walk Through Document Workflow** (upload → review → approve)
4. **Show Advanced Queries** (joins, aggregations, views)
5. **Highlight Business Rules** (permissions, status transitions)

---

## 🔧 Troubleshooting

### **Common Issues:**
- **"Cannot connect to MySQL"** → Start XAMPP/WAMP or MySQL service
- **"Backend not responding"** → Check if port 8000 is free
- **"Frontend won't load"** → Clear browser cache, check port 5173
- **"Login doesn't work"** → Verify database has sample data loaded

### **Quick Fixes:**
```bash
# Test if everything is working
python test-system.py

# Restart backend
cd backend && uvicorn main:app --reload --port 8001

# Restart frontend  
cd frontend && npm run dev -- --port 5174

# Reset database
mysql -u root -p < database/simple_schema.sql
mysql -u root -p < database/sample_data.sql
```

---

## 📚 More Information

- 📖 **Detailed Guide:** `PROJECT_GUIDE_FOR_FRIENDS.md`
- 🚀 **Quick Start:** `QUICK_START_FOR_FRIENDS.md`
- 🎤 **Presentation Guide:** `PRESENTATION_GUIDE.md`

---

## 🎉 Have Fun!

This is a real, working system that demonstrates advanced database concepts in action. Play around, break things, and see how it all works together!

**Good luck with the presentation! 🚀**
