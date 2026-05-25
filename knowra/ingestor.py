from knowra.store import KnowraStore
import os

def chunk_text(text: str, size: int = 500, overlap: int = 50) -> list[str]:
    chunks, start = [], 0
    while start < len(text):
        chunks.append(text[start:start + size])
        start += size - overlap
    return chunks

def ingest_regulatory_docs(folder_path: str = "knowra/regulatory_docs") -> int:
    store = KnowraStore()
    total = 0
    for fname in os.listdir(folder_path):
        if not fname.endswith(".txt"):
            continue
        with open(os.path.join(folder_path, fname)) as f:
            text = f.read()
        chunks = chunk_text(text)
        ids = [f"{fname}-chunk-{i}" for i in range(len(chunks))]
        store.add_documents(chunks, ids)
        total += len(chunks)
        print(f"  Ingested {len(chunks)} chunks from {fname}")
    print(f"✅ Total chunks ingested: {total}")
    return total

if __name__ == "__main__":
    count = ingest_regulatory_docs()
    assert count >= 0
    print("✅ Ingestor ready. Chunks:", count)
