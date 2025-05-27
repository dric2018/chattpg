from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse

import requests

import os.path as osp
import shutil
from .model_manager import ModelManager
from .rag import RAGEngine

app         = FastAPI()
manager     = ModelManager("app/models")
rag         = RAGEngine()
rag.load_documents()


@app.get("/")
def root():
    return FileResponse("frontend/index.html")

@app.get("/api/models")
def get_models():
    print("📡 /api/models hit")
    return manager.list_models()

@app.post("/api/load")
async def load_model(request: Request):
    data = await request.json()
    manager.load_model(data["model"])
    return {"status": "loaded", "model": data["model"]}

@app.post("/api/chat")
async def chat(request: Request):
    data = await request.json()

    user_prompt = data["prompt"]
    chunks      = rag.query(user_prompt)
    prompt      = "\n\n".join(["Use the context to answer:", *chunks, f"Question: {user_prompt}", "Answer:"])
    response    = manager.infer(prompt)

    return {"response": response} 

@app.post("/api/upload")
async def upload(file: UploadFile = File(...)):
    path = osp.join("app/uploads", file.filename)
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    rag.load_documents()

    return {"status": "uploaded", "filename": file.filename}

@app.post("/api/chat_stream")
async def stream_chat_rag(request: Request):
    data = await request.json()
    user_prompt = data["prompt"]
    context_chunks = rag.query(user_prompt)
    full_prompt = "\n\n".join(context_chunks + [user_prompt])

    def generate():
        for chunk in manager.model(full_prompt, stream=True):
            yield chunk["choices"][0]["text"]

    return StreamingResponse(generate(), media_type="text/plain")

app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
