# Academic Research Repository System
## Complete Project Guide for Friends & Presentation Practice

---

## 🎯 Project Overview

This is a **Database Management System Course Project** - an Academic Research Repository System that manages research documents with role-based access control, document workflow, and comprehensive audit trails.

### **What This System Does:**
- **Students & Staff** can upload research documents
- **Supervisors** can review and approve/reject documents  
- **Admins** can manage the entire system
- **Everyone** can search and download approved documents
- **System** automatically logs all activities for audit trails

---

## 🚀 How to Run the Complete System

### **Prerequisites:**
- MySQL Server running on port 3306
- Node.js installed
- Python 3.11+ installed

### **Quick Start (5 minutes):**

1. **Start Backend:**
   ```bash
   cd backend
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

2. **Start Frontend:** (New terminal)
   ```bash
   cd frontend  
   npm run dev
   ```

3. **Access the System:**
   - **Frontend Application:** http://localhost:5173
   - **Backend API Documentation:** http://localhost:8000/docs
   - **Database:** MySQL on localhost:3306

---

## 👥 Test User Accounts

Use these accounts to test different user roles:

### **Admin Account:**
- **Email:** admin@university.edu
- **Password:** password123
- **Can:** Manage everything, view all documents, user management

### **Supervisor Account:**
- **Email:** supervisor1@university.edu  
- **Password:** password123
- **Can:** Review documents, approve/reject, view department documents

### **Student Account:**
- **Email:** alice.johnson@student.edu
- **Password:** password123
- **Can:** Upload documents, view own documents, download approved documents

### **Staff Account:**
- **Email:** staff1@university.edu
- **Password:** password123
- **Can:** Upload documents, view department documents, download approved documents

---

## 🎯 Key Features to Demonstrate

### **1. Role-Based Access Control**
- Different users see different features based on their role
- Students can't approve documents
- Only supervisors can review documents from their department

### **2. Document Workflow**
1. **Upload** → Document starts as "draft"
2. **Submit** → Status changes to "submitted" 
3. **Review** → Supervisor reviews and comments
4. **Approve/Reject** → Final decision with reasons
5. **Publish** → Approved documents become downloadable

### **3. Advanced Search & Filtering**
- Search by title, author, keywords
- Filter by department, year, status
- Advanced metadata search

### **4. Audit Trail**
- Every action is logged (upload, review, download, etc.)
- Complete traceability for compliance
- IP address and timestamp tracking

### **5. Dashboard Analytics**
- Document statistics by department
- User activity metrics
- System usage trends
- Performance analytics

---

## 📊 Database Features (For DMS Course)

### **Complete ERD Implementation:**
- **8 Tables:** Users, Documents, Departments, Reviews, Downloads, Audit Logs, Metadata, Collaborators
- **Complex Relationships:** One-to-many, many-to-many with proper foreign keys
- **Business Rule Enforcement:** Through constraints and triggers
- **Advanced Queries:** JOINs, subqueries, aggregations, analytics

### **Business Rules Implemented:**
✅ Role-based access control  
✅ Document approval workflow  
✅ Department-based organization  
✅ Audit trail for all actions  
✅ Metadata requirement validation  
✅ Unique title per uploader  
✅ Supervisor department alignment  
✅ Download tracking  

---

## 🎭 Presentation Practice Guide

### **For Database Management System Course (20 minutes):**

#### **1. Introduction (2 minutes)**
"This Academic Research Repository System solves the problem of scattered research documents in universities by providing a centralized, role-based platform for document management."

#### **2. Database Schema Demo (6 minutes)**
- Open MySQL Workbench
- Show table structure: `SHOW TABLES;`
- Demonstrate relationships: `DESCRIBE users; DESCRIBE documents;`
- Explain normalization and constraints

#### **3. Business Rules Demo (8 minutes)**
```sql
-- Show role-based document uploads
SELECT u.name, u.role, COUNT(d.id) as documents 
FROM users u LEFT JOIN documents d ON u.id = d.uploader_id 
GROUP BY u.id, u.name, u.role;

