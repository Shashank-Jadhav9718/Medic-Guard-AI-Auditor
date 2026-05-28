from typing import TypedDict

class AuditState(TypedDict):
    document_text: str       # Raw text extracted from uploaded PDF
    retrieved_rules: list    # Rule chunks from Knowra
    retry_count: int         # CRAG fallback counter (max 1)
    validation_passed: bool  # Set by Validator Node
    confidence_score: float  # 0.0 – 1.0 from CRAG scoring
    audit_status: str        # "PASSED" | "FLAGGED" | "PENDING"
    rule_references: list    # Rule citations used in decision
    remediation: str         # Suggested correction if FLAGGED
    error: str               # Error message if any node fails

def empty_state(document_text: str) -> AuditState:
    return AuditState(
        document_text=document_text,
        retrieved_rules=[],
        retry_count=0,
        validation_passed=False,
        confidence_score=0.0,
        audit_status="PENDING",
        rule_references=[],
        remediation="",
        error="",
    )

if __name__ == "__main__":
    s = empty_state("Test product label text.")
    assert s["audit_status"] == "PENDING"
    assert s["retry_count"] == 0
    print("[OK] AuditState schema valid:", list(s.keys()))
