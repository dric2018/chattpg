# ChatTPG: A simple app with LLM and text summarization support

ChatTPG is a browser-based application that enables users to interact with local LLMs for answering queries in natural language, and summarizing documents in either PDF or directly pasted text inputs. The system is fully containerized for portability and supports huggingface API integration for model downloads.

### Design
The application is composed of two components:

* Backaned (FastAPI + llama-cpp-python)

    Handles model loading, document querying, and API endpoints for chat, upload and model inference.
    It supports quantized GGUF models and FAISS-based vector seach over chunked documents (txt/PDF).

* Frontend (React + Vite)

    A simple single-page UI for chat interaction, document upload, and copy-paste text input.
    it includes a UI tab for entering optional API keys (e.g. Hugging Face) and displays chat history inline.

The backend exposes `/api/...` endpoints for the above functionalities.

### Usage
Run with Docker

```bash
docker build -t chattpg .
docker run -p8080:8080 chattpg
```
The open your browser and visit: http://localhost:8080 to use the app

Run tests with docker

```bash
docker run chattpg python /home/src/tests/run_tests.py
```
PS: Note that not all required (or envisioned) tests have been implemented by the time of the submission.

### Acknowledgement

The overall app was designed and structured with the assistance of chatGPT for the initial setup, debugging, and frontend development. However, the actual implementation is my own work.
I also acknowledge the fact that designing the app on the server side took some time, but the design of the frontend took quite a while due to my very limited ease with frontend functions.

