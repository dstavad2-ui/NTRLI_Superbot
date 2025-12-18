"""
E-commerce Module
Features:
- Product catalog with thumbnails
- Shopping cart
- Pre-orders
- 400 NOK minimum order
- Delivery scheduling
- Multiple payment methods
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


class Order:
    """Order model"""

    def __init__(self, order_id: str, user_id: int, items: List[CartItem],
                 delivery_date: str, payment_method: str, status: str = 'pending'):
        self.order_id = order_id
        self.user_id = user_id
        self.items = items
        self.delivery_date = delivery_date
        self.payment_method = payment_method
        self.status = status
        self.created_at = datetime.now().isoformat()

    @property
    def total_amount(self) -> float:
        return sum(item.total_price for item in self.items)

    def to_dict(self) -> Dict:
        return {
            'order_id': self.order_id,
            'user_id': self.user_id,
            'items': [item.to_dict() for item in self.items],
            'total_amount': self.total_amount,
            'delivery_date': self.delivery_date,
            'payment_method': self.payment_method,
            'status': self.status,
            'created_at': self.created_at
        }


class EcommerceManager:
    """Manages e-commerce functionality"""

    def __init__(self):
        self.products: List[Product] = []
        self.cart: List[CartItem] = []
        self.orders: List[Order] = []

        # Data files
        self.data_dir = Path(__file__).parent.parent / 'data'
        self.data_dir.mkdir(exist_ok=True)

        self.products_file = self.data_dir / 'products.json'
        self.orders_file = self.data_dir / 'orders.json'

        # Payment methods
        self.payment_methods = [
            'credit_card',
            'debit_card',
            'vipps',
            'paypal',
            'crypto',
            'bank_transfer'
        ]

        # Load data
        self.load_products()
        self.load_orders()

    def load_products(self):
        """Load products from file"""
        if self.products_file.exists():
            try:
                with open(self.products_file, 'r') as f:
                    data = json.load(f)
                    self.products = [Product.from_dict(p) for p in data]
            except Exception as e:
                print(f"Failed to load products: {e}")
                self.create_sample_products()
        else:
            self.create_sample_products()

    def create_sample_products(self):
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
            ),
            Product(
                id="PREORDER001",
                name="Next-Gen Console",
                price=4999.00,
                description="Pre-order the latest gaming console",
                thumbnail="assets/products/console.jpg",
                category="Gaming",
                stock=0,
                is_preorder=True
            )
        ]
        self.products = sample_products
        self.save_products()

    def save_products(self):
        """Save products to file"""
        try:
            with open(self.products_file, 'w') as f:
                json.dump([p.to_dict() for p in self.products], f, indent=2)
        except Exception as e:
            print(f"Failed to save products: {e}")

    def load_orders(self):
        """Load orders from file"""
        if self.orders_file.exists():
            try:
                with open(self.orders_file, 'r') as f:
                    data = json.load(f)
                    # Reconstruct orders (simplified)
                    self.orders = data
            except Exception as e:
                print(f"Failed to load orders: {e}")

    def save_orders(self):
        """Save orders to file"""
        try:
            with open(self.orders_file, 'w') as f:
                json.dump([o.to_dict() for o in self.orders], f, indent=2)
        except Exception as e:
            print(f"Failed to save orders: {e}")

    def get_products(self, category: Optional[str] = None) -> List[Product]:
        """Get all products or by category"""
        if category:
            return [p for p in self.products if p.category == category]
        return self.products

    def get_product(self, product_id: str) -> Optional[Product]:
        """Get product by ID"""
        for product in self.products:
            if product.id == product_id:
                return product
        return None

    def add_to_cart(self, product_id: str, quantity: int = 1) -> Dict:
        """Add product to cart"""
        product = self.get_product(product_id)
        if not product:
            return {'success': False, 'error': 'Product not found'}

        # Check stock (except for pre-orders)
        if not product.is_preorder and product.stock < quantity:
            return {'success': False, 'error': 'Insufficient stock'}

        # Check if product already in cart
        for item in self.cart:
            if item.product.id == product_id:
                item.quantity += quantity
                return {'success': True, 'cart': self.get_cart_summary()}

        # Add new item to cart
        self.cart.append(CartItem(product, quantity))
        return {'success': True, 'cart': self.get_cart_summary()}

    def remove_from_cart(self, product_id: str) -> Dict:
        """Remove product from cart"""
        self.cart = [item for item in self.cart if item.product.id != product_id]
        return {'success': True, 'cart': self.get_cart_summary()}

    def update_cart_quantity(self, product_id: str, quantity: int) -> Dict:
        """Update quantity of item in cart"""
        for item in self.cart:
            if item.product.id == product_id:
                if quantity <= 0:
                    return self.remove_from_cart(product_id)
                item.quantity = quantity
                return {'success': True, 'cart': self.get_cart_summary()}

        return {'success': False, 'error': 'Product not in cart'}

    def get_cart_summary(self) -> Dict:
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

    def checkout(self, user_id: int, delivery_date: str, payment_method: str) -> Dict:
        """Process checkout"""
        # Validate cart
        cart_summary = self.get_cart_summary()

        if not cart_summary['items']:
            return {'success': False, 'error': 'Cart is empty'}

        if not cart_summary['meets_minimum']:
            return {
                'success': False,
                'error': f'Minimum order amount is {MINIMUM_ORDER_AMOUNT} NOK'
            }

        # Validate payment method
        if payment_method not in self.payment_methods:
            return {'success': False, 'error': 'Invalid payment method'}

        # Validate delivery date
        try:
            delivery = datetime.fromisoformat(delivery_date)
            if delivery < datetime.now() + timedelta(days=1):
                return {'success': False, 'error': 'Delivery date must be at least 1 day ahead'}
        except ValueError:
            return {'success': False, 'error': 'Invalid delivery date format'}

        # Create order
        order_id = f"ORDER{datetime.now().strftime('%Y%m%d%H%M%S')}"
        order = Order(
            order_id=order_id,
            user_id=user_id,
            items=self.cart.copy(),
            delivery_date=delivery_date,
            payment_method=payment_method
        )

        # Update stock
        for item in self.cart:
            if not item.product.is_preorder:
                item.product.stock -= item.quantity

        # Save order
        self.orders.append(order)
        self.save_orders()
        self.save_products()

        # Clear cart
        self.clear_cart()

        return {
            'success': True,
            'order': order.to_dict(),
            'message': f'Order {order_id} placed successfully'
        }

    def get_orders(self, user_id: Optional[int] = None) -> List[Dict]:
        """Get orders, optionally filtered by user"""
        if user_id:
            return [o.to_dict() for o in self.orders if o.user_id == user_id]
        return [o.to_dict() for o in self.orders]

    def get_order(self, order_id: str) -> Optional[Dict]:
        """Get specific order"""
        for order in self.orders:
            if order.order_id == order_id:
                return order.to_dict()
        return None
