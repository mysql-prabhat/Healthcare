# Healthcare
AI health care report review of patients


# Healthcare AI Platform - Setup Guide

## Repository Setup

### 1. Clone Repository

```bash
git clone <repository-url>
```

### 2. Checkout Branch

```bash
git checkout <branch-name>
```

### 3. Pull Latest Changes

```bash
git pull
```

---

# Backend Setup

## Navigate to Backend Folder

Open Git Bash and run:

```bash
cd backend
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Using Docker

### Build Containers

```bash
docker compose build --no-cache
```

### Start Containers

```bash
docker compose up -d
```

## Run Without Docker

### Uvicorn

```bash
uvicorn app.main:app --reload
```

### FastAPI CLI

```bash
fastapi dev
```

---

## Backend URLs

### Application

```text
http://localhost:8000/
```

### Swagger UI

```text
http://localhost:8000/docs
```

---

# Frontend Setup

## Start Frontend

```bash
npm run dev
```

### Frontend URL

```text
http://localhost:5173/
```

---

# Initial Database Setup

Run the following commands in sequence:

```bash
python db/create_tables.py
```

```bash
python db/seed.py
```

```bash
python db/seed_patients.py
```

---

# Docker PostgreSQL

## Connect to Database

```bash
docker exec -it healthcare-postgres psql -U admin -d healthcare
```

---

## Useful SQL Commands

### Get All Documents

```sql
SELECT * FROM documents;
```

### Remove Payload Column

```sql
ALTER TABLE documents
DROP COLUMN payload;
```

### Update Title Length

```sql
ALTER TABLE documents
ALTER COLUMN title TYPE CHAR(100);
```

---

# Docker Services

The application uses the following containers:

```text
healthcare-backend
healthcare-worker
healthcare-postgres
healthcare-redis
healthcare-ollama
```

Verify running containers:

```bash
docker ps
```

---

# Application Workflow

```text
Login
  ↓
Select Patient
  ↓
Upload Document
  ↓
Redis Queue
  ↓
Document Worker
  ↓
Ollama Processing
  ↓
AI Summary Generation
  ↓
Review Queue
  ↓
Approve / Reject
  ↓
Audit Logs
```

---

# Key Application Features

- JWT Authentication
- Role-Based Access Control (RBAC)
- Patient Management
- Document Upload
- AI-Powered Clinical Summaries (Ollama)
- Review Queue
- Approval Workflow
- Audit Logging
- Redis Background Processing
- Retry & Dead Letter Queue Support
- FHIR-Ready Architecture
- Multi-Tenant Design

---

# Troubleshooting

## Restart Docker Environment

```bash
docker compose down
docker compose up -d --build
```

## View Backend Logs

```bash
docker logs healthcare-backend
```

## View Worker Logs

```bash
docker logs healthcare-worker
```

## View PostgreSQL Logs

```bash
docker logs healthcare-postgres
```

## View Ollama Logs

```bash
docker logs healthcare-ollama
```

---

# Development URLs

| Service | URL |
|----------|------|
| Frontend | http://localhost:5173 |
| Backend | http://localhost:8000 |
| Swagger | http://localhost:8000/docs |
| Ollama API | http://localhost:11434 |

---
