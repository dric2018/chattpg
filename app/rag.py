import os
import os.path as osp
import faiss
import fitz
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter

class RAGEngine:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.embedder = SentenceTransformer(model_name)
        self.index = None
        self.texts = []

    def load_documents(self, folder:str="app/uploads"):
        splitter    = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        documents   = []

        for fname in os.listdir(folder):
            path = osp.join(folder, fname)
            if fname.endswith(".txt"):
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read()
            elif fname.endswith(".pdf"):
                text = self.extract_text_from_pdf(path)
            else:
                continue
            
            docs = splitter.split_text(text)
            documents.extend(docs)

        self.texts = documents
        embeddings = self.embedder.encode(documents, convert_to_numpy=True)
        self.index = faiss.IndexFlatL2(embeddings.shape[-1])
        self.index.add(embeddings)

    def extract_text_from_pdf(self, path):
        text = ""
        with fitz.open(path) as doc:
            for page in doc:
                text += page.get_text()
        return text

    def query(self, question, top_k:int=3):
        q_embed = self.embedder.encode([question], convert_to_numpy=True)
        D, I    = self.index.search(q_embed, top_k)
        return [self.texts[i] for i in I[0]]
