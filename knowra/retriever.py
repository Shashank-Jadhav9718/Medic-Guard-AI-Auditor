from knowra.store import KnowraStore

def retrieve_rules(query: str, top_k: int = 5) -> list[str]:
    """Public API for Medic-Guard to call. Returns top_k rule chunks."""
    store = KnowraStore()
    return store.query(query, n_results=top_k)

if __name__ == "__main__":
    results = retrieve_rules("product labeling requirements", top_k=3)
    assert len(results) > 0, "No results — did you run ingestor.py first?"
    for i, r in enumerate(results, 1):
        print(f"Result {i}: {r[:80]}...")
    print("✅ Retriever working.")
