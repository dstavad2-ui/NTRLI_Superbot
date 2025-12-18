"""
NTRLI SuperAPK - Internationalization Module
Phase 3: Multi-language support
"""
import json
import os
from pathlib import Path

LANG_DIR = "/sdcard/superapk_languages"
DEFAULT_LANG = "en"

class I18nManager:
    """Handles multi-language support"""
    
    # Default translations
    DEFAULT_TRANSLATIONS = {
        "en": {
            "app_title": "NTRLI SuperAPK",
            "app_subtitle": "AI-Powered Business Platform",
            "get_started": "Get Started",
            "settings": "Settings",
            "login": "Login",
            "logout": "Logout",
            "username": "Username",
            "password": "Password",
            "register": "Register",
            "products": "Products",
            "cart": "Shopping Cart",
            "checkout": "Checkout",
            "total": "Total",
            "minimum_order": "Minimum Order",
            "add_to_cart": "Add to Cart",
            "news": "News",
            "business": "Business",
            "technology": "Technology",
            "admin_panel": "Admin Panel",
            "users": "Users",
            "orders": "Orders",
            "system_stats": "System Statistics"
        },
        "no": {
            "app_title": "NTRLI SuperAPK",
            "app_subtitle": "AI-drevet forretningsplattform",
            "get_started": "Kom i gang",
            "settings": "Innstillinger",
            "login": "Logg inn",
            "logout": "Logg ut",
            "username": "Brukernavn",
            "password": "Passord",
            "register": "Registrer",
            "products": "Produkter",
            "cart": "Handlekurv",
            "checkout": "Kasse",
            "total": "Totalt",
            "minimum_order": "Minimumsbestilling",
            "add_to_cart": "Legg til i handlekurv",
            "news": "Nyheter",
            "business": "Business",
            "technology": "Teknologi",
            "admin_panel": "Adminpanel",
            "users": "Brukere",
            "orders": "Bestillinger",
            "system_stats": "Systemstatistikk"
        },
        "es": {
            "app_title": "NTRLI SuperAPK",
            "app_subtitle": "Plataforma empresarial impulsada por IA",
            "get_started": "Comenzar",
            "settings": "Configuración",
            "login": "Iniciar sesión",
            "logout": "Cerrar sesión",
            "username": "Nombre de usuario",
            "password": "Contraseña",
            "register": "Registrarse",
            "products": "Productos",
            "cart": "Carrito",
            "checkout": "Pagar",
            "total": "Total",
            "minimum_order": "Pedido mínimo",
            "add_to_cart": "Agregar al carrito",
            "news": "Noticias",
            "business": "Negocios",
            "technology": "Tecnología",
            "admin_panel": "Panel de administración",
            "users": "Usuarios",
            "orders": "Pedidos",
            "system_stats": "Estadísticas del sistema"
        },
        "fr": {
            "app_title": "NTRLI SuperAPK",
            "app_subtitle": "Plateforme d'affaires alimentée par l'IA",
            "get_started": "Commencer",
            "settings": "Paramètres",
            "login": "Connexion",
            "logout": "Déconnexion",
            "username": "Nom d'utilisateur",
            "password": "Mot de passe",
            "register": "S'inscrire",
            "products": "Produits",
            "cart": "Panier",
            "checkout": "Paiement",
            "total": "Total",
            "minimum_order": "Commande minimum",
            "add_to_cart": "Ajouter au panier",
            "news": "Actualités",
            "business": "Affaires",
            "technology": "Technologie",
            "admin_panel": "Panneau d'administration",
            "users": "Utilisateurs",
            "orders": "Commandes",
            "system_stats": "Statistiques système"
        }
    }
    
    def __init__(self, ai_console=None, default_lang=DEFAULT_LANG):
        self.ai_console = ai_console
        self.current_lang = default_lang
        self.translations = self._load_translations()
        self._ensure_default_translations()
        self.log(f"I18nManager initialized - Language: {default_lang}")
    
    def log(self, msg, level="INFO"):
        if self.ai_console:
            self.ai_console.log(f"[I18N] {msg}", level)
        else:
            print(f"[I18N] {msg}")
    
    def _ensure_lang_dir(self):
        """Ensure language directory exists"""
        try:
            Path(LANG_DIR).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            self.log(f"Error creating language dir: {e}", "ERROR")
    
    def _load_translations(self):
        """Load all translations from files"""
        self._ensure_lang_dir()
        translations = {}
        
        try:
            for lang_file in Path(LANG_DIR).glob("*.json"):
                lang_code = lang_file.stem
                with open(lang_file, "r", encoding="utf-8") as f:
                    translations[lang_code] = json.load(f)
                self.log(f"Loaded translations: {lang_code}")
        except Exception as e:
            self.log(f"Error loading translations: {e}", "ERROR")
        
        return translations
    
    def _ensure_default_translations(self):
        """Ensure default translations exist"""
        for lang_code, translations in self.DEFAULT_TRANSLATIONS.items():
            if lang_code not in self.translations:
                self.translations[lang_code] = translations
                self._save_translation(lang_code)
    
    def _save_translation(self, lang_code):
        """Save translation to file"""
        self._ensure_lang_dir()
        try:
            lang_file = os.path.join(LANG_DIR, f"{lang_code}.json")
            with open(lang_file, "w", encoding="utf-8") as f:
                json.dump(self.translations[lang_code], f, indent=2, ensure_ascii=False)
            self.log(f"Saved translations: {lang_code}")
        except Exception as e:
            self.log(f"Error saving translations: {e}", "ERROR")
    
    def get_available_languages(self):
        """Get list of available languages"""
        return list(self.translations.keys())
    
    def set_language(self, lang_code):
        """Set current language"""
        if lang_code in self.translations:
            self.current_lang = lang_code
            self.log(f"Language changed to: {lang_code}")
            return True
        else:
            self.log(f"Language not found: {lang_code}", "WARNING")
            return False
    
    def get_language(self):
        """Get current language"""
        return self.current_lang
    
    def translate(self, key, lang=None):
        """Get translation for key"""
        lang = lang or self.current_lang
        
        if lang not in self.translations:
            lang = DEFAULT_LANG
        
        translation = self.translations[lang].get(key)
        
        if translation is None:
            # Fallback to English
            translation = self.translations[DEFAULT_LANG].get(key, key)
            self.log(f"Translation missing: {key} ({lang})", "WARNING")
        
        return translation
    
    def t(self, key, lang=None):
        """Shorthand for translate"""
        return self.translate(key, lang)
    
    def add_translation(self, lang_code, key, value):
        """Add or update a translation"""
        if lang_code not in self.translations:
            self.translations[lang_code] = {}
        
        self.translations[lang_code][key] = value
        self._save_translation(lang_code)
        self.log(f"Translation added: {lang_code}.{key}")
        return True
    
    def add_language(self, lang_code, translations):
        """Add a new language with translations"""
        self.translations[lang_code] = translations
        self._save_translation(lang_code)
        self.log(f"Language added: {lang_code}")
        return True
    
    def remove_language(self, lang_code):
        """Remove a language"""
        if lang_code == DEFAULT_LANG:
            self.log(f"Cannot remove default language: {lang_code}", "ERROR")
            return False
        
        if lang_code in self.translations:
            del self.translations[lang_code]
            
            # Remove file
            try:
                lang_file = os.path.join(LANG_DIR, f"{lang_code}.json")
                if os.path.exists(lang_file):
                    os.remove(lang_file)
            except Exception as e:
                self.log(f"Error removing language file: {e}", "ERROR")
            
            self.log(f"Language removed: {lang_code}")
            return True
        
        return False
    
    def get_all_translations(self, lang=None):
        """Get all translations for a language"""
        lang = lang or self.current_lang
        return self.translations.get(lang, {})
    
    def export_translations(self, lang_code):
        """Export translations for a language"""
        if lang_code in self.translations:
            return self.translations[lang_code]
        return None
    
    def import_translations(self, lang_code, translations):
        """Import translations for a language"""
        self.translations[lang_code] = translations
        self._save_translation(lang_code)
        self.log(f"Translations imported: {lang_code}")
        return True
    
    def get_language_name(self, lang_code):
        """Get human-readable language name"""
        language_names = {
            "en": "English",
            "no": "Norsk",
            "es": "Español",
            "fr": "Français",
            "de": "Deutsch",
            "it": "Italiano",
            "pt": "Português",
            "ru": "Русский",
            "zh": "中文",
            "ja": "日本語",
            "ar": "العربية"
        }
        return language_names.get(lang_code, lang_code.upper())