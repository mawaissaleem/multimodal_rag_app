from embedder import Embedder


def main():
    model_name = "all-MiniLM-L6-v2"
    embedder = Embedder(model_name=model_name)

    texts = [
        "The quick brown fox jumps over the lazy dog.",
        "Artificial intelligence is transforming industries.",
        "The capital of France is Paris.",
        "Cats are often more independent than dogs.",
    ]

    embeddings = embedder.encode(texts)

    print(f"\nGenerated {len(embeddings)} embeddings of shape {embeddings.shape}.\n")
    for i, emb in enumerate(embeddings):
        print(f"Sentence {i+1}: '{texts[i]}'")
        print(f"Embedding (first 5 values): {emb[:5]}\n")


if __name__ == "__main__":
    main()
