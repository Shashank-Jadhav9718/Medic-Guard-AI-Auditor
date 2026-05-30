from medic_guard.state import AuditState
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from medic_guard.config import load_config
import json
import re


def reporter_node(state: AuditState) -> AuditState:
    if state.get("error"):
        state["audit_status"] = "FLAGGED"
        return state
    cfg = load_config()
    model_name = cfg["MODEL_NAME"]
    if "gemini" in model_name.lower():
        llm = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=cfg["GOOGLE_API_KEY"] or cfg["GEMINI_API_KEY"],
            temperature=0.0,
        )
    else:
        llm = ChatOpenAI(
            model=model_name, api_key=cfg["OPENAI_API_KEY"], temperature=0.0
        )
    rules_text = "\n".join(f"- {r[:200]}" for r in state["retrieved_rules"])
    prompt = (
        "You are a medical compliance auditor. Given a product document and regulatory rules, "
        "respond ONLY with a JSON object (no markdown, no explanation) with keys:\n"
        '  "audit_status": "PASSED" or "FLAGGED"\n'
        '  "rule_references": [list of short rule citations used]\n'
        '  "remediation": "empty string if PASSED, corrective action string if FLAGGED"\n\n'
        f"Document:\n{state['document_text'][:600]}\n\nRules:\n{rules_text}"
    )
    response = llm.invoke(prompt)
    try:
        clean = re.sub(r"```json|```", "", response.content).strip()
        data = json.loads(clean)
        state["audit_status"] = data.get("audit_status", "FLAGGED")
        state["rule_references"] = data.get("rule_references", [])
        state["remediation"] = data.get("remediation", "")
    except Exception as e:
        state["error"] = f"Reporter parse error: {e}"
        state["audit_status"] = "FLAGGED"
    return state


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win"):
        sys.stdout.reconfigure(encoding="utf-8")
    from medic_guard.state import AuditState

    mock_state: AuditState = {
        "document_text": "Product: Ibuprofen 200mg. All labeling requirements met.",
        "retrieved_rules": ["Ingredient list must appear in descending order."],
        "retry_count": 0,
        "validation_passed": True,
        "confidence_score": 0.8,
        "audit_status": "PENDING",
        "rule_references": [],
        "remediation": "",
        "error": "",
    }
    result = reporter_node(mock_state)
    assert result["audit_status"] in ("PASSED", "FLAGGED")
    print(f"✅ Reporter Node: status={result['audit_status']}")
    print(f"   References: {result['rule_references']}")
    print(f"   Remediation: {result['remediation'][:80] or '(none)'}")
