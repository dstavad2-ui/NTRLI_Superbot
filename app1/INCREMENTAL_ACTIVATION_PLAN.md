# NTRLI Superbot - Incremental Module Activation Plan

## Overview
This plan ensures crash-free feature enablement by activating modules in controlled phases.

**Current Status:** Phase 0 (Minimal Stable) ✅

---

## Phase 0: Minimal Stable (CURRENT)
**Status:** ✅ Complete and tested
**Features:**
- Basic UI with NTRLI branding
- Two buttons: "Get Started" and "Settings"
- Global crash logging to `/sdcard/superbot_crash.log`
- Platform-specific window sizing

**Dependencies:**
```
python3
kivy==2.3.1
kivymd==1.1.1
```

**Test Checklist:**
- [x] App launches without crash
- [x] UI displays correctly
- [x] Buttons respond to taps
- [x] Crash logging works

---

## Phase 1: Authentication & Network
**Target:** Enable Telegram login and privacy features

### Modules to Activate:
1. `modules/auth.py` - Telegram authentication
2. `modules/network.py` - Tor/VPN integration

### Additional Dependencies Required:
```
python3
kivy==2.3.1
kivymd==1.1.1
telethon==1.34.0
pysocks==1.7.1
requests==2.31.0
cryptography==41.0.7
```

### Android Permissions to Add:
```
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
```

### Integration Steps:
1. **Update `buildozer.spec`:**
   - Add new dependencies to `requirements`
   - Add storage permissions

2. **Update `main.py`:**
   ```python
   # Add at top
   from modules.auth import TelegramAuth
   from modules.network import NetworkManager

   # In NTRLIApp.__init__:
   def __init__(self, **kwargs):
       super().__init__(**kwargs)
       self.auth = TelegramAuth()
       self.network = NetworkManager()

   # Update show_message() to trigger login:
   def show_message(self):
       if not self.auth.is_authenticated():
           self.auth.show_login_dialog()
       else:
           Snackbar(text=f"Welcome, {self.auth.get_username()}!").open()
   ```

3. **Build and Deploy:**
   ```bash
   rm -rf ~/.buildozer app1/.buildozer
   cd app1
   buildozer android debug
   ```

4. **Test on Device:**
   - Launch app
   - Tap "Get Started"
   - Verify Telegram login dialog appears
   - Complete login flow
   - Check crash log: `adb shell cat /sdcard/superbot_crash.log`
   - Verify network connectivity

### Success Criteria:
- [ ] App launches without crash
- [ ] Telegram login dialog appears
- [ ] User can authenticate with @Sir_NTRLI_II
- [ ] Admin status detected correctly
- [ ] Tor/VPN connection works
- [ ] No crashes logged

**If crashes occur:** Revert to Phase 0, analyze crash log, fix issues, retry.

---

## Phase 2: News & E-commerce
**Target:** Enable business features

### Modules to Activate:
1. `modules/news.py` - Business news feed
2. `modules/ecommerce.py` - Product catalog and shopping

### Additional Dependencies Required:
```
feedparser==6.0.10
pillow==10.2.0
sqlalchemy==2.0.25
```

### Android Permissions to Add:
```
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,POST_NOTIFICATIONS
```

### Integration Steps:
1. **Update `buildozer.spec`:**
   - Add feedparser, pillow, sqlalchemy to `requirements`
   - Add POST_NOTIFICATIONS permission

2. **Update `main.py`:**
   ```python
   # Add imports
   from modules.news import NewsManager
   from modules.ecommerce import EcommerceManager

   # In NTRLIApp.__init__:
   self.news = NewsManager()
   self.ecommerce = EcommerceManager()

   # Add navigation tabs to KV string
   ```

3. **Build and Deploy:**
   ```bash
   rm -rf ~/.buildozer app1/.buildozer
   cd app1
   buildozer android debug
   ```

4. **Test on Device:**
   - Verify news feed loads
   - Test product catalog
   - Test shopping cart functionality
   - Check 400 NOK minimum order enforcement

### Success Criteria:
- [ ] News feed displays correctly
- [ ] Products load with thumbnails
- [ ] Shopping cart works
- [ ] Pre-orders functional
- [ ] Minimum order enforced
- [ ] No crashes

---

## Phase 3: AI & Admin
**Target:** Enable advanced features

### Modules to Activate:
1. `modules/ai.py` - Claude + GPT-4 integration
2. `modules/admin.py` - Web admin panel
3. `modules/i18n.py` - Multi-language support

### Additional Dependencies Required:
```
anthropic==0.18.0
openai==1.12.0
flask==3.0.2
babel==2.14.0
```

### Integration Steps:
1. **Update `buildozer.spec`:**
   - Add AI and admin dependencies

2. **Update `main.py`:**
   ```python
   # Add imports
   from modules.ai import AIManager
   from modules.admin import AdminPanel
   from modules.i18n import I18nManager

   # In NTRLIApp.__init__:
   self.ai = AIManager()
   self.admin = AdminPanel()
   self.i18n = I18nManager()
   ```

3. **Build and Deploy:**
   ```bash
   rm -rf ~/.buildozer app1/.buildozer
   cd app1
   buildozer android debug
   ```

4. **Test on Device:**
   - Test AI queries
   - Access admin panel (admin only)
   - Switch languages
   - Verify all 20+ languages work

### Success Criteria:
- [ ] AI responds to queries
- [ ] Admin panel accessible to @Sir_NTRLI_II only
- [ ] Language switching works without restart
- [ ] All features integrated smoothly
- [ ] No crashes

---

## Emergency Rollback Procedure

If any phase causes crashes:

1. **Check crash log:**
   ```bash
   adb shell cat /sdcard/superbot_crash.log
   ```

2. **Identify failing module from traceback**

3. **Revert to previous phase:**
   - Remove new dependencies from `buildozer.spec`
   - Comment out module imports in `main.py`
   - Rebuild APK

4. **Analyze and fix:**
   - Review module code
   - Check dependency compatibility
   - Test module in isolation
   - Fix issues

5. **Retry phase after fixes**

---

## Build Environment Cleanup

Before each phase build:

```bash
# On development machine
rm -rf ~/.buildozer
rm -rf app1/.buildozer

# Via GitHub Actions (automatic with workflow)
# Uses cached dependencies but fresh build artifacts
```

---

## Testing Matrix

Each phase should be tested on:

| Android Version | API Level | Priority |
|----------------|-----------|----------|
| Android 5.0    | 21        | Medium   |
| Android 7.0    | 24        | High     |
| Android 10     | 29        | High     |
| Android 12     | 31        | Critical |

---

## Monitoring & Logs

**Device crash log location:**
```
/sdcard/superbot_crash.log
```

**How to retrieve:**
```bash
adb shell cat /sdcard/superbot_crash.log
```

**GitHub Actions build logs:**
- Navigate to Actions tab
- Click on latest workflow run
- Download build artifacts if available

---

## Current Phase Status

✅ **Phase 0:** Complete - Minimal stable version running
⏳ **Phase 1:** Ready to activate
⏳ **Phase 2:** Pending Phase 1 success
⏳ **Phase 3:** Pending Phase 2 success

---

## Notes

- **Never activate all modules at once** - causes immediate crashes
- **Always clean build environment** between phases
- **Test thoroughly** before moving to next phase
- **Keep crash logs** from each phase for analysis
- **Pin all dependency versions** to avoid conflicts
- **Use logcat** for real-time debugging: `adb logcat | grep python`

---

*Last Updated: 2025-12-18*
*Current Version: v1.0.10 (Phase 0)*
