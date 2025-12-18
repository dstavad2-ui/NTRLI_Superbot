"""
NTRLI SuperAPK - Admin Module
Phase 3: Admin panel for @Sir_NTRLI_II
"""
import json
import os
from datetime import datetime
from pathlib import Path

ADMIN_LOGS = "/sdcard/superapk_admin_logs.json"

class AdminManager:
    """Handles admin operations and monitoring"""
    
    ADMIN_USERNAME = "Sir_NTRLI_II"
    
    def __init__(self, ai_console=None, auth_manager=None, ecommerce_manager=None, news_manager=None, ai_manager=None):
        self.ai_console = ai_console
        self.auth_manager = auth_manager
        self.ecommerce_manager = ecommerce_manager
        self.news_manager = news_manager
        self.ai_manager = ai_manager
        self.admin_logs = self._load_admin_logs()
        self.log("AdminManager initialized")
    
    def log(self, msg, level="INFO"):
        if self.ai_console:
            self.ai_console.log(f"[ADMIN] {msg}", level)
        else:
            print(f"[ADMIN] {msg}")
        
        # Also log to admin logs
        self._add_admin_log(msg, level)
    
    def _load_admin_logs(self):
        """Load admin logs"""
        try:
            if os.path.exists(ADMIN_LOGS):
                with open(ADMIN_LOGS, "r") as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error loading admin logs: {e}")
            return []
    
    def _save_admin_logs(self):
        """Save admin logs"""
        try:
            Path(ADMIN_LOGS).parent.mkdir(parents=True, exist_ok=True)
            with open(ADMIN_LOGS, "w") as f:
                json.dump(self.admin_logs, f, indent=2)
        except Exception as e:
            print(f"Error saving admin logs: {e}")
    
    def _add_admin_log(self, message, level="INFO"):
        """Add entry to admin logs"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message
        }
        self.admin_logs.append(log_entry)
        
        # Keep only last 1000 logs
        if len(self.admin_logs) > 1000:
            self.admin_logs = self.admin_logs[-1000:]
        
        self._save_admin_logs()
    
    def verify_admin(self, session_token):
        """Verify if session belongs to admin"""
        if not self.auth_manager:
            return False
        
        return self.auth_manager.is_admin(session_token)
    
    def get_system_stats(self):
        """Get comprehensive system statistics"""
        stats = {
            "timestamp": datetime.now().isoformat(),
            "users": self._get_user_stats(),
            "ecommerce": self._get_ecommerce_stats(),
            "news": self._get_news_stats(),
            "ai": self._get_ai_stats(),
            "logs": len(self.admin_logs)
        }
        
        self.log("System stats retrieved")
        return stats
    
    def _get_user_stats(self):
        """Get user statistics"""
        if not self.auth_manager:
            return {"error": "AuthManager not available"}
        
        return {
            "total_users": len(self.auth_manager.users),
            "active_sessions": len(self.auth_manager.sessions),
            "users_list": list(self.auth_manager.users.keys())
        }
    
    def _get_ecommerce_stats(self):
        """Get e-commerce statistics"""
        if not self.ecommerce_manager:
            return {"error": "EcommerceManager not available"}
        
        total_revenue = sum(order["total"] for order in self.ecommerce_manager.orders)
        
        return {
            "total_products": len(self.ecommerce_manager.products),
            "total_orders": len(self.ecommerce_manager.orders),
            "total_revenue": total_revenue,
            "pending_orders": len([o for o in self.ecommerce_manager.orders if o["status"] == "pending"])
        }
    
    def _get_news_stats(self):
        """Get news statistics"""
        if not self.news_manager:
            return {"error": "NewsManager not available"}
        
        return {
            "sources": len(self.news_manager.sources),
            "cached_articles": len(self.news_manager.cache),
            "categories": self.news_manager.get_categories()
        }
    
    def _get_ai_stats(self):
        """Get AI statistics"""
        if not self.ai_manager:
            return {"error": "AIManager not available"}
        
        return {
            "conversation_length": len(self.ai_manager.conversation_history),
            "anthropic_configured": bool(self.ai_manager.anthropic_key),
            "openai_configured": bool(self.ai_manager.openai_key)
        }
    
    def manage_user(self, action, username, **kwargs):
        """Manage user accounts"""
        if not self.auth_manager:
            return False, "AuthManager not available"
        
        if action == "delete":
            if username in self.auth_manager.users:
                del self.auth_manager.users[username]
                self.auth_manager._save_users()
                self.log(f"User deleted: {username}")
                return True, "User deleted"
            return False, "User not found"
        
        elif action == "promote_admin":
            if username in self.auth_manager.users:
                self.auth_manager.users[username]["role"] = "admin"
                self.auth_manager._save_users()
                self.log(f"User promoted to admin: {username}")
                return True, "User promoted"
            return False, "User not found"
        
        elif action == "demote":
            if username in self.auth_manager.users:
                self.auth_manager.users[username]["role"] = "user"
                self.auth_manager._save_users()
                self.log(f"User demoted: {username}")
                return True, "User demoted"
            return False, "User not found"
        
        return False, "Unknown action"
    
    def manage_product(self, action, product_id=None, **kwargs):
        """Manage products"""
        if not self.ecommerce_manager:
            return False, "EcommerceManager not available"
        
        if action == "create":
            from modules.ecommerce import Product
            product = Product(
                id=kwargs.get("id"),
                name=kwargs.get("name"),
                description=kwargs.get("description"),
                price=kwargs.get("price"),
                category=kwargs.get("category"),
                stock=kwargs.get("stock"),
                image_url=kwargs.get("image_url")
            )
            self.ecommerce_manager.products.append(product)
            self.ecommerce_manager._save_products()
            self.log(f"Product created: {product.name}")
            return True, "Product created"
        
        elif action == "delete":
            self.ecommerce_manager.products = [
                p for p in self.ecommerce_manager.products if p.id != product_id
            ]
            self.ecommerce_manager._save_products()
            self.log(f"Product deleted: {product_id}")
            return True, "Product deleted"
        
        elif action == "update_stock":
            product = self.ecommerce_manager.get_product(product_id)
            if product:
                product.stock = kwargs.get("stock")
                self.ecommerce_manager._save_products()
                self.log(f"Stock updated: {product_id} - {product.stock}")
                return True, "Stock updated"
            return False, "Product not found"
        
        return False, "Unknown action"
    
    def manage_order(self, action, order_id, **kwargs):
        """Manage orders"""
        if not self.ecommerce_manager:
            return False, "EcommerceManager not available"
        
        order = next((o for o in self.ecommerce_manager.orders if o["order_id"] == order_id), None)
        
        if not order:
            return False, "Order not found"
        
        if action == "update_status":
            order["status"] = kwargs.get("status")
            self.ecommerce_manager._save_orders()
            self.log(f"Order status updated: {order_id} - {order['status']}")
            return True, "Order updated"
        
        elif action == "cancel":
            order["status"] = "cancelled"
            # Restore stock
            for item in order["items"]:
                product = self.ecommerce_manager.get_product(item["product"]["id"])
                if product:
                    product.stock += item["quantity"]
            self.ecommerce_manager._save_products()
            self.ecommerce_manager._save_orders()
            self.log(f"Order cancelled: {order_id}")
            return True, "Order cancelled"
        
        return False, "Unknown action"
    
    def get_admin_logs(self, limit=100, level=None):
        """Get admin logs"""
        logs = self.admin_logs
        
        if level:
            logs = [l for l in logs if l["level"] == level]
        
        return logs[-limit:]
    
    def clear_admin_logs(self):
        """Clear admin logs"""
        self.admin_logs = []
        self._save_admin_logs()
        self.log("Admin logs cleared")
        return True
    
    def export_data(self, data_type):
        """Export system data"""
        exports = {}
        
        if data_type == "all" or data_type == "users":
            if self.auth_manager:
                exports["users"] = list(self.auth_manager.users.values())
        
        if data_type == "all" or data_type == "products":
            if self.ecommerce_manager:
                exports["products"] = [p.to_dict() for p in self.ecommerce_manager.products]
        
        if data_type == "all" or data_type == "orders":
            if self.ecommerce_manager:
                exports["orders"] = self.ecommerce_manager.orders
        
        if data_type == "all" or data_type == "logs":
            exports["admin_logs"] = self.admin_logs
        
        self.log(f"Data exported: {data_type}")
        return exports