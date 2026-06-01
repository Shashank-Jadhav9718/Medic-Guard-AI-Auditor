from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from medic_guard.graph import audit_graph
from medic_guard.state import empty_state

app = FastAPI(title="Medic-Guard API", version="1.0.0")

class AuditRequest(BaseModel):
    document_text: str

class AuditResponse(BaseModel):
    audit_status: str
    confidence_score: float
    rule_references: list
    remediation: str
    error: str

@app.get("/health")
def health():
    return {"status": "ok", "service": "medic-guard"}

@app.post("/audit", response_model=AuditResponse)
async def audit(request: AuditRequest):
    if not request.document_text.strip():
        raise HTTPException(status_code=400, detail="document_text cannot be empty")
    state = empty_state(request.document_text)
    result = audit_graph.invoke(state)
    return AuditResponse(
        audit_status=result["audit_status"],
        confidence_score=result["confidence_score"],
        rule_references=result["rule_references"],
        remediation=result["remediation"],
        error=result["error"],
    )
