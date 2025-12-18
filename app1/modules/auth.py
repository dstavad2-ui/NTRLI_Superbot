"""
NTRLI SuperAPK - Authentication Module
Phase 1: Internal authentication (Telegram removed)
"""
import hashlib
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

AUTH_DB = "/sdcard/superapk_users.json"
SESSION_DB = "/sdcard/superapk_sessions.json"

class AuthManager:
    """Handles user authentication and session management"""
    
    def __init__(self, ai_console=None):
        self.ai_console = ai_console
        self.users = self._load_users()
        self.sessions = self._load_sessions()
        self._ensure_admin_user()
        self.log("AuthManager initialized")
    
    def log(self, msg, level="INFO"):
        if self.ai_console:
            self.ai_console.log(f"[AUTH] {msg}", level)
        else:
            print(f"[AUTH] {msg}")
    
    def _load_users(self):
        """Load user database"""
        try:
            if os.path.exists(AUTH_DB):
                with open(AUTH_DB, "r") as f:
                    return json.load(f)
            return {}
        except Exception as e:
            self.log(f"Error loading users: {e}", "ERROR")
            return {}
    
    def _save_users(self):
        """Save user database"""
        try:
            Path(AUTH_DB).parent.mkdir(parents=True, exist_ok=True)
            with open(AUTH_DB, "w") as f:
                json.dump(self.users, f, indent=2)
        except Exception as e:
            self.log(f"Error saving users: {e}", "ERROR")
    
    def _load_sessions(self):
        """Load session database"""
        try:
            if os.path.exists(SESSION_DB):
                with open(SESSION_DB, "r") as f:
                    return json.load(f)
            return {}
        except Exception as e:
            self.log(f"Error loading sessions: {e}", "ERROR")
            return {}
    
    def _save_sessions(self):
        """Save session database"""
        try:
            Path(SESSION_DB).parent.mkdir(parents=True, exist_ok=True)
            with open(SESSION_DB, "w") as f:
                json.dump(self.sessions, f, indent=2)
        except Exception as e:
            self.log(f"Error saving sessions: {e}", "ERROR")
    
    def _ensure_admin_user(self):
        """Ensure admin user @Sir_NTRLI_II exists"""
        admin_username = "Sir_NTRLI_II"
        if admin_username not in self.users:
            admin_pass = self._hash_password("NTRLI_ADMIN_2024")
            self.users[admin_username] = {
                "username": admin_username,
                "password_hash": admin_pass,
                "role": "admin",
                "created": datetime.now().isoformat(),
                "telegram_id": None
            }
            self._save_users()
            self.log(f"Admin user {admin_username} created")
    
    def _hash_password(self, password):
        """Hash password with SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username, password, telegram_id=None):
        """Register new user"""
        if username in self.users:
            self.log(f"Registration failed: {username} already exists", "WARNING")
            return False, "Username already exists"
        
        self.users[username] = {
            "username": username,
            "password_hash": self._hash_password(password),
            "role": "user",
            "created": datetime.now().isoformat(),
            "telegram_id": telegram_id
        }
        self._save_users()
        self.log(f"User registered: {username}")
        return True, "Registration successful"
    
    def login(self, username, password):
        """Login user and create session"""
        if username not in self.users:
            self.log(f"Login failed: {username} not found", "WARNING")
            return False, None, "Invalid credentials"
        
        user = self.users[username]
        password_hash = self._hash_password(password)
        
        if user["password_hash"] != password_hash:
            self.log(f"Login failed: Invalid password for {username}", "WARNING")
            return False, None, "Invalid credentials"
        
        # Create session
        session_token = hashlib.sha256(
            f"{username}{datetime.now().isoformat()}".encode()
        ).hexdigest()
        
        expires = (datetime.now() + timedelta(days=7)).isoformat()
        
        self.sessions[session_token] = {
            "username": username,
            "role": user["role"],
            "created": datetime.now().isoformat(),
            "expires": expires
        }
        self._save_sessions()
        
        self.log(f"User logged in: {username}")
        return True, session_token, "Login successful"
    
    def validate_session(self, session_token):
        """Validate session token"""
        if session_token not in self.sessions:
            return False, None
        
        session = self.sessions[session_token]
        expires = datetime.fromisoformat(session["expires"])
        
        if datetime.now() > expires:
            self.log(f"Session expired: {session_token[:16]}...", "WARNING")
            del self.sessions[session_token]
            self._save_sessions()
            return False, None
        
        return True, session
    
    def logout(self, session_token):
        """Logout user"""
        if session_token in self.sessions:
            username = self.sessions[session_token]["username"]
            del self.sessions[session_token]
            self._save_sessions()
            self.log(f"User logged out: {username}")
            return True
        return False
    
    def is_admin(self, session_token):
        """Check if session belongs to admin"""
        valid, session = self.validate_session(session_token)
        if valid and session["role"] == "admin":
            return True
        return False
    
    def get_user_info(self, session_token):
        """Get user info from session"""
        valid, session = self.validate_session(session_token)
        if valid:
            username = session["username"]
            return self.users.get(username)
        return None