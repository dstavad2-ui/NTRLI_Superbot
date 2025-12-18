# NTRLI Superbot - Quick Start Guide

## 🚀 Build APK in 3 Steps

### Step 1: Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Buildozer (APK builder)
pip install buildozer

# Install Android build tools (Linux/Ubuntu)
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev cmake libffi-dev libssl-dev
```

### Step 2: Configure API Keys

Edit `config.ini` and add your API keys:

```ini
[ai]
anthropic_api_key = your-actual-anthropic-key
openai_api_key = your-actual-openai-key
```

### Step 3: Build APK

```bash
# Make build script executable
chmod +x build_apk.sh

# Run build script
./build_apk.sh

# Or build manually:
buildozer android debug
```

## 📱 Install on Android

1. Transfer APK from `bin/` folder to your phone
2. Enable "Install from Unknown Sources" in Settings
3. Install the APK
4. Launch NTRLI Superbot!

## 🎯 Features Checklist

✅ **Authentication**
- [x] Telegram login only
- [x] Admin access for @Sir_NTRLI_II

✅ **Privacy**
- [x] Tor/Orbot integration
- [x] ProtonVPN fallback
- [x] Anonymous mode
- [x] Standard mode

✅ **AI System**
- [x] Claude API integration
- [x] GPT-4 API integration
- [x] Data validation
- [x] Self-improvement

✅ **E-commerce**
- [x] Product catalog
- [x] Shopping cart
- [x] 400 NOK minimum
- [x] Multiple payment methods
- [x] Pre-orders

✅ **News**
- [x] Business news feed
- [x] Push notifications

✅ **Languages**
- [x] 20+ languages
- [x] Real-time switching

✅ **Admin Panel**
- [x] Web-based panel
- [x] Zero-code config
- [x] Instant deployment

## 🔧 Troubleshooting

### Build fails?
- Make sure you're in the `app1` directory
- Check that all dependencies are installed
- Try: `buildozer android clean`

### APK won't install?
- Enable "Unknown Sources" in Android settings
- Check minimum Android version (7.0+)

### Tor not connecting?
- Install Orbot from Play Store
- Enable Orbot VPN mode

## 📞 Support

Contact: @Sir_NTRLI_II

---

**That's it! You're ready to go! 🎉**
