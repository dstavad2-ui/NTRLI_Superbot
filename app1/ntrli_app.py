"""
NTRLI' AI - Application Entry Point
Unified AI API System with Admin/User Separation

Usage:
    # For Admin (full access):
    from app1 import AdminController
    admin = AdminController(admin_id=8467779489)
    admin.verify_admin(8467779489)
    response = await admin.query_admin_ai("Your query here")

    # For Users (restricted access):
    from app1 import UserController
    user = UserController(user_id=12345, username="customer")
    response = await user.query("Your query here")

    # Direct engine access:
    from app1 import NTRLIAIEngine
    engine = NTRLIAIEngine(is_admin=False)
    response = await engine.query("Your query here")
"""

import asyncio
import logging
from typing import Optional

from .core.ntrli_ai_engine import NTRLIAIEngine, SynthesizedResponse
from .core.ai_selector import AISelector, TaskType
from .admin_panel.admin_controller import AdminController
from .user_interface.user_controller import UserController
from .config.api_config import APIConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("NTRLI_AI")


class NTRLIApp:
    """
    Main NTRLI' AI Application

    This class provides a unified interface for both admin and user access.
    """

    def __init__(self):
        self.config = APIConfig()
        self._admin_controller: Optional[AdminController] = None
        self._user_controllers: dict = {}
        logger.info("NTRLI' AI App initialized")

    def get_admin_controller(self, admin_id: int) -> AdminController:
        """
        Get or create an AdminController for an admin user.

        Args:
            admin_id: The admin's user ID

        Returns:
            AdminController instance (must call verify_admin before use)
        """
        if self._admin_controller is None:
            self._admin_controller = AdminController(admin_id)
        return self._admin_controller

    def get_user_controller(self, user_id: int, username: str = None) -> UserController:
        """
        Get or create a UserController for a user.

        Args:
            user_id: The user's ID
            username: Optional username

        Returns:
            UserController instance
        """
        if user_id not in self._user_controllers:
            self._user_controllers[user_id] = UserController(user_id, username)
        return self._user_controllers[user_id]

    async def quick_query(self, prompt: str, user_id: int = None,
                          is_admin: bool = False) -> SynthesizedResponse:
        """
        Quick query without creating a full controller.

        Args:
            prompt: The query
            user_id: Optional user ID for tracking
            is_admin: Whether to use admin-level access

        Returns:
            SynthesizedResponse
        """
        engine = NTRLIAIEngine(is_admin=is_admin)
        return await engine.query(prompt)

    def list_available_apis(self, is_admin: bool = False) -> list:
        """List all available APIs based on access level"""
        if is_admin:
            return list(self.config.get_all_apis_for_admin().keys())
        return list(self.config.get_all_apis_for_user().keys())


# Convenience function for quick access
async def ntrli_query(prompt: str, is_admin: bool = False) -> str:
    """
    Quick NTRLI' AI query function.

    Args:
        prompt: Your question or request
        is_admin: Use admin-level access

    Returns:
        AI response as string
    """
    engine = NTRLIAIEngine(is_admin=is_admin)
    response = await engine.query(prompt)
    return response.content


# Demo/Test function
async def demo():
    """Demonstration of NTRLI' AI capabilities"""
    print("=" * 60)
    print("NTRLI' AI - Demonstration")
    print("=" * 60)

    # Show available APIs
    config = APIConfig()

    print("\n--- ADMIN APIs (Admin Panel Only) ---")
    for name, cfg in config.get_admin_apis().items():
        print(f"  {name}")
        print(f"    Provider: {cfg.provider}")
        print(f"    Owner: {cfg.owner}")
        print(f"    Capabilities: {', '.join(cfg.capabilities[:3])}...")

    print("\n--- USER APIs (For Customers) ---")
    for name, cfg in config.get_user_apis().items():
        print(f"  {name}")
        print(f"    Provider: {cfg.provider}")
        print(f"    Owner: {cfg.owner}")
        print(f"    Capabilities: {', '.join(cfg.capabilities[:3])}...")

    print("\n--- GENERAL APIs (Both) ---")
    for name, cfg in config.get_general_apis().items():
        print(f"  {name}")
        print(f"    Provider: {cfg.provider}")
        print(f"    Owner: {cfg.owner}")
        print(f"    Capabilities: {', '.join(cfg.capabilities[:3])}...")

    print("\n" + "=" * 60)
    print("NTRLI' AI is ready!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(demo())
