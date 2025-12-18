"""
Authentication Module - Telegram Login
Admin: @Sir_NTRLI_II (ID: 8467779489)

ANDROID SAFE: Uses lazy imports to prevent crashes
"""
import json
from pathlib import Path
from typing import Dict, Optional

# Admin configuration
ADMIN_USERNAME = "@Sir_NTRLI_II"
ADMIN_ID = 8467779489

# Telegram API credentials (loaded from environment)
API_ID = 8546101037
API_HASH = "7defa4b44a90dd22ed93ec4bf36374d4"

SESSION_FILE = Path(__file__).parent.parent / "data" / "session.json"


class TelegramAuth:
    """Safe stub for Telegram authentication - Android compatible"""

    def __init__(self):
        self.session_data = self._load_session()
        self._client = None

    def _load_session(self) -> Dict:
        """Load saved session if exists"""
        if SESSION_FILE.exists():
            try:
                with open(SESSION_FILE, 'r') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_session(self, data: Dict):
        """Save session data"""
        SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(SESSION_FILE, 'w') as f:
            json.dump(data, f)

    def login(self) -> Dict:
        """
        Login stub - lazy loads Telethon only if available
        Returns status dict
        """
        print("TelegramAuth: Login initiated")

        # Check for existing session first
        if self.session_data.get('user_id'):
            return {
                'success': True,
                'user': self.get_user(),
                'message': 'Restored from session'
            }

        # Try to load Telethon (may not be available on Android)
        try:
            from telethon import TelegramClient
            print("TelegramAuth: Telethon available")
            return {
                'success': False,
                'pending': True,
                'message': 'Phone number required for login'
            }
        except ImportError:
            print("TelegramAuth: Running in stub mode (Telethon not available)")
            return {
                'success': False,
                'stub_mode': True,
                'message': 'Auth stub active - Telethon not available on this platform'
            }

    def check_session(self) -> bool:
        """Check if valid session exists"""
        return bool(self.session_data.get('user_id'))

    def get_user(self) -> Optional[Dict]:
        """Get current user from session"""
        if self.session_data.get('user_id'):
            return {
                'id': self.session_data['user_id'],
                'username': self.session_data.get('username'),
                'phone': self.session_data.get('phone'),
                'first_name': self.session_data.get('first_name'),
            }
        return None

    def is_admin(self, user: Optional[Dict] = None) -> bool:
        """Check if user is admin"""
        if user is None:
            user = self.get_user()
        if not user:
            return False
        return (
            user.get('id') == ADMIN_ID or
            user.get('username') == ADMIN_USERNAME or
            user.get('username') == ADMIN_USERNAME.lstrip('@')
        )

    def logout(self):
        """Logout and clear session"""
        self.session_data = {}
        if SESSION_FILE.exists():
            SESSION_FILE.unlink()
        print("TelegramAuth: Logged out")


# Alias for backward compatibility
AuthManager = TelegramAuth
