"""
Downloads large assets (OSM graph + trained model) from HuggingFace Hub.
Runs during Docker build on Railway. Set HF_REPO_ID build argument to your
HuggingFace dataset repo, e.g. "your-username/gridlock-assets".
"""
import os
from pathlib import Path

HF_REPO_ID = os.environ.get("HF_REPO_ID", "")
GRAPH_PATH = Path("data/processed/bengaluru_drive.graphml")
MODEL_PATH = Path("backend/models/impact_model.pkl")


def download():
    if not HF_REPO_ID:
        print("[assets] HF_REPO_ID not set — skipping download (files must exist locally)")
        return

    from huggingface_hub import hf_hub_download

    GRAPH_PATH.parent.mkdir(parents=True, exist_ok=True)
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    if not GRAPH_PATH.exists():
        print(f"[assets] Downloading OSM graph from {HF_REPO_ID}...")
        hf_hub_download(
            repo_id=HF_REPO_ID,
            filename="bengaluru_drive.graphml",
            local_dir=str(GRAPH_PATH.parent),
            repo_type="dataset",
        )
        print("[assets] OSM graph ready.")
    else:
        print("[assets] OSM graph already present — skipping.")

    if not MODEL_PATH.exists():
        print(f"[assets] Downloading model from {HF_REPO_ID}...")
        hf_hub_download(
            repo_id=HF_REPO_ID,
            filename="impact_model.pkl",
            local_dir=str(MODEL_PATH.parent),
            repo_type="dataset",
        )
        print("[assets] Model ready.")
    else:
        print("[assets] Model already present — skipping.")


if __name__ == "__main__":
    download()
