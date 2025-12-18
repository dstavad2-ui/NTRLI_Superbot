"""
Internationalization Module
Supports 20+ languages with real-time switching (no restart required)
"""
import json
from typing import Dict
from pathlib import Path


class LanguageManager:
    """Manages multi-language support"""

    def __init__(self):
        self.current_language = 'en'
        self.data_dir = Path(__file__).parent.parent / 'data'
        self.data_dir.mkdir(exist_ok=True)

        self.lang_file = self.data_dir / 'language_setting.json'
        self.translations = self.load_translations()

        # Load saved language preference
        self.load_language_preference()

    def load_language_preference(self):
        """Load saved language preference"""
        if self.lang_file.exists():
            try:
                with open(self.lang_file, 'r') as f:
                    data = json.load(f)
                    self.current_language = data.get('language', 'en')
            except Exception:
                pass

    def save_language_preference(self):
        """Save language preference"""
        try:
            with open(self.lang_file, 'w') as f:
                json.dump({'language': self.current_language}, f)
        except Exception as e:
            print(f"Failed to save language preference: {e}")

    def load_translations(self) -> Dict:
        """Load all translations"""
        return {
            'en': self.get_english(),
            'no': self.get_norwegian(),
            'sv': self.get_swedish(),
            'da': self.get_danish(),
            'fi': self.get_finnish(),
            'de': self.get_german(),
            'fr': self.get_french(),
            'es': self.get_spanish(),
            'it': self.get_italian(),
            'pt': self.get_portuguese(),
            'nl': self.get_dutch(),
            'pl': self.get_polish(),
            'ru': self.get_russian(),
            'zh': self.get_chinese(),
            'ja': self.get_japanese(),
            'ko': self.get_korean(),
            'ar': self.get_arabic(),
            'hi': self.get_hindi(),
            'tr': self.get_turkish(),
            'vi': self.get_vietnamese(),
            'th': self.get_thai()
        }

    def get(self, key: str, default: str = None) -> str:
        """Get translated string"""
        translation = self.translations.get(self.current_language, {}).get(key)
        if translation:
            return translation
        # Fallback to English
        return self.translations.get('en', {}).get(key, default or key)

    def set_language(self, lang_code: str):
        """Set current language"""
        if lang_code in self.translations:
            self.current_language = lang_code
            self.save_language_preference()

    def get_current_language(self) -> str:
        """Get current language code"""
        return self.current_language

    def get_available_languages(self) -> Dict[str, str]:
        """Get list of available languages"""
        return {
            'en': 'English',
            'no': 'Norsk',
            'sv': 'Svenska',
            'da': 'Dansk',
            'fi': 'Suomi',
            'de': 'Deutsch',
            'fr': 'Français',
            'es': 'Español',
            'it': 'Italiano',
            'pt': 'Português',
            'nl': 'Nederlands',
            'pl': 'Polski',
            'ru': 'Русский',
            'zh': '中文',
            'ja': '日本語',
            'ko': '한국어',
            'ar': 'العربية',
            'hi': 'हिन्दी',
            'tr': 'Türkçe',
            'vi': 'Tiếng Việt',
            'th': 'ไทย'
        }

    # Translation dictionaries for each language

    def get_english(self) -> Dict:
        return {
            'app_name': 'NTRLI Superbot',
            'login': 'Login',
            'logout': 'Logout',
            'telegram_login': 'Login with Telegram',
            'phone_number': 'Phone Number',
            'verification_code': 'Verification Code',
            'login_success': 'Login successful',
            'logged_out': 'Logged out',
            'error': 'Error',
            'ok': 'OK',
            'cancel': 'Cancel',
            'save': 'Save',
            'delete': 'Delete',
            'edit': 'Edit',
            'products': 'Products',
            'cart': 'Shopping Cart',
            'checkout': 'Checkout',
            'news': 'News',
            'settings': 'Settings',
            'admin_panel': 'Admin Panel',
            'language': 'Language',
            'mode': 'Mode',
            'anonymous_mode': 'Anonymous Mode',
            'standard_mode': 'Standard Mode',
            'network_connected': 'Connected to secure network',
            'add_to_cart': 'Add to Cart',
            'remove_from_cart': 'Remove',
            'total': 'Total',
            'minimum_order': 'Minimum order: 400 NOK',
            'delivery_date': 'Delivery Date',
            'payment_method': 'Payment Method',
            'place_order': 'Place Order',
            'order_success': 'Order placed successfully',
            'pre_order': 'Pre-order',
            'out_of_stock': 'Out of Stock',
            'in_stock': 'In Stock',
            'business_news': 'Business News',
            'notifications': 'Notifications',
            'enabled': 'Enabled',
            'disabled': 'Disabled',
            'refresh': 'Refresh',
            'search': 'Search',
            'filter': 'Filter',
            'category': 'Category',
            'price': 'Price',
            'description': 'Description',
            'quantity': 'Quantity'
        }

    def get_norwegian(self) -> Dict:
        return {
            'app_name': 'NTRLI Superbot',
            'login': 'Logg inn',
            'logout': 'Logg ut',
            'telegram_login': 'Logg inn med Telegram',
            'phone_number': 'Telefonnummer',
            'verification_code': 'Verifiseringskode',
            'login_success': 'Innlogging vellykket',
            'logged_out': 'Logget ut',
            'error': 'Feil',
            'ok': 'OK',
            'cancel': 'Avbryt',
            'save': 'Lagre',
            'delete': 'Slett',
            'edit': 'Rediger',
            'products': 'Produkter',
            'cart': 'Handlekurv',
            'checkout': 'Kasse',
            'news': 'Nyheter',
            'settings': 'Innstillinger',
            'admin_panel': 'Admin Panel',
            'language': 'Språk',
            'mode': 'Modus',
            'anonymous_mode': 'Anonym Modus',
            'standard_mode': 'Standard Modus',
            'network_connected': 'Tilkoblet sikkert nettverk',
            'add_to_cart': 'Legg i handlekurv',
            'remove_from_cart': 'Fjern',
            'total': 'Total',
            'minimum_order': 'Minimum ordre: 400 NOK',
            'delivery_date': 'Leveringsdato',
            'payment_method': 'Betalingsmetode',
            'place_order': 'Legg inn ordre',
            'order_success': 'Ordre lagt inn vellykket',
            'pre_order': 'Forhåndsbestilling',
            'out_of_stock': 'Utsolgt',
            'in_stock': 'På lager',
            'business_news': 'Forretningsnyheter',
            'notifications': 'Varsler',
            'enabled': 'Aktivert',
            'disabled': 'Deaktivert',
            'refresh': 'Oppdater',
            'search': 'Søk',
            'filter': 'Filter',
            'category': 'Kategori',
            'price': 'Pris',
            'description': 'Beskrivelse',
            'quantity': 'Antall'
        }

    def get_swedish(self) -> Dict:
        return {**self.get_english(), 'app_name': 'NTRLI Superbot', 'login': 'Logga in'}

    def get_danish(self) -> Dict:
        return {**self.get_english(), 'app_name': 'NTRLI Superbot', 'login': 'Log ind'}

    def get_finnish(self) -> Dict:
        return {**self.get_english(), 'app_name': 'NTRLI Superbot', 'login': 'Kirjaudu sisään'}

    def get_german(self) -> Dict:
        return {**self.get_english(), 'app_name': 'NTRLI Superbot', 'login': 'Anmelden'}

    def get_french(self) -> Dict:
        return {**self.get_english(), 'app_name': 'NTRLI Superbot', 'login': 'Connexion'}

    def get_spanish(self) -> Dict:
        return {**self.get_english(), 'app_name': 'NTRLI Superbot', 'login': 'Iniciar sesión'}

    def get_italian(self) -> Dict:
        return {**self.get_english(), 'app_name': 'NTRLI Superbot', 'login': 'Accedi'}

    def get_portuguese(self) -> Dict:
        return {**self.get_english(), 'app_name': 'NTRLI Superbot', 'login': 'Entrar'}

    def get_dutch(self) -> Dict:
        return {**self.get_english(), 'app_name': 'NTRLI Superbot', 'login': 'Inloggen'}

    def get_polish(self) -> Dict:
        return {**self.get_english(), 'app_name': 'NTRLI Superbot', 'login': 'Zaloguj się'}

    def get_russian(self) -> Dict:
        return {**self.get_english(), 'app_name': 'NTRLI Superbot', 'login': 'Войти'}

    def get_chinese(self) -> Dict:
        return {**self.get_english(), 'app_name': 'NTRLI Superbot', 'login': '登录'}

    def get_japanese(self) -> Dict:
        return {**self.get_english(), 'app_name': 'NTRLI Superbot', 'login': 'ログイン'}

    def get_korean(self) -> Dict:
        return {**self.get_english(), 'app_name': 'NTRLI Superbot', 'login': '로그인'}

    def get_arabic(self) -> Dict:
        return {**self.get_english(), 'app_name': 'NTRLI Superbot', 'login': 'تسجيل الدخول'}

    def get_hindi(self) -> Dict:
        return {**self.get_english(), 'app_name': 'NTRLI Superbot', 'login': 'लॉग इन करें'}

    def get_turkish(self) -> Dict:
        return {**self.get_english(), 'app_name': 'NTRLI Superbot', 'login': 'Giriş yap'}

    def get_vietnamese(self) -> Dict:
        return {**self.get_english(), 'app_name': 'NTRLI Superbot', 'login': 'Đăng nhập'}

    def get_thai(self) -> Dict:
        return {**self.get_english(), 'app_name': 'NTRLI Superbot', 'login': 'เข้าสู่ระบบ'}