-- Show supervisor review process  
SELECT r.*, u.name as reviewer, d.title 
FROM reviews r 
JOIN users u ON r.reviewer_id = u.id 
JOIN documents d ON r.document_id = d.id;

-- Show audit trail
SELECT al.action, al.timestamp, u.name, d.title 
FROM audit_logs al 
JOIN users u ON al.user_id = u.id 
LEFT JOIN documents d ON al.document_id = d.id 
ORDER BY al.timestamp DESC;
```

#### **4. Advanced Features (4 minutes)**
- Complex analytics queries
- Performance optimization with indexes
- Trigger demonstrations
- View usage for simplified access

### **For General Presentation:**

#### **1. Live Demo (15 minutes)**
1. **Login as Student** → Upload a document
2. **Login as Supervisor** → Review and approve
3. **Login as different user** → Search and download
4. **Login as Admin** → View analytics dashboard

#### **2. Technical Architecture (5 minutes)**
- React frontend with TypeScript
- FastAPI backend with Python
- MySQL database with comprehensive schema
- RESTful API design

---

## 📋 Project Completeness Checklist

### **✅ Backend Complete:**
- ✅ All 8 database entities implemented
- ✅ Complete CRUD operations for all entities
- ✅ Role-based authentication & authorization  
- ✅ Document upload & file management
- ✅ Review workflow implementation
- ✅ Audit logging for all actions
- ✅ Advanced search & filtering APIs
- ✅ Dashboard analytics APIs
- ✅ Comprehensive error handling
- ✅ API documentation (Swagger/OpenAPI)

### **✅ Database Complete:**
- ✅ Complete schema with all relationships
- ✅ Business rule enforcement
- ✅ Sample data for demonstration
- ✅ Complex queries for analytics
- ✅ Proper indexing for performance
- ✅ Triggers for automatic logging
- ✅ Views for simplified access

### **✅ Frontend Complete:**
- ✅ Role-based UI components
- ✅ Document upload interface
- ✅ Review & approval workflow UI
- ✅ Advanced search functionality
- ✅ Dashboard with analytics
- ✅ User management interface
- ✅ Responsive design
- ✅ Error handling & user feedback

### **✅ Integration Complete:**
- ✅ Backend-Frontend communication
- ✅ Database-Backend integration
- ✅ File upload & download working
- ✅ Authentication flow complete
- ✅ Real-time updates working

---

## 🛠️ Quick Troubleshooting

### **If Backend Won't Start:**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### **If Frontend Won't Start:**
```bash
cd frontend
npm install
npm run dev
```

### **If Database Connection Fails:**
```bash
mysql -u root -p260307
# Then run: USE academic_repo_db;
```

---

## 📁 Project Structure
```
Academic-repository-system/
├── backend/          # FastAPI backend
├── frontend/         # React frontend  
├── database/         # SQL scripts & documentation
├── uploads/          # Document storage
├── docker-compose.yml # Container setup
└── README.md         # Project documentation
```

---

## 🎓 Academic Value

### **For Database Management System Course:**
- **Complete ERD Implementation** with 8 normalized tables
- **Advanced SQL** with complex joins, subqueries, triggers
- **Business Logic** enforcement through database constraints
- **Real-world Application** solving actual university problems

### **For Software Engineering:**
- **Full-stack Development** with modern technologies
- **Clean Architecture** with separation of concerns
- **API Design** following RESTful principles
- **User Experience** with role-based interfaces

---

## 🤝 How Friends Can Help Practice

1. **Role-play different users** (student, supervisor, admin)
2. **Ask technical questions** about database design
3. **Test edge cases** in the application
4. **Time your presentation** to stay within limits
5. **Provide feedback** on explanation clarity

---

**This is a complete, production-ready Academic Research Repository System! 🚀**

**Total Development Time:** ~40 hours  
**Technologies Used:** React, TypeScript, FastAPI, Python, MySQL, Docker  
**Lines of Code:** ~2000+ (Backend) + ~1500+ (Frontend) + ~500+ (SQL)  
**Features Implemented:** 25+ core features with full CRUD operations
