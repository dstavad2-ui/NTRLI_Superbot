[app]

# (str) Title of your application
title = NTRLI SuperAPK

# (str) Package name
package.name = superapk

# (str) Package domain (needed for android/ios packaging)
package.domain = org.ntrli

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,txt,json

# (str) Application versioning (method 1)
version = 1.0.10

# (int) Application versioning (method 2)
version.code = 10

# (list) Application requirements
# PHASE 0: Minimal stable
requirements = python3==3.11.8,kivy==2.3.1,kivymd==1.1.1

# PHASE 1: Add these after Phase 0 works
# requests==2.31.0,pysocks==1.7.1,cryptography==41.0.7

# PHASE 2: Add these after Phase 1 works
# feedparser==6.0.10,pillow==10.2.0,sqlalchemy==2.0.25

# PHASE 3: Add these after Phase 2 works
# flask==3.0.2,anthropic==0.18.0,openai==1.12.0,babel==2.14.0

# (str) Custom source folders for requirements
# requirements.source.kivy = ../../kivy

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/assets/presplash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/assets/icon.png

# (str) Supported orientation (landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
android.fullscreen = 0

# (list) Permissions
# PHASE 0:
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# PHASE 2: Add POST_NOTIFICATIONS

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 33

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android entry point, default is ok for Kivy-based app
# android.entrypoint = org.kivy.android.PythonActivity

# (str) Full name including package path of the Java class that implements Android Activity
# android.activity_class_name = org.kivy.android.PythonActivity

# (str) Extra xml to write directly inside the <manifest> element of AndroidManifest.xml
# android.extra_manifest_xml = 

# (str) Extra xml to write directly inside the <application> element of AndroidManifest.xml
# android.extra_manifest_application_xml = 

# (list) Pattern to whitelist for the whole project
# android.whitelist =

# (str) Path to a custom whitelist file
# android.whitelist_src =

# (str) Path to a custom blacklist file
# android.blacklist_src =

# (bool) If True, then skip trying to update the Android sdk
# android.skip_update = False

# (bool) If True, then automatically accept SDK license agreements
android.accept_sdk_license = True

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (str) The Android arch to build for
android.archs = arm64-v8a,armeabi-v7a

#
# Python for android (p4a) specific
#

# (str) python-for-android fork to use, defaults to upstream (kivy)
# p4a.fork = kivy

# (str) python-for-android branch to use, defaults to master
# p4a.branch = master

# (str) python-for-android git clone directory (if empty, it will be automatically cloned from github)
# p4a.source_dir =

# (str) The directory in which python-for-android should look for your own build recipes (if any)
# p4a.local_recipes =

# (str) Filename to the hook for p4a
# p4a.hook =

# (str) Bootstrap to use for android builds
# p4a.bootstrap = sdl2

# (int) port number to specify an explicit --port= p4a argument (eg for bootstrap flask)
# p4a.port =

# (str) python-for-android url to use for checkout
# p4a.url =

#
# iOS specific
#

# (str) Path to a custom kivy-ios folder
# ios.kivy_ios_dir = ../kivy-ios

# (str) Name of the certificate to use for signing the debug version
# ios.codesign.debug = "iPhone Developer: <lastname> <firstname> (<hexstring>)"

#
# Buildozer
#

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 0

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .ipa) storage
# bin_dir = ./bin

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 0