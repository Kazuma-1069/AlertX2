#!/usr/bin/env bash
set -e

echo "Starting AlertX2 FastAPI server..."
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
