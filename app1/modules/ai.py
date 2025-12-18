"""
NTRLI SuperAPK - AI Module
Phase 3: Claude + GPT-4 multi-model AI with logging
"""
import json
import os
from datetime import datetime
from pathlib import Path

# AI API keys - should be set via environment or config
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

AI_LOGS_DIR = "/sdcard/AI_consoles"

class AIManager:
    """Handles AI model interactions with Claude and GPT-4"""
    
    def __init__(self, ai_console=None):
        self.ai_console = ai_console
        self.anthropic_key = ANTHROPIC_API_KEY
        self.openai_key = OPENAI_API_KEY
        self.logs_dir = AI_LOGS_DIR
        self._ensure_logs_dir()
        self.conversation_history = []
        self.log("AIManager initialized")
        
        # Check API keys
        if not self.anthropic_key:
            self.log("WARNING: Anthropic API key not set", "WARNING")
        if not self.openai_key:
            self.log("WARNING: OpenAI API key not set", "WARNING")
    
    def log(self, msg, level="INFO"):
        if self.ai_console:
            self.ai_console.log(f"[AI] {msg}", level)
        else:
            print(f"[AI] {msg}")
    
    def _ensure_logs_dir(self):
        """Ensure AI logs directory exists"""
        try:
            Path(self.logs_dir).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            self.log(f"Error creating logs dir: {e}", "ERROR")
    
    def _log_interaction(self, model, prompt, response, metadata=None):
        """Log AI interaction to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"{self.logs_dir}/ai_interaction_{timestamp}.json"
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "model": model,
            "prompt": prompt,
            "response": response,
            "metadata": metadata or {}
        }
        
        try:
            with open(log_file, "w") as f:
                json.dump(log_entry, f, indent=2)
            self.log(f"Interaction logged: {log_file}")
        except Exception as e:
            self.log(f"Failed to log interaction: {e}", "ERROR")
    
    def query_claude(self, prompt, model="claude-sonnet-4-20250514", max_tokens=1000):
        """Query Claude API"""
        if not self.anthropic_key:
            self.log("Claude API key not configured", "ERROR")
            return None, "API key not configured"
        
        try:
            # Import here to avoid dependency issues if not installed
            from anthropic import Anthropic
            
            client = Anthropic(api_key=self.anthropic_key)
            
            self.log(f"Querying Claude: {model}")
            
            response = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            response_text = response.content[0].text
            
            # Log interaction
            self._log_interaction("claude", prompt, response_text, {
                "model": model,
                "max_tokens": max_tokens
            })
            
            # Add to conversation history
            self.conversation_history.append({
                "role": "user",
                "content": prompt,
                "model": "claude"
            })
            self.conversation_history.append({
                "role": "assistant",
                "content": response_text,
                "model": "claude"
            })
            
            self.log("Claude query successful")
            return response_text, None
        
        except Exception as e:
            self.log(f"Claude query failed: {e}", "ERROR")
            return None, str(e)
    
    def query_gpt4(self, prompt, model="gpt-4", max_tokens=1000):
        """Query GPT-4 API"""
        if not self.openai_key:
            self.log("OpenAI API key not configured", "ERROR")
            return None, "API key not configured"
        
        try:
            # Import here to avoid dependency issues if not installed
            from openai import OpenAI
            
            client = OpenAI(api_key=self.openai_key)
            
            self.log(f"Querying GPT-4: {model}")
            
            response = client.chat.completions.create(
                model=model,
                max_tokens=max_tokens,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            response_text = response.choices[0].message.content
            
            # Log interaction
            self._log_interaction("gpt4", prompt, response_text, {
                "model": model,
                "max_tokens": max_tokens
            })
            
            # Add to conversation history
            self.conversation_history.append({
                "role": "user",
                "content": prompt,
                "model": "gpt4"
            })
            self.conversation_history.append({
                "role": "assistant",
                "content": response_text,
                "model": "gpt4"
            })
            
            self.log("GPT-4 query successful")
            return response_text, None
        
        except Exception as e:
            self.log(f"GPT-4 query failed: {e}", "ERROR")
            return None, str(e)
    
    def query_multi_model(self, prompt, models=["claude", "gpt4"]):
        """Query multiple AI models and compare responses"""
        results = {}
        
        for model in models:
            if model == "claude":
                response, error = self.query_claude(prompt)
            elif model == "gpt4":
                response, error = self.query_gpt4(prompt)
            else:
                self.log(f"Unknown model: {model}", "WARNING")
                continue
            
            results[model] = {
                "response": response,
                "error": error
            }
        
        return results
    
    def analyze_sentiment(self, text):
        """Analyze sentiment using AI"""
        prompt = f"""Analyze the sentiment of the following text and respond with only one word: positive, negative, or neutral.

Text: {text}"""
        
        response, error = self.query_claude(prompt, max_tokens=10)
        if response:
            sentiment = response.strip().lower()
            self.log(f"Sentiment analysis: {sentiment}")
            return sentiment
        return "unknown"
    
    def summarize_text(self, text, max_length=100):
        """Summarize text using AI"""
        prompt = f"""Summarize the following text in {max_length} words or less:

{text}"""
        
        response, error = self.query_claude(prompt, max_tokens=max_length * 2)
        if response:
            self.log("Text summarized")
            return response
        return None
    
    def get_conversation_history(self, limit=10):
        """Get recent conversation history"""
        return self.conversation_history[-limit:]
    
    def clear_conversation_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        self.log("Conversation history cleared")
    
    def generate_business_insight(self, data):
        """Generate business insight from data"""
        prompt = f"""Analyze the following business data and provide key insights and recommendations:

{json.dumps(data, indent=2)}

Provide:
1. Key findings
2. Trends
3. Recommendations"""
        
        response, error = self.query_claude(prompt, max_tokens=1500)
        if response:
            self.log("Business insight generated")
            return response
        return None
    
    def get_ai_logs(self, limit=10):
        """Get recent AI interaction logs"""
        try:
            log_files = sorted(Path(self.logs_dir).glob("ai_interaction_*.json"), reverse=True)
            logs = []
            
            for log_file in log_files[:limit]:
                with open(log_file, "r") as f:
                    logs.append(json.load(f))
            
            return logs
        except Exception as e:
            self.log(f"Error reading logs: {e}", "ERROR")
            return []