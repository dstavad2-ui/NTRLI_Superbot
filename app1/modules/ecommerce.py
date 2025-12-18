"""
E-commerce Module
ANDROID SAFE: No heavy imports at top level
"""
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from pathlib import Path

MINIMUM_ORDER_AMOUNT = 400  # NOK


class Product:
    """Product model"""

    def __init__(self, id: str, name: str, price: float, description: str,
                 thumbnail: str, category: str, stock: int = 0, is_preorder: bool = False):
        self.id = id
        self.name = name
        self.price = price
        self.description = description
        self.thumbnail = thumbnail
        self.category = category
        self.stock = stock
        self.is_preorder = is_preorder

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'thumbnail': self.thumbnail,
            'category': self.category,
            'stock': self.stock,
            'is_preorder': self.is_preorder
        }

    @staticmethod
    def from_dict(data: Dict) -> 'Product':
        return Product(**data)


class CartItem:
    """Shopping cart item"""

    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity

    @property
    def total_price(self) -> float:
        return self.product.price * self.quantity

    def to_dict(self) -> Dict:
        return {
            'product': self.product.to_dict(),
            'quantity': self.quantity,
            'total': self.total_price
        }


class EcommerceManager:
    """Manages e-commerce - Android safe"""

    def __init__(self):
        self.products: List[Product] = []
        self.cart: List[CartItem] = []

        self.data_dir = Path(__file__).parent.parent / 'data'
        self.data_dir.mkdir(exist_ok=True)

        self.products_file = self.data_dir / 'products.json'

        self.payment_methods = [
            'credit_card', 'debit_card', 'vipps',
            'paypal', 'crypto', 'bank_transfer'
        ]

        self._load_products()

    def _load_products(self):
        """Load products from file"""
        if self.products_file.exists():
            try:
                with open(self.products_file, 'r') as f:
                    data = json.load(f)
                    self.products = [Product.from_dict(p) for p in data]
            except Exception as e:
                print(f"Failed to load products: {e}")
                self._create_sample_products()
        else:
            self._create_sample_products()

    def _create_sample_products(self):
        """Create sample products"""
        sample_products = [
            Product(
                id="PROD001",
                name="Premium Headphones",
                price=599.00,
                description="High-quality wireless headphones",
                thumbnail="assets/products/headphones.jpg",
                category="Electronics",
                stock=50
            ),
            Product(
                id="PROD002",
                name="Smart Watch",
                price=899.00,
                description="Fitness tracking smartwatch",
                thumbnail="assets/products/smartwatch.jpg",
                category="Electronics",
                stock=30
            ),
            Product(
                id="PROD003",
                name="Coffee Maker",
                price=450.00,
                description="Automatic coffee maker",
                thumbnail="assets/products/coffee.jpg",
                category="Home",
                stock=20
            )
        ]
        self.products = sample_products
        self._save_products()

    def _save_products(self):
        """Save products to file"""
        try:
            with open(self.products_file, 'w') as f:
                json.dump([p.to_dict() for p in self.products], f, indent=2)
        except Exception as e:
            print(f"Failed to save products: {e}")

    def list_products(self) -> List[Dict]:
        """List all products - simple interface"""
        return [{'name': p.name, 'price': p.price} for p in self.products]

    def get_products(self, category: Optional[str] = None) -> List[Dict]:
        """Get all products or by category"""
        products = self.products
        if category:
            products = [p for p in products if p.category == category]
        return [p.to_dict() for p in products]

    def get_product(self, product_id: str) -> Optional[Dict]:
        """Get product by ID"""
        for product in self.products:
            if product.id == product_id:
                return product.to_dict()
        return None

    def add_to_cart(self, product_id: str, quantity: int = 1) -> Dict:
        """Add product to cart"""
        product = None
        for p in self.products:
            if p.id == product_id:
                product = p
                break

        if not product:
            return {'success': False, 'error': 'Product not found'}

        for item in self.cart:
            if item.product.id == product_id:
                item.quantity += quantity
                return {'success': True, 'cart': self.get_cart()}

        self.cart.append(CartItem(product, quantity))
        return {'success': True, 'cart': self.get_cart()}

    def get_cart(self) -> Dict:
        """Get cart summary"""
        total = sum(item.total_price for item in self.cart)
        return {
            'items': [item.to_dict() for item in self.cart],
            'total': total,
            'item_count': len(self.cart),
            'meets_minimum': total >= MINIMUM_ORDER_AMOUNT
        }

    def clear_cart(self):
        """Clear shopping cart"""
        self.cart = []
        return {'success': True}
