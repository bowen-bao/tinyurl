#!/bin/bash
set -e

echo "Launching full development stack..."

# -------------------------
# Backend (Django)
# -------------------------
echo "Starting Django backend on http://localhost:8000"
cd backend
source .venv/bin/activate
python manage.py runserver 0.0.0.0:8000 &
BACKEND_PID=$!
cd ..

# -------------------------
# Frontend (React)
# -------------------------
echo "Starting React frontend on http://localhost:3000"
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

# -------------------------
# Cleanup when exiting
# -------------------------
trap "echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID" EXIT

echo "✅ Both servers running:
   - Django API:   http://localhost:8000
   - React client: http://localhost:3000"

wait