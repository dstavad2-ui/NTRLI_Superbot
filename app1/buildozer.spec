[app]

# Basic app info
title = NTRLI Superbot
package.name = ntrli_superbot
package.domain = org.ntrli

# Source configuration
source.dir = .
source.include_exts = py,png,jpg,kv,json

# Icon and presplash
presplash.filename = %(source.dir)s/images/presplash.png
icon.filename = %(source.dir)s/images/icon.png

# Version
version = 1.0.12

# Requirements - PINNED VERSIONS (validated for Android)
# Only include dependencies proven to build with python-for-android
requirements = python3,kivy==2.3.1,kivymd==1.1.1,aiohttp

# Orientation
orientation = portrait
fullscreen = 0

# Android permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# Android API versions (validated)
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.accept_sdk_license = True

# Android archs
android.archs = arm64-v8a,armeabi-v7a

# Enable AndroidX
android.enable_androidx = True

# Gradle dependencies
android.gradle_dependencies = com.google.android.material:material:1.6.0

[buildozer]

# Log level (2 = debug for crash investigation)
log_level = 2
warn_on_root = 1
