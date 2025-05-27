#!/bin/bash

set -e  # Stop on error

echo "👉 Building Docker image..."
sudo docker build -t chattpg .

echo "👉 Running Docker container..."
sudo docker run -p 8080:8080 -v $(pwd)/app/models:/app/app/models chattpg