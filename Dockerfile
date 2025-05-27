FROM python:3.12-slim AS base

RUN apt-get update && apt-get install -y \
    build-essential cmake libopenblas-dev git curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# running on cpu only
ENV CMAKE_ARGS="-DLLAMA_CUBLAS=OFF"

WORKDIR /home/src

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY tests ./tests

# build frontend
FROM node:18-slim AS frontend-builder
WORKDIR /app
COPY frontend ./frontend
WORKDIR /app/frontend
RUN npm install && npm run build

WORKDIR /app

# finalize image
FROM base AS final
COPY --from=frontend-builder /app/frontend/dist /home/src/frontend

WORKDIR /home/src
EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
