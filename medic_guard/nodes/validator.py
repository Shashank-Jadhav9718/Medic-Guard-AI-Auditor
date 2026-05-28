import re
from medic_guard.state import AuditState
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from medic_guard.config import load_config

def validator_node(state: AuditState) -> AuditState:
    """
    CRAG: Scores relevance of each retrieved rule against the document.
    If mean score < 0.5, sets validation_passed=False for retry.
    """
    if state.get("error"):
        return state
    cfg = load_config()
    
    model_name = cfg["MODEL_NAME"]
    if "gemini" in model_name.lower():
        llm = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=cfg["GOOGLE_API_KEY"] or cfg["GEMINI_API_KEY"],
            temperature=0.0
        )
    else:
        llm = ChatOpenAI(
            model=model_name,
            api_key=cfg["OPENAI_API_KEY"],
            temperature=0.0
        )
        
    doc_text = str(state.get("document_text", ""))[:300]
    retrieved_rules = state.get("retrieved_rules", [])
    
    scores = []
    for rule in retrieved_rules:
        rule_str = str(rule)[:300]
        prompt = (
            f"Rate how relevant this rule is to the document on a scale of 0 to 1. "
            f"Reply with ONLY a number between 0 and 1, nothing else.\n\n"
            f"Document: {doc_text}\n\nRule: {rule_str}"
        )
        try:
            response = llm.invoke(prompt)
            content = response.content.strip()
            # Extract first number (float or integer) using regex
            match = re.search(r"[+-]?\d*\.?\d+", content)
            if match:
                score = float(match.group())
            else:
                score = 0.0
            scores.append(max(0.0, min(1.0, score)))
        except Exception:
            scores.append(0.0)
            
    mean_score = sum(scores) / len(scores) if scores else 0.0
    state["confidence_score"] = round(mean_score, 3)
    state["validation_passed"] = mean_score >= 0.5
    return state

if __name__ == "__main__":
    from medic_guard.state import AuditState
    mock_state: AuditState = {
        "document_text": "Product: Ibuprofen 200mg. Ingredients listed in descending order.",
        "retrieved_rules": ["Ingredient list must appear in descending order of predominance."],
        "retry_count": 0, "validation_passed": False, "confidence_score": 0.0,
        "audit_status": "PENDING", "rule_references": [], "remediation": "", "error": ""
    }
    result = validator_node(mock_state)
    assert 0.0 <= result["confidence_score"] <= 1.0
    print(f"[OK] Validator Node: score={result['confidence_score']}, passed={result['validation_passed']}")
