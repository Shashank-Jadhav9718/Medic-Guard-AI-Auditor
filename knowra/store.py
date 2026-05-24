import chromadb

class KnowraStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./chroma_data")
        self.collection = self.client.get_or_create_collection(name="regulatory_rules")

    def add_documents(self, texts: list[str], ids: list[str]) -> None:
        self.collection.add(documents=texts, ids=ids)

    def query(self, text: str, n_results: int = 5) -> list[str]:
        results = self.collection.query(query_texts=[text], n_results=n_results)
        return results["documents"][0]

if __name__ == "__main__":
    store = KnowraStore()
    store.add_documents(["PII must be redacted before submission"], ["test-001"])
    results = store.query("PII redaction policy")
    assert len(results) > 0
    print("✅ ChromaDB working. Retrieved:", results[0][:60])
