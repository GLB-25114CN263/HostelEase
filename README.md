# HostelEase — Smart Hostel Management System

HostelEase is a B.Tech mini-project prototype for organizing common hostel tasks in one web application.

## Technology stack
- **Frontend:** React, Vite, React Router, CSS
- **Backend:** Python, Flask, Flask-CORS
- **Database:** MongoDB with PyMongo
- **Security basics:** passwords for newly registered users are hashed using Werkzeug

## Features
- Student registration and login
- Student profile page
- Dashboard statistics from MongoDB
- Room records and availability status
- Fee records with total, paid, pending and automatically calculated status
- Complaint submission and resolve/reopen status
- Visitor entry and exit status
- Hostel notices
- REST API health and database connection checks

> This is an educational mini-project, not a production-ready system. Before public deployment, add proper authentication tokens/sessions, role-based authorization, server-side access controls, input validation, and secure production configuration. Fee records are not connected to a payment gateway.

## Requirements
Install Python 3.10+ and Node.js 20.19+ (or a compatible newer version). MongoDB Community Server must be installed and running locally, unless you configure a cloud MongoDB URI.

## Setup on Windows / VS Code

### 1. Configure MongoDB
The included `backend/.env` uses local MongoDB:

```dotenv
MONGO_URI=mongodb://localhost:27017/hostelease
```

If your MongoDB is hosted elsewhere, change `MONGO_URI` in `backend/.env`. Never share real credentials or commit a private database URI to GitHub.

### 2. Start the backend
Open a VS Code terminal at the project root and run these commands one by one:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Keep this terminal open. Test these endpoints in Chrome:
- `http://127.0.0.1:5000/api/health` — should show backend status `ok`.
- `http://127.0.0.1:5000/api/db-test` — should show MongoDB connection status `ok`.

If PowerShell blocks activation, use `python -m pip install -r requirements.txt` and `python app.py` without activating the venv, or fix the local PowerShell execution policy with your administrator's guidance.

### 3. Start the frontend
Open a **second** VS Code terminal at the project root:

```powershell
cd frontend
npm install
npm run dev
```

Open the exact `Local` URL printed by Vite (usually `http://localhost:5173`). If 5173 is occupied, Vite may use 5174; the backend CORS list includes both.

## Suggested demo flow for project evaluation
1. Open the home page and explain the six modules.
2. Register a new test student with a unique email.
3. Log in using that account and show the dashboard/profile.
4. Add a room record and show it in Rooms.
5. Add a fee record with total amount and paid amount; the backend calculates pending amount and status.
6. Add a complaint and mark it resolved.
7. Add a visitor and toggle entry/exit status.
8. Add a notice and show the record list.
9. Show `/api/health` and `/api/db-test` to explain the backend/database connection.

Use test data for a classroom demonstration. Do not use other students' private information.

## API overview
- `GET /api/health`
- `GET /api/db-test`
- `POST /api/register`
- `POST /api/login`
- `GET /api/students`
- `GET /api/dashboard`
- `GET, POST /api/rooms|fees|complaints|visitors|notices`
- `PATCH /api/<collection>/<record_id>`
- `DELETE /api/<collection>/<record_id>`

## Database
MongoDB database name: `hostelease`. Main collections: `users`, `rooms`, `fees`, `complaints`, `visitors`, `notices`.
