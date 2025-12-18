[app]
title = NTRLI SuperAPK
package.name = superapk
package.domain = org.ntrli
source.dir = .
source.include_exts = py,kv,txt

# Versioning
version = 1.0.0
version.code = 100

# Orientation
orientation = portrait

# REQUIRED PERMISSIONS
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,POST_NOTIFICATIONS

# ANDROID API TARGET
android.api = 35
android.minapi = 21
android.sdk = 35
android.ndk = 25b

# REQUIREMENTS — only proven Android buildable deps
requirements = python3==3.11.8,kivy==2.3.1,kivymd==1.1.1,pillow==10.2.0,certifi,openssl

# ENTRYPOINT
entrypoint = main.py

# BUILD OPTIONS
fullscreen = 0
log_level = 2
clean_build = True

# Archs (standard)
android.archs = arm64-v8a,armeabi-v7a

# INCLUDE SOURCES
android.include_src = True