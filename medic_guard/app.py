import streamlit as st
import httpx, fitz, json

st.set_page_config(page_title="Medic-Guard Auditor", layout="centered",
                   initial_sidebar_state="collapsed")

st.title("🛡️ Medic-Guard AI Auditor")
st.caption("Upload a medical product PDF to run an autonomous compliance audit.")

API_URL = "http://localhost:8000/audit"

uploaded = st.file_uploader("Upload product documentation (PDF)", type=["pdf"])

if uploaded:
    with st.spinner("Extracting text from PDF..."):
        doc = fitz.open(stream=uploaded.read(), filetype="pdf")
        text = "\n".join(page.get_text() for page in doc)
    st.info(f"Extracted {len(text)} characters from {len(doc)} pages.")

    if st.button("▶ Run Compliance Audit"):
        with st.spinner("Running audit pipeline..."):
            try:
                resp = httpx.post(API_URL, json={"document_text": text}, timeout=60)
                result = resp.json()
            except Exception as e:
                st.error(f"API error: {e}")
                st.stop()

        status = result.get("audit_status", "UNKNOWN")
        score = result.get("confidence_score", 0.0)

        if status == "PASSED":
            st.success("✅  PASSED — Document meets compliance requirements.")
        else:
            st.error("🚨  FLAGGED — Compliance issues detected.")

        st.metric("Confidence Score", f"{score:.0%}")
        st.progress(score)

        with st.expander("📋 Rule References"):
            refs = result.get("rule_references", [])
            if refs:
                for r in refs:
                    st.markdown(f"- {r}")
            else:
                st.write("No specific rules cited.")

        if status == "FLAGGED" and result.get("remediation"):
            st.warning("**Recommended Remediation:**\n\n" + result["remediation"])

        if result.get("error"):
            st.error("Pipeline error: " + result["error"])
