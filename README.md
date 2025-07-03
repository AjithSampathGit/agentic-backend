# Agentic AI Backend (FastAPI)

This is the backend service that powers the agentic AI intervention system for detecting drop-off in a digital account opening flow.

### 🔧 Requirements

- Python 3.9+
- OpenAI API key

### 🚀 Running Locally

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=your_key_here
uvicorn main:app --reload
