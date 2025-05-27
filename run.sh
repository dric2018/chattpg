#!/bin/bash

set -e  # Stop on error

echo "👉 Running Docker container..."
sudo docker run -p 8080:8080 -v $(pwd)/app/models:/app/app/models chattpg