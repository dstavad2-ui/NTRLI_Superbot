# NTRLI' AI - Master Script 
import os, json, requests
from bs4 import BeautifulSoup

OFFLINE_CACHE_FILE = "offline_cache.json"
CHAT_CACHE_FILE = "ai_chat_memory.json"

OFFLINE_KNOWLEDGE = []
CHAT_MEMORY = []

# ---------------------------------------------------
# Load Offline Knowledge Cache
# ---------------------------------------------------
def load_offline():
    global OFFLINE_KNOWLEDGE
    if os.path.exists(OFFLINE_CACHE_FILE):
        for line in open(OFFLINE_CACHE_FILE, "r", encoding="utf-8"):
            try:
                OFFLINE_KNOWLEDGE.append(json.loads(line))
            except:
                pass
    return OFFLINE_KNOWLEDGE

load_offline()

# ---------------------------------------------------
# Chat Memory Persistence
# ---------------------------------------------------
def load_chat_memory():
    global CHAT_MEMORY
    if os.path.exists(CHAT_CACHE_FILE):
        try:
            CHAT_MEMORY = json.load(open(CHAT_CACHE_FILE, "r", encoding="utf-8"))
        except:
            CHAT_MEMORY = []
    return CHAT_MEMORY

def save_chat_memory():
    with open(CHAT_CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(CHAT_MEMORY, f, indent=2, ensure_ascii=False)

load_chat_memory()

# ---------------------------------------------------
#  Store new knowledge
# ---------------------------------------------------
def store_knowledge(key, value):
    with open(OFFLINE_CACHE_FILE, "a", encoding="utf-8") as f:
        json.dump({key: value}, f)
        f.write("\n")

# ---------------------------------------------------
#  Self-Healing
# ---------------------------------------------------
def self_heal(reason, exc=None):
    print(f"[SELF_HEAL] {reason}")
    load_offline()

# ---------------------------------------------------
#  Internet Fetch + Parsing
# ---------------------------------------------------
def fetch_live(url):
    try:
        html = requests.get(url, timeout=6).text
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(separator="\n")
        return text
    except Exception as e:
        self_heal(f"Live fetch failed: {e}")
        return None

# ---------------------------------------------------
# TTS Output
# ---------------------------------------------------
try:
    import pyttsx3
    engine = pyttsx3.init()
    def speak(text):
        engine.say(text)
        engine.runAndWait()
except:
    def speak(text):
        print(f"[TTS] {text}")

# ---------------------------------------------------
# AI Processing (Single Response)
# ---------------------------------------------------
def ai_process(user_input):
    try:
        response = f"NTRLI’ AI: '{user_input}' forstået."
        store_knowledge("user_input", user_input)
        speak(response)
        return response
    except Exception as e:
        self_heal("Runtime error", e)
        return "⚠️ AI fejl – systemet heler."

# ---------------------------------------------------
# Chat Mode (Persistent Conversation)
# ---------------------------------------------------
def ai_chat(user_input):
    CHAT_MEMORY.append({"user": user_input})
    response = f"🧠 NTRLI’ AI (chat): Jeg forstår '{user_input}'."

    CHAT_MEMORY.append({"assistant": response})
    save_chat_memory()

    speak(response)
    return response

# ---------------------------------------------------
# Debug Function
# ---------------------------------------------------
def ai_debug():
    return {
        "offline_memory_items": len(OFFLINE_KNOWLEDGE),
        "chat_memory_items": len(CHAT_MEMORY),
        "sample_chat": CHAT_MEMORY[-5:],
    }
