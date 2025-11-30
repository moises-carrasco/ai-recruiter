# Environment Setup & Startup Rules (Backend + Frontend)

## 1. Backend Environment Setup

- Before running the FastAPI server, ensure the virtual environment is activated.
- The virtual environment name is **`iachlg`**.
- Activate it with:
  ```bash
  pyenv activate iachlg
  ```
- Make sure no previous Uvicorn process is running on port **8000**:
  ```bash
  lsof -i :8000
  kill -9 <PID>
  ```

### Start the Backend Server
From the **project root**, run:
```bash
uvicorn app.main:app --reload --port 8000 --app-dir backend
```

---

## 2. Database Preparation

- The project uses **SQLite**.
- The database file is:
  ```
  interview_system.db
  ```
  located in the **project root**.
- This database already contains some tables.  
  Before creating or altering tables, verify whether they already exist.
- If the schema needs updates, please also sync those changes in the DDL script: backend/db/schema.sql
- Before applying any change to the database please ask for confirmation.

---

## 3. Frontend Environment Setup

- Ensure Node.js version **18** is installed:
  ```bash
  node -v
  ```
- If the frontend runs on any port other than **3000**, **3001**, or **3003**, update the backend CORS configuration in:
  ```
  backend/app/core/config.py
  ```
  to add the correct frontend origin and prevent CORS errors.

---
