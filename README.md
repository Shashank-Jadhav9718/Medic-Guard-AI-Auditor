## Quick Start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your OPENAI_API_KEY
python knowra/ingestor.py
uvicorn medic_guard.api:app --reload --port 8000 &
streamlit run medic_guard/app.py
```

## Streamlit Cloud Deployment
1. Push repo to GitHub (chroma_data/ and .env are gitignored)
2. Connect repo at share.streamlit.io
3. Add Gemini_API_KEY in Settings → Secrets Manager
4. Set main file path: medic_guard/app.py

## Standard Operating Procedure (SOP)
Medic-Guard AI Auditor is an automated system designed to check medical documents against FDA and EMA guidelines. It uses LangGraph for structured auditing, Knowra for regulatory document ingestion and retrieval, and Streamlit for the frontend UI.
