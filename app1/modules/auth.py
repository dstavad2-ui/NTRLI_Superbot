"""
Authentication Module - Telegram Login Only
Admin: @Sir_NTRLI_II (ID: 8467779489)
"""
import json
import asyncio
from pathlib import Path
from typing import Dict, Optional
from telethon import TelegramClient
from telethon.sessions import StringSession

# Admin configuration
ADMIN_USERNAME = "@Sir_NTRLI_II"
ADMIN_ID = 8467779489

# Telegram API credentials (loaded from environment)
API_ID = 8546101037
API_HASH = "7defa4b44a90dd22ed93ec4bf36374d4"

SESSION_FILE = Path(__file__).parent.parent / "data" / "session.json"


class AuthManager:
    """Handles Telegram authentication"""

    def __init__(self):
        self.client: Optional[TelegramClient] = None
        self.current_user = None
        self.session_data = self.load_session()

    def load_session(self) -> Dict:
        """Load saved session if exists"""
        if SESSION_FILE.exists():
            try:
                with open(SESSION_FILE, 'r') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def save_session(self, data: Dict):
        """Save session data"""
        SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(SESSION_FILE, 'w') as f:
            json.dump(data, f)

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

    def is_admin(self, user: Optional[Dict]) -> bool:
        """Check if user is admin"""
        if not user:
            return False
        # Check by user ID or username
        return (
            user.get('id') == ADMIN_ID or
            user.get('username') == ADMIN_USERNAME or
            user.get('username') == ADMIN_USERNAME.lstrip('@')
        )

    def telegram_login(self, phone: str) -> Dict:
        """
        Login via Telegram
        Returns: {'success': bool, 'user': dict, 'error': str}
        """
        try:
            # Create event loop for async operation
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self._async_login(phone))
            loop.close()
            return result
        except Exception as e:
            return {'success': False, 'error': str(e)}

    async def _async_login(self, phone: str) -> Dict:
        """Async Telegram login"""
        try:
            # Create Telegram client
            self.client = TelegramClient(
                StringSession(),
                API_ID,
                API_HASH
            )

            await self.client.connect()

            # Send code request
            await self.client.send_code_request(phone)

            # Note: In production, you'll need to get code from user
            # For now, return pending status
            return {
                'success': False,
                'pending_code': True,
                'phone': phone,
                'error': 'Please implement code verification UI'
            }

            # After code verification:
            # await self.client.sign_in(phone, code)
            # me = await self.client.get_me()
            #
            # user_data = {
            #     'id': me.id,
            #     'username': me.username,
            #     'phone': me.phone,
            #     'first_name': me.first_name,
            # }
            #
            # # Save session
            # self.session_data = user_data
            # self.save_session(user_data)
            # self.current_user = user_data
            #
            # return {'success': True, 'user': user_data}

        except Exception as e:
            return {'success': False, 'error': str(e)}

    def verify_code(self, phone: str, code: str) -> Dict:
        """Verify login code"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self._async_verify(phone, code))
            loop.close()
            return result
        except Exception as e:
            return {'success': False, 'error': str(e)}

    async def _async_verify(self, phone: str, code: str) -> Dict:
        """Async code verification"""
        try:
            if not self.client:
                return {'success': False, 'error': 'No active login session'}

            await self.client.sign_in(phone, code)
            me = await self.client.get_me()

            user_data = {
                'id': me.id,
                'username': me.username,
                'phone': me.phone,
                'first_name': me.first_name,
                'session_string': self.client.session.save()
            }

            # Save session
            self.session_data = user_data
            self.save_session(user_data)
            self.current_user = user_data

            return {'success': True, 'user': user_data}

        except Exception as e:
            return {'success': False, 'error': str(e)}

    def logout(self):
        """Logout and clear session"""
        self.session_data = {}
        self.current_user = None
        if SESSION_FILE.exists():
            SESSION_FILE.unlink()

        if self.client:
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.client.disconnect())
                loop.close()
            except Exception:
                pass
