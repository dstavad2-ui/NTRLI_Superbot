"""
NTRLI' AI - App1 Module
AI API Selection System with Admin/User Separation
"""

from .core.ntrli_ai_engine import NTRLIAIEngine
from .core.ai_selector import AISelector
from .admin_panel.admin_controller import AdminController
from .user_interface.user_controller import UserController

__version__ = "1.0.0"
__author__ = "NTRLI"

__all__ = [
    "NTRLIAIEngine",
    "AISelector",
    "AdminController",
    "UserController"
]
