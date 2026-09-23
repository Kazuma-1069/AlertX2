#!/usr/bin/env bash
set -e

echo "=== Setting up AlertX2 Development Environment ==="

# Backend virtual environment
cd backend
python -m venv venv
source venv/bin/activate || source venv/Scripts/activate
pip install --upgrade pip
pip install -r requirements.txt
cd ..

echo "Backend dependencies installed."
echo "Setup complete. Copy .env.example to .env and configure secrets."
