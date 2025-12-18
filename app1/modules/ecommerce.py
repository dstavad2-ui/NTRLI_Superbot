"""
NTRLI SuperAPK - E-commerce Module
Phase 2: Product catalog, shopping cart, 400 NOK minimum order
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

PRODUCTS_DB = "/sdcard/superapk_products.json"
ORDERS_DB = "/sdcard/superapk_orders.json"
CART_DB = "/sdcard/superapk_cart.json"

MINIMUM_ORDER = 400.0  # NOK

class Product:
    """Product model"""
    def __init__(self, id, name, description, price, category, stock, image_url=None):
        self.id = id
        self.name = name
        self.description = description
        self.price = float(price)
        self.category = category
        self.stock = int(stock)
        self.image_url = image_url
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "category": self.category,
            "stock": self.stock,
            "image_url": self.image_url
        }

class CartItem:
    """Shopping cart item"""
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = int(quantity)
    
    def get_subtotal(self):
        return self.product.price * self.quantity
    
    def to_dict(self):
        return {
            "product": self.product.to_dict(),
            "quantity": self.quantity,
            "subtotal": self.get_subtotal()
        }

class EcommerceManager:
    """Handles product catalog, cart, and orders"""
    
    def __init__(self, ai_console=None):
        self.ai_console = ai_console
        self.products = self._load_products()
        self.cart = self._load_cart()
        self.orders = self._load_orders()
        self._ensure_sample_products()
        self.log("EcommerceManager initialized")
    
    def log(self, msg, level="INFO"):
        if self.ai_console:
            self.ai_console.log(f"[ECOMMERCE] {msg}", level)
        else:
            print(f"[ECOMMERCE] {msg}")
    
    def _load_products(self):
        """Load product catalog"""
        try:
            if os.path.exists(PRODUCTS_DB):
                with open(PRODUCTS_DB, "r") as f:
                    data = json.load(f)
                    return [Product(**p) for p in data]
            return []
        except Exception as e:
            self.log(f"Error loading products: {e}", "ERROR")
            return []
    
    def _save_products(self):
        """Save product catalog"""
        try:
            Path(PRODUCTS_DB).parent.mkdir(parents=True, exist_ok=True)
            with open(PRODUCTS_DB, "w") as f:
                json.dump([p.to_dict() for p in self.products], f, indent=2)
        except Exception as e:
            self.log(f"Error saving products: {e}", "ERROR")
    
    def _load_cart(self):
        """Load shopping cart"""
        try:
            if os.path.exists(CART_DB):
                with open(CART_DB, "r") as f:
                    data = json.load(f)
                    cart = []
                    for item_data in data:
                        product = Product(**item_data["product"])
                        cart.append(CartItem(product, item_data["quantity"]))
                    return cart
            return []
        except Exception as e:
            self.log(f"Error loading cart: {e}", "ERROR")
            return []
    
    def _save_cart(self):
        """Save shopping cart"""
        try:
            Path(CART_DB).parent.mkdir(parents=True, exist_ok=True)
            with open(CART_DB, "w") as f:
                json.dump([item.to_dict() for item in self.cart], f, indent=2)
        except Exception as e:
            self.log(f"Error saving cart: {e}", "ERROR")
    
    def _load_orders(self):
        """Load order history"""
        try:
            if os.path.exists(ORDERS_DB):
                with open(ORDERS_DB, "r") as f:
                    return json.load(f)
            return []
        except Exception as e:
            self.log(f"Error loading orders: {e}", "ERROR")
            return []
    
    def _save_orders(self):
        """Save order history"""
        try:
            Path(ORDERS_DB).parent.mkdir(parents=True, exist_ok=True)
            with open(ORDERS_DB, "w") as f:
                json.dump(self.orders, f, indent=2)
        except Exception as e:
            self.log(f"Error saving orders: {e}", "ERROR")
    
    def _ensure_sample_products(self):
        """Create sample products if none exist"""
        if len(self.products) == 0:
            sample_products = [
                Product("prod_001", "Premium Business Consulting", "Expert business strategy consultation", 500.0, "services", 100),
                Product("prod_002", "AI Integration Package", "Complete AI integration for your business", 800.0, "services", 50),
                Product("prod_003", "Digital Marketing Suite", "Comprehensive digital marketing package", 600.0, "marketing", 75),
                Product("prod_004", "E-commerce Setup", "Full e-commerce platform setup", 1200.0, "services", 30),
                Product("prod_005", "Brand Development", "Professional brand identity package", 450.0, "marketing", 60),
            ]
            self.products = sample_products
            self._save_products()
            self.log("Sample products created")
    
    def get_products(self, category=None):
        """Get all products or by category"""
        if category:
            return [p for p in self.products if p.category == category]
        return self.products
    
    def get_product(self, product_id):
        """Get product by ID"""
        for product in self.products:
            if product.id == product_id:
                return product
        return None
    
    def add_to_cart(self, product_id, quantity=1):
        """Add product to cart"""
        product = self.get_product(product_id)
        if not product:
            self.log(f"Product not found: {product_id}", "ERROR")
            return False, "Product not found"
        
        if product.stock < quantity:
            self.log(f"Insufficient stock for {product_id}", "WARNING")
            return False, "Insufficient stock"
        
        # Check if product already in cart
        for item in self.cart:
            if item.product.id == product_id:
                item.quantity += quantity
                self._save_cart()
                self.log(f"Updated cart: {product.name} x{item.quantity}")
                return True, f"Updated quantity to {item.quantity}"
        
        # Add new item
        self.cart.append(CartItem(product, quantity))
        self._save_cart()
        self.log(f"Added to cart: {product.name} x{quantity}")
        return True, "Added to cart"
    
    def remove_from_cart(self, product_id):
        """Remove product from cart"""
        self.cart = [item for item in self.cart if item.product.id != product_id]
        self._save_cart()
        self.log(f"Removed from cart: {product_id}")
        return True
    
    def update_cart_quantity(self, product_id, quantity):
        """Update quantity in cart"""
        for item in self.cart:
            if item.product.id == product_id:
                if quantity <= 0:
                    return self.remove_from_cart(product_id)
                item.quantity = quantity
                self._save_cart()
                self.log(f"Updated cart quantity: {product_id} x{quantity}")
                return True, "Quantity updated"
        return False, "Item not in cart"
    
    def get_cart(self):
        """Get current cart"""
        return self.cart
    
    def get_cart_total(self):
        """Calculate cart total"""
        total = sum(item.get_subtotal() for item in self.cart)
        return total
    
    def clear_cart(self):
        """Clear shopping cart"""
        self.cart = []
        self._save_cart()
        self.log("Cart cleared")
        return True
    
    def checkout(self, user_info):
        """Process checkout"""
        total = self.get_cart_total()
        
        # Check minimum order
        if total < MINIMUM_ORDER:
            self.log(f"Order below minimum: {total} NOK < {MINIMUM_ORDER} NOK", "WARNING")
            return False, f"Minimum order is {MINIMUM_ORDER} NOK. Current total: {total} NOK"
        
        # Check stock availability
        for item in self.cart:
            product = self.get_product(item.product.id)
            if product.stock < item.quantity:
                return False, f"Insufficient stock for {product.name}"
        
        # Create order
        order = {
            "order_id": f"ORD_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "user": user_info,
            "items": [item.to_dict() for item in self.cart],
            "total": total,
            "status": "pending",
            "created": datetime.now().isoformat()
        }
        
        # Update stock
        for item in self.cart:
            product = self.get_product(item.product.id)
            product.stock -= item.quantity
        self._save_products()
        
        # Save order
        self.orders.append(order)
        self._save_orders()
        
        # Clear cart
        self.clear_cart()
        
        self.log(f"Order created: {order['order_id']} - {total} NOK")
        return True, order
    
    def get_orders(self, username=None):
        """Get order history"""
        if username:
            return [o for o in self.orders if o["user"].get("username") == username]
        return self.orders