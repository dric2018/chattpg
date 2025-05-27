from datasets import load_dataset
import os

dataset = load_dataset("ccdv/arxiv-summarization", split="train[:5]")
output_dir = "app/uploads"
os.makedirs(output_dir, exist_ok=True)

for i, sample in enumerate(dataset):
    article = sample["article"]
    with open(f"{output_dir}/arxiv_{i+1}.txt", "w", encoding="utf-8") as f:
        f.write(article)