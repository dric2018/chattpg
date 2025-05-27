import os
import os.path as osp
from llama_cpp import Llama

class ModelManager:
    def __init__(self, model_dir:str):
        self.model_dir  = model_dir
        self.model      = None

    def list_models(self):
        return [f for f in os.listdir(self.model_dir) if f.endswith(".gguf")]
    

    def load_model(self, model_name):
        path        = osp.join(self.model_dir, model_name)
        self.model  = Llama(model_path=path, n_ctx=2048, n_threads=4)

    def infer(self, prompt):
        result = self.model(prompt=prompt[:2048], max_tokens=256)
        return result["choices"][0]["text"].strip()