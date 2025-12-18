[app]
title = NTRLI Superbot
package.name = ntrli_superbot
package.domain = org.ntrli

source.dir = .
source.include_exts = py,png,jpg,kv

# Icon and presplash
presplash.filename = %(source.dir)s/images/presplash.png
icon.filename = %(source.dir)s/images/icon.png

# versioning
version = 1.0

# REQUIRED: basic requirements
requirements = python3,kivy

# Optional additional modules
# Only add these if you have recipes for them:
# openai, requests

orientation = portrait

# Permissions
android.permissions = INTERNET

[buildozer]
log_level = 2

# Android archs
android.archs = arm64-v8a, armeabi-v7a
