from medic_guard.state import AuditState
from knowra.retriever import retrieve_rules

def auditor_node(state: AuditState) -> AuditState:
    """Queries Knowra with the document text and stores retrieved rules."""
    try:
        query = state["document_text"][:500]  # Use first 500 chars as query
        rules = retrieve_rules(query, top_k=5)
        state["retrieved_rules"] = rules
    except Exception as e:
        state["error"] = f"Auditor error: {str(e)}"
    return state

if __name__ == "__main__":
    from medic_guard.state import empty_state
    test_state = empty_state("Product label: Paracetamol 500mg tablets. Contains paracetamol.")
    result = auditor_node(test_state)
    assert len(result["retrieved_rules"]) > 0, "No rules retrieved — check Knowra ingestion"
    print(f"[OK] Auditor Node: retrieved {len(result['retrieved_rules'])} rules.")
    print("  First rule preview:", result["retrieved_rules"][0][:80])
