from transformers import AutoTokenizer
from vectorize_utils import load_transcript, chunk_transcript, embed_chunks, create_faiss_index, query_index


def main():
    # Load transcript
    transcript = load_transcript("transcript.json")

    # Initialize tokenizer
    tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

    # Chunk transcript
    chunks = chunk_transcript(transcript, tokenizer, chunk_size=200, overlap=50)

    # Generate embeddings
    embeddings, chunks = embed_chunks(chunks)

    # Create FAISS index
    index = create_faiss_index(embeddings)

    # Example query
    question = "I love future bread"
    top_chunks = query_index(question, index, chunks, top_k=3)

    for c in top_chunks:
        print(f"Text: {c['text']}, Start: {c['start']}, End: {c['end']}")


if __name__ == "__main__":
    main()
