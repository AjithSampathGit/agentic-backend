# agentic_backend/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import random
import os
import openai
from pydantic import BaseModel

app = FastAPI()

# CORS middleware to allow frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")

# --- Models ---
class SessionData(BaseModel):
    customer_id: str
    step: str
    inactivity_minutes: int

# --- Drop-off Detection ---
def is_likely_to_drop_off(session: SessionData) -> bool:
    return session.inactivity_minutes >= 1 and session.step == "upload_docs"

# --- GPT Help Agent ---
def get_ai_help(step: str) -> str:
    try:
        prompt = f"The customer is stuck on '{step}'. Provide short, helpful guidance."
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return "Sorry, I'm currently unavailable. Please try again later."

# --- Live Agent ---
def escalate_to_agent(customer_id: str) -> str:
    return f"A live agent will join shortly for customer {customer_id}."

# --- Save & Schedule ---
def save_and_schedule(customer_id: str) -> str:
    return f"Progress saved for {customer_id}. Appointment scheduled for tomorrow at 10 AM."

# --- Intervention Decision ---
@app.post("/intervene")
async def intervene(session: SessionData):
    if not is_likely_to_drop_off(session):
        return {"action": "none", "message": "No intervention needed."}

    action = random.choice(["help", "agent", "save_schedule"])

    if action == "help":
        return {"action": "help", "message": get_ai_help(session.step)}
    elif action == "agent":
        return {"action": "agent", "message": escalate_to_agent(session.customer_id)}
    else:
        return {"action": "save_schedule", "message": save_and_schedule(session.customer_id)}
