#!/bin/bash

set -e  # Stop on error

echo "👉 Building Docker image..."
sudo docker build -t chattpg .