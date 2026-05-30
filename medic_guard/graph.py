from langgraph.graph import StateGraph, END
from medic_guard.state import AuditState
from medic_guard.nodes.auditor import auditor_node
from medic_guard.nodes.validator import validator_node
from medic_guard.nodes.reporter import reporter_node

MAX_RETRIES = 1

def route_after_validation(state: AuditState) -> str:
    if not state["validation_passed"] and state["retry_count"] < MAX_RETRIES:
        state["retry_count"] += 1
        return "auditor"   # CRAG fallback: re-query Knowra
    return "reporter"

builder = StateGraph(AuditState)
builder.add_node("auditor", auditor_node)
builder.add_node("validator", validator_node)
builder.add_node("reporter", reporter_node)

builder.set_entry_point("auditor")
builder.add_edge("auditor", "validator")
builder.add_conditional_edges("validator", route_after_validation, {
    "auditor": "auditor",
    "reporter": "reporter",
})
builder.add_edge("reporter", END)

audit_graph = builder.compile()

if __name__ == "__main__":
    import sys
    if sys.platform.startswith("win"):
        sys.stdout.reconfigure(encoding="utf-8")
    from medic_guard.state import empty_state
    state = empty_state("Paracetamol 500mg. Ingredients: Paracetamol, Microcrystalline Cellulose.")
    result = audit_graph.invoke(state)
    assert result["audit_status"] in ("PASSED", "FLAGGED")
    print("✅ Graph assembled and executed.")
    print(f"   Status: {result['audit_status']}")
    print(f"   Confidence: {result['confidence_score']}")
    print(f"   Retries used: {result['retry_count']}")
