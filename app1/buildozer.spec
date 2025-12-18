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
version = 1.0

# Requirements - PINNED VERSIONS to avoid conflicts
requirements = python3,kivy==2.3.1,kivymd==1.1.1

# Orientation
orientation = portrait
fullscreen = 0

# Android permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# Android API versions
android.api = 31
android.minapi = 21
android.ndk = 25b
android.sdk = 31
android.accept_sdk_license = True

# Android archs
android.archs = arm64-v8a,armeabi-v7a

# Enable AndroidX
android.enable_androidx = True

# Gradle dependencies
android.gradle_dependencies = com.google.android.material:material:1.6.0

[buildozer]

# Log level
log_level = 2
warn_on_root = 1
