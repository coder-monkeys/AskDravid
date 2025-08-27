import json
from typing import List, Dict, Any
from transformers import AutoTokenizer
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


# -------------------------------
# STEP 1: Load the transcript
# -------------------------------
def load_transcript(file_path: str) -> List[Dict[str, Any]]:
    """
    Loads the cleaned transcript JSON file.
    Each entry has 'id', 'text', 'start', 'end'.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        transcript = json.load(f)
    return transcript


# -------------------------------
# STEP 2: Chunk the transcript
# -------------------------------
def chunk_transcript(
        transcript: List[Dict[str, Any]],
        tokenizer: AutoTokenizer,
        chunk_size: int = 200,
        overlap: int = 50
) -> List[Dict[str, Any]]:
    """
    Splits transcript text into chunks of approximately `chunk_size` tokens
    using the Hugging Face tokenizer. Optional overlap can help with context.
    Returns a list of chunks with text and metadata.
    """
    chunks = []
    for entry in transcript:
        text = entry["text"]
        start_time = entry["start"]
        end_time = entry["end"]

        # Encode text into tokens
        tokens = tokenizer.encode(text, add_special_tokens=False)
        i = 0
        while i < len(tokens):
            chunk_tokens = tokens[i:i + chunk_size]
            chunk_text = tokenizer.decode(chunk_tokens)
            chunks.append({
                "text": chunk_text,
                "start": start_time,
                "end": end_time
            })
            i += chunk_size - overlap  # move by chunk_size minus overlap
    return chunks


# -------------------------------
# STEP 3: Generate embeddings
# -------------------------------
def embed_chunks(chunks: List[Dict[str, Any]], model_name="sentence-transformers/all-MiniLM-L6-v2"):
    """
    Generates embeddings for each chunk using Sentence Transformers.
    Returns numpy array of embeddings and list of chunk metadata.
    """
    model = SentenceTransformer(model_name)
    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings, chunks


# -------------------------------
# STEP 4: Create FAISS vector store
# -------------------------------
def create_faiss_index(embeddings: np.ndarray):
    """
    Creates a FAISS index from the embeddings.
    """
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)  # L2 distance metric
    index.add(embeddings)
    return index


# -------------------------------
# STEP 5: Query the vector store
# -------------------------------
def query_index(
        question: str,
        index: faiss.IndexFlatL2,
        chunks: List[Dict[str, Any]],
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        top_k=5
):
    """
    Query the FAISS vector store with a question.
    Returns top-k most relevant transcript chunks with timestamps.
    """
    model = SentenceTransformer(model_name)
    query_embedding = model.encode([question], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, top_k)

    results = []
    for idx in indices[0]:
        results.append(chunks[idx])
    return results