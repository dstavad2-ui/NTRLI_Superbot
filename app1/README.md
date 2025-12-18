# NTRLI Superbot - Android Application

A comprehensive e-commerce and business news Android application with advanced privacy features, AI integration, and multi-language support.

## Features

### 1. AUTHENTICATION ✅
- **Telegram login ONLY** (no other login methods)
- **@Sir_NTRLI_II** = automatic admin access (User ID: 8467779489)
- Cannot use app without login

### 2. PRIVACY & NETWORK 🔒
- **Orbot/Tor integration** (primary connection)
- **ProtonVPN fallback** (if Tor fails)
- **Anonymous Mode:**
  - Browse products ✅
  - View news ✅
  - NO shopping ✅
  - NO logging ✅
- **Standard Mode:**
  - Full shopping ✅
  - Secure logging ✅

### 3. AI SYSTEM 🤖
- Real-time data validation
- Web research capability
- Self-improvement (monitors logs → suggests changes → needs admin approval)
- Claude + GPT-4 APIs integration

### 4. E-COMMERCE 🛍️
- Product catalog with thumbnails
- Shopping cart
- Pre-orders
- 400 NOK minimum order
- Delivery scheduling
- Multiple payment methods:
  - Credit/Debit cards
  - Vipps
  - PayPal
  - Cryptocurrency
  - Bank transfer

### 5. NEWS 📰
- Business news feed
- Push notifications
- Real-time updates

### 6. LANGUAGES 🌍
- **20+ languages supported:**
  - English, Norwegian, Swedish, Danish, Finnish
  - German, French, Spanish, Italian, Portuguese
  - Dutch, Polish, Russian, Chinese, Japanese
  - Korean, Arabic, Hindi, Turkish, Vietnamese, Thai
- Real-time switching (no restart required)

### 7. ADMIN PANEL 🎛️
- Web-based admin panel
- Zero-code configuration
- Control ALL app settings from browser
- Deploy changes instantly
- Access via @Sir_NTRLI_II Telegram handle

### 8. APK REQUIREMENTS 📱
- Ready-to-install APK file
- Works on Android 7.0+ (API 24+)
- Executable immediately on phone
- All features included in APK

## Project Structure

```
app1/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── buildozer.spec         # APK build configuration
├── modules/               # Application modules
│   ├── __init__.py
│   ├── auth.py           # Telegram authentication
│   ├── network.py        # Tor/VPN integration
│   ├── ai.py             # AI system (Claude + GPT-4)
│   ├── ecommerce.py      # E-commerce functionality
│   ├── news.py           # News feed
│   ├── admin.py          # Admin panel
│   └── i18n.py           # Multi-language support
├── ui/                    # Kivy UI files
│   ├── login.kv
│   ├── main.kv
│   ├── products.kv
│   ├── cart.kv
│   ├── news.kv
│   ├── admin.kv
│   └── settings.kv
├── data/                  # Application data
└── assets/                # Images, icons, etc.
```

## Building the APK

### Prerequisites

1. Install Python 3.8+
2. Install Buildozer:
   ```bash
   pip install buildozer
   ```

3. Install Android dependencies (Linux):
   ```bash
   sudo apt update
   sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
   ```

### Build Instructions

1. **Navigate to app directory:**
   ```bash
   cd app1
   ```

2. **Initialize Buildozer (first time only):**
   ```bash
   buildozer init
   ```

3. **Build APK:**
   ```bash
   buildozer android debug
   ```

4. **For release APK:**
   ```bash
   buildozer android release
   ```

5. **Find your APK:**
   The APK will be in `app1/bin/` directory:
   - Debug: `ntrli_superbot-1.0.0-debug.apk`
   - Release: `ntrli_superbot-1.0.0-release-unsigned.apk`

### Installing on Android Device

1. **Transfer APK to your Android device**
2. **Enable "Install from Unknown Sources" in Android settings**
3. **Open the APK file and install**
4. **Launch NTRLI Superbot**

## Configuration

### API Keys

Before building, configure your API keys in the respective modules:

1. **Telegram API** (`modules/auth.py`):
   - Already configured from `.env.ini`

2. **Claude API** (`modules/ai.py`):
   ```python
   self.anthropic_key = "your-anthropic-api-key"
   ```

3. **OpenAI API** (`modules/ai.py`):
   ```python
   self.openai_key = "your-openai-api-key"
   ```

## Usage

### First Launch

1. **Login with Telegram:**
   - Enter your phone number with country code
   - Enter verification code from Telegram

2. **Network Connection:**
   - App automatically connects via Tor
   - Falls back to ProtonVPN if Tor unavailable

3. **Choose Mode:**
   - **Anonymous Mode:** Browse only, no shopping
   - **Standard Mode:** Full functionality

### Admin Access

**For @Sir_NTRLI_II only:**

1. Login with admin Telegram account
2. Access Admin Panel from main menu
3. Click "Open Web Admin Panel"
4. Access at `http://localhost:5000`

### Shopping

1. Browse products
2. Add to cart
3. Checkout (minimum 400 NOK)
4. Select delivery date
5. Choose payment method
6. Complete order

### Language Change

1. Go to Settings
2. Select Language
3. Choose from 20+ available languages
4. UI updates immediately (no restart)

## Development

### Running in Development Mode

```bash
cd app1
python main.py
```

### Testing on Desktop

The app can run on desktop for testing:
- Window size: 360x640 (mobile dimensions)
- All features work except Android-specific (notifications, Orbot)

## Security

- **Tor/VPN encrypted connections**
- **Telegram authentication**
- **Anonymous mode for privacy**
- **No tracking in anonymous mode**
- **Secure data storage**

## Support

For issues or questions, contact: @Sir_NTRLI_II

## License

Proprietary - All rights reserved

---

**Built with:**
- Kivy/KivyMD (UI Framework)
- Telethon (Telegram Integration)
- Tor/Orbot (Privacy Network)
- Claude AI & GPT-4 (AI Features)
- Flask (Admin Panel)
