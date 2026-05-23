[app]
title = HealthMate
package.name = healthmate
package.domain = org.yourdomain

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,ttf

version = 1.0

requirements = python3,kivy

orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.arch = arm64-v8a
android.accept_sdk_license = True

p4a.branch = master
