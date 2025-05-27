from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_models_list():
    res = client.get("/api/models")
    assert res.status_code == 200
    assert isinstance(res.json(), list)

def test_file_upload_and_reload():
    with open("app/uploads/arxiv_2.txt", "rb") as f:
        res = client.post("/api/upload", files={"file": ("sample.txt", f, "text/plain")})
        assert res.status_code == 200

def test_model_loading():
    response = client.post("/api/load", json={"model": "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"})
    assert response.status_code == 200

def test_chat_response(monkeypatch):
    monkeypatch.setattr("app.main.manager.infer", lambda prompt: "mocked answer")
    res = client.post("/api/chat", json={"prompt": "What does the rainbow mean?"})
    assert res.status_code == 200
    assert "response" in res.json()