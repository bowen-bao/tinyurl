#!/bin/bash
set -e

echo "⚙️ Setting up development environment..."

# -------------------------
# Backend (Django/Python)
# -------------------------
echo "🐍 Setting up backend..."
cd backend

# Create venv if missing
if [ ! -d ".venv" ]; then
  echo "📦 Creating Python virtualenv..."
  python3 -m venv .venv
fi

source .venv/bin/activate
pip install --upgrade pip

# Install dev dependencies (includes prod + testing/linting tools)
pip install -r requirements-dev.txt

cd ..

# -------------------------
# Frontend (React/Node)
# -------------------------
echo "⚛️ Setting up frontend..."
cd frontend

# Install Node dependencies if missing
if [ ! -d "node_modules" ]; then
  echo "📦 Installing npm packages..."
  npm install
else
  echo "✅ npm packages already installed (skipping)"
fi

cd ..

echo "✅ Development environment ready!"
echo "👉 Use ./quick_dev_start.sh to launch servers."
