#!/bin/bash

set -e  # Stop on error

echo "👉 Building frontend (React + Vite)..."
cd frontend
npm install
npm run build
cd ..
