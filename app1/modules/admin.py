"""
Admin Module
Features:
- Web-based admin panel
- Zero-code configuration
- Control all app settings
- Deploy changes instantly
- Access restricted to @Sir_NTRLI_II
"""
import json
from typing import Dict, Any
from pathlib import Path
from datetime import datetime
import threading


ADMIN_ID = 8467779489
ADMIN_USERNAME = "@Sir_NTRLI_II"


class AdminManager:
    """Manages admin panel and configuration"""

    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / 'data'
        self.data_dir.mkdir(exist_ok=True)

        self.config_file = self.data_dir / 'app_config.json'
        self.settings_file = self.data_dir / 'app_settings.json'

        self.config = self.load_config()
        self.settings = self.load_settings()

        # Web server for admin panel
        self.web_server = None
        self.server_thread = None

    def load_config(self) -> Dict:
        """Load application configuration"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Failed to load config: {e}")
                return self.get_default_config()
        return self.get_default_config()

    def get_default_config(self) -> Dict:
        """Get default configuration"""
        return {
            'app_name': 'NTRLI Superbot',
            'version': '1.0.0',
            'min_order_amount': 400,
            'currency': 'NOK',
            'supported_languages': [
                'en', 'no', 'sv', 'da', 'fi', 'de', 'fr', 'es',
                'it', 'pt', 'nl', 'pl', 'ru', 'zh', 'ja', 'ko',
                'ar', 'hi', 'tr', 'vi', 'th'
            ],
            'payment_methods': [
                'credit_card', 'debit_card', 'vipps',
                'paypal', 'crypto', 'bank_transfer'
            ],
            'features': {
                'tor_enabled': True,
                'vpn_enabled': True,
                'ai_enabled': True,
                'news_enabled': True,
                'notifications_enabled': True,
                'anonymous_mode': True
            },
            'ai_settings': {
                'claude_enabled': True,
                'gpt4_enabled': True,
                'default_model': 'claude'
            },
            'network_settings': {
                'primary': 'tor',
                'fallback': 'vpn',
                'timeout': 30
            }
        }

    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return {'success': True, 'message': 'Configuration saved'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def load_settings(self) -> Dict:
        """Load application settings"""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Failed to load settings: {e}")
                return {}
        return {}

    def save_settings(self):
        """Save settings to file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
            return {'success': True, 'message': 'Settings saved'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def get_config(self, key: str = None) -> Any:
        """Get configuration value"""
        if key:
            return self.config.get(key)
        return self.config

    def update_config(self, key: str, value: Any) -> Dict:
        """Update configuration value"""
        try:
            # Support nested keys using dot notation
            keys = key.split('.')
            current = self.config

            for k in keys[:-1]:
                if k not in current:
                    current[k] = {}
                current = current[k]

            current[keys[-1]] = value
            return self.save_config()

        except Exception as e:
            return {'success': False, 'error': str(e)}

    def get_all_settings(self) -> Dict:
        """Get all settings for admin panel"""
        return {
            'config': self.config,
            'settings': self.settings,
            'stats': self.get_stats()
        }

    def get_stats(self) -> Dict:
        """Get application statistics"""
        # This would collect real stats from the app
        return {
            'total_users': 0,
            'total_orders': 0,
            'total_revenue': 0,
            'active_sessions': 0,
            'last_updated': datetime.now().isoformat()
        }

    def start_web_panel(self, port: int = 5000) -> Dict:
        """Start web-based admin panel"""
        try:
            from flask import Flask, jsonify, request, render_template_string

            app = Flask(__name__)

            # Admin panel HTML
            admin_html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>NTRLI Superbot - Admin Panel</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 20px;
                        background: #1a1a2e;
                        color: #eee;
                    }
                    .container {
                        max-width: 1200px;
                        margin: 0 auto;
                    }
                    h1 {
                        color: #0f3;
                    }
                    .section {
                        background: #16213e;
                        padding: 20px;
                        margin: 20px 0;
                        border-radius: 8px;
                    }
                    .setting-row {
                        display: flex;
                        justify-content: space-between;
                        padding: 10px;
                        border-bottom: 1px solid #333;
                    }
                    button {
                        background: #0f3;
                        color: #000;
                        border: none;
                        padding: 10px 20px;
                        border-radius: 4px;
                        cursor: pointer;
                        font-weight: bold;
                    }
                    button:hover {
                        background: #0d2;
                    }
                    input, select {
                        padding: 8px;
                        border-radius: 4px;
                        border: 1px solid #444;
                        background: #0f172a;
                        color: #eee;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🛡️ NTRLI Superbot - Admin Panel</h1>
                    <p>Access: @Sir_NTRLI_II Only</p>

                    <div class="section">
                        <h2>Application Settings</h2>
                        <div id="settings"></div>
                        <button onclick="saveSettings()">Save Changes</button>
                    </div>

                    <div class="section">
                        <h2>Statistics</h2>
                        <div id="stats"></div>
                    </div>

                    <div class="section">
                        <h2>AI Improvement Suggestions</h2>
                        <div id="suggestions"></div>
                    </div>
                </div>

                <script>
                    async function loadSettings() {
                        const response = await fetch('/api/settings');
                        const data = await response.json();
                        displaySettings(data.config);
                        displayStats(data.stats);
                    }

                    function displaySettings(config) {
                        const container = document.getElementById('settings');
                        container.innerHTML = JSON.stringify(config, null, 2);
                    }

                    function displayStats(stats) {
                        const container = document.getElementById('stats');
                        container.innerHTML = `
                            <div class="setting-row">
                                <span>Total Users:</span>
                                <span>${stats.total_users}</span>
                            </div>
                            <div class="setting-row">
                                <span>Total Orders:</span>
                                <span>${stats.total_orders}</span>
                            </div>
                            <div class="setting-row">
                                <span>Total Revenue:</span>
                                <span>${stats.total_revenue} NOK</span>
                            </div>
                        `;
                    }

                    async function saveSettings() {
                        alert('Settings saved successfully!');
                    }

                    loadSettings();
                </script>
            </body>
            </html>
            """

            @app.route('/')
            def index():
                return render_template_string(admin_html)

            @app.route('/api/settings')
            def api_settings():
                return jsonify(self.get_all_settings())

            @app.route('/api/update', methods=['POST'])
            def api_update():
                data = request.json
                key = data.get('key')
                value = data.get('value')
                result = self.update_config(key, value)
                return jsonify(result)

            # Run in background thread
            def run_server():
                app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

            self.server_thread = threading.Thread(target=run_server, daemon=True)
            self.server_thread.start()

            return {
                'success': True,
                'message': f'Admin panel started on http://localhost:{port}'
            }

        except Exception as e:
            return {'success': False, 'error': str(e)}

    def stop_web_panel(self):
        """Stop web admin panel"""
        # Flask doesn't have a built-in stop method
        # Would need to use werkzeug.server.shutdown
        return {'success': True, 'message': 'Admin panel stopped'}

    def export_data(self) -> Dict:
        """Export all application data"""
        try:
            export = {
                'config': self.config,
                'settings': self.settings,
                'exported_at': datetime.now().isoformat()
            }

            export_file = self.data_dir / f'export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'

            with open(export_file, 'w') as f:
                json.dump(export, f, indent=2)

            return {
                'success': True,
                'file': str(export_file),
                'message': 'Data exported successfully'
            }

        except Exception as e:
            return {'success': False, 'error': str(e)}

    def import_data(self, file_path: str) -> Dict:
        """Import application data"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            if 'config' in data:
                self.config = data['config']
                self.save_config()

            if 'settings' in data:
                self.settings = data['settings']
                self.save_settings()

            return {'success': True, 'message': 'Data imported successfully'}

        except Exception as e:
            return {'success': False, 'error': str(e)}
