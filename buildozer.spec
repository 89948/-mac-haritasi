[app]

title = Maç Haritası

package.name = macharitasi
package.domain = org.macharitasi

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,ttf
source.exclude_dirs = .git,.github,.buildozer,bin,__pycache__

version = 0.1.0

requirements = python3,kivy==2.3.1

orientation = portrait
fullscreen = 0

android.api = 35
android.minapi = 23
android.ndk = 25b
android.archs = arm64-v8a

android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 1
