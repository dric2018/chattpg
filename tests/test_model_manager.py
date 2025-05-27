from app.model_manager import ModelManager
import os

def test_list_models(tmp_path):
    (tmp_path / "test1.gguf").write_text("fake")
    (tmp_path / "test2.txt").write_text("ignore this")
    manager = ModelManager(str(tmp_path))
    assert "test1.gguf" in manager.list_models()

def test_infer_mock(monkeypatch):
    manager = ModelManager(".")
    monkeypatch.setattr(manager, "model", lambda prompt, max_tokens: {"choices": [{"text": "mocked output"}]})
    result = manager.infer("test")
    assert result == "mocked output"