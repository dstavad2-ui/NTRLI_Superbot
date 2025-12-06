# ============================================================
# NTRLI' AI — Backend Engine (FastAPI)
# Hybrid Local/Remote AI + Work Modes + Self-Healing
# ============================================================

import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel

MODEL_MODE = "remote"  # "local" or "remote"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

app = FastAPI(title="NTRLI AI Backend", version="1.0")

def self_heal(error_msg):
    print("\n[SELF-HEAL TRIGGERED]")
    print("Reason:", error_msg)
    print("Recalibrating...\n")
    try:
        global MODEL_MODE
        MODEL_MODE = "local" if MODEL_MODE == "remote" else "remote"
        print("[SELF-HEAL] Mode switched to:", MODEL_MODE)
    except:
        print("[SELF-HEAL FAILSAFE] unable to toggle modes")

class ChatRequest(BaseModel):
    message: str
    mode: str = "default"

def local_llm(prompt):
    return f"[LOCAL MODEL RESPONSE] {prompt}"

def remote_llm(prompt: str):
    try:
        if OPENAI_API_KEY == "":
            raise RuntimeError("OpenAI API key missing")
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
        data = {
            "model": "gpt-4.1-mini",
            "messages": [
                {"role": "system", "content": "You are NTRLI' AI — pragmatic, loyal, structured."},
                {"role": "user", "content": prompt}
            ]
        }
        r = requests.post(
            "https://api.openai.com/v1/chat/completions",
            json=data,
            headers=headers,
            timeout=10
        )
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        else:
            raise RuntimeError(f"OpenAI API error: {r.text}")
    except Exception as e:
        self_heal(str(e))
        return local_llm(prompt)

@app.get("/api/health")
def health():
    return {"status": "ok", "mode": MODEL_MODE}

@app.post("/api/chat")
def chat(data: ChatRequest):
    prompt = f"[MODE: {data.mode}] {data.message}"
    try:
        if MODEL_MODE == "remote":
            return {"response": remote_llm(prompt)}
        else:
            return {"response": local_llm(prompt)}
    except Exception as e:
        self_heal(str(e))
        fallback = local_llm(prompt)
        return {"response": fallback}

@app.get("/api/mode/{task}")
def work_mode(task: str):
    modes = {
        "focus": "High concentration mode activated.",
        "tg_boutique": "Telegram boutique work mode enabled.",
        "graphics": "Graphics creation mode enabled.",
        "batch": "Batch-production mode operational.",
        "analysis": "Deep analysis mode active."
    }
    return {"status": "ok", "task": task, "message": modes.get(task, "Unknown mode")}

print("""
===========================================
      N T R L I '   B A C K E N D
===========================================
Running at: http://localhost:8000
Use Ctrl+C to stop.
""")
