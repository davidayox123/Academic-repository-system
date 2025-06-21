# 🚀 Academic Repository System - Quick Start Guide

## For Your Friends to Run & Test the Project

---

## ⚡ Super Quick Setup (Under 10 Minutes!)

### **Step 1: Prerequisites Check**
Make sure you have:
- ✅ MySQL Server running (XAMPP/WAMP/Standalone)
- ✅ Node.js installed
- ✅ Python 3.11+ installed

### **Step 2: Clone & Setup Database**
```bash
# Clone the project
git clone <your-repo-url>
cd Academic-repository-system

# Setup database (Windows)
.\setup-database-simple.ps1

# OR setup database (Manual)
mysql -u root -p < database/simple_schema.sql
mysql -u root -p < database/sample_data.sql
```

### **Step 3: Start Backend**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### **Step 4: Start Frontend**
```bash
# New terminal window
cd frontend
npm install
npm run dev
```

### **Step 5: Access the System**
- 🌐 **Main App:** http://localhost:5173
- 📊 **API Docs:** http://localhost:8000/docs
- 🔗 **Database:** localhost:3306 (use MySQL Workbench)

---

## 🎭 Test Accounts (Ready to Use!)

### **👨‍💼 Admin (Full Access)**
```
Email: admin@university.edu
Password: password123
```

### **👨‍🏫 Supervisor (Review Documents)**
```
Email: supervisor1@university.edu
Password: password123
```

### **👩‍🎓 Student (Upload Documents)**
```
Email: alice.johnson@student.edu
Password: password123
```

---

## 🎯 Things to Try & Demo

### **For Presentation:**

1. **Login as Different Users**
   - Show different dashboards for each role
   - Demonstrate role-based access control

2. **Document Workflow**
   - Student: Upload a research paper
   - Supervisor: Review and approve/reject
   - Anyone: Search and download approved papers

3. **Advanced Features**
   - Search with filters (department, year, status)
   - View audit logs (who did what, when)
   - Dashboard analytics and charts

4. **Database Queries** (MySQL Workbench)
   ```sql
   -- Show all documents with their status
   SELECT d.title, u.name as author, d.status, d.created_at 
   FROM documents d 
   JOIN users u ON d.user_id = u.id;

   -- Show review workflow
   SELECT d.title, r.decision, r.comments, r.created_at
   FROM documents d 
   JOIN reviews r ON d.id = r.document_id;

   -- Show audit trail
   SELECT a.action, u.name, a.details, a.created_at 
   FROM audit_logs a 
   JOIN users u ON a.user_id = u.id 
   ORDER BY a.created_at DESC;
   ```

---

## 🐛 Quick Troubleshooting

### **Backend Won't Start?**
```bash
# Check if port 8000 is free
netstat -ano | findstr :8000

# Try different port
uvicorn main:app --reload --port 8001
```

### **Frontend Won't Start?**
```bash
# Clear npm cache
npm cache clean --force
npm install
npm run dev
```

### **Database Connection Issues?**
```bash
# Check MySQL is running
mysql -u root -p -e "SELECT 1;"

# Check database exists
mysql -u root -p -e "SHOW DATABASES LIKE 'academic_repository';"
```

### **CORS Errors?**
- Make sure backend is running on http://127.0.0.1:8000
- Frontend should be on http://localhost:5173
- Check browser console for exact error

---

## 📊 What Makes This Project Special

### **Database Design Excellence:**
- ✅ Proper normalization (3NF)
- ✅ Foreign key relationships
- ✅ Triggers for business rules
- ✅ Views for complex queries
- ✅ Indexes for performance

### **Modern Tech Stack:**
- ✅ React + TypeScript (Frontend)
- ✅ FastAPI + Python (Backend)
- ✅ MySQL with proper schemas
- ✅ JWT Authentication
- ✅ RESTful API design

### **Business Logic Implementation:**
- ✅ Role-based access control
- ✅ Document approval workflow
- ✅ Audit trail logging
- ✅ Advanced search capabilities
- ✅ Real-time notifications

---

## 🎓 For Your Database Course Presentation

### **Key Points to Highlight:**

1. **Database Design:**
   - Show ER diagram
   - Explain normalization
   - Demonstrate relationships

2. **Business Rules Implementation:**
   - Role-based permissions
   - Document workflow states
   - Audit trail requirements

3. **Query Optimization:**
   - Show complex JOIN queries
   - Explain indexing strategy
   - Demonstrate views and triggers

4. **Real-World Application:**
   - Solves actual university problem
   - Scalable architecture
   - Security considerations

---

## 💡 Tips for Demo Success

1. **Prepare Sample Data:** Use the provided test accounts
2. **Practice Workflow:** Know the document submission → review → approval flow
3. **Show Database:** Have MySQL Workbench open to show tables/queries
4. **Highlight Features:** Role-based access, audit logs, search capabilities
5. **Be Ready for Questions:** About database design choices and business rules

---

## 🤝 Getting Help

If something isn't working:
1. Check the main `PROJECT_GUIDE_FOR_FRIENDS.md` for detailed troubleshooting
2. Look at the browser console for errors
3. Check the backend terminal for error messages
4. Verify MySQL is running and accessible

**Remember:** This is a complete, production-ready system that demonstrates advanced database concepts in a real-world application!

---

**Good luck with your presentation! 🎉**
