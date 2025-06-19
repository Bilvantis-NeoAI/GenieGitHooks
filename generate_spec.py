import os
import sys

print("Generating PyInstaller spec file for Genie- Commit Review...")

# Check if icon files exist
icon_ico = 'icon.ico' if os.path.exists('icon.ico') else None
icon_icns = 'icon.icns' if os.path.exists('icon.icns') else None

# Build the spec content
spec_content = f'''# -*- mode: python ; coding: utf-8 -*-
# Auto-generated spec file for Genie- Commit Review

import sys

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('hooks', 'hooks'),  # Include the hooks directory
    ],
    hiddenimports=[
        'PySide6.QtWidgets',
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtNetwork',
        'requests',
        'subprocess',
        'traceback',
        'logging',
        'platform',
        'pkg_resources.py2_warn'
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[
        'PySide6.QtWebEngineCore', 
        'PySide6.QtWebEngineWidgets', 
        'PySide6.QtWebEngine',
        'matplotlib',
        'numpy',
        'scipy'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GenieCommitReview',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=True,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,{f"""
    icon='{icon_ico}'""" if icon_ico else ""}
)

# Create app bundle on macOS
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='GenieCommitReview.app',{f"""
        icon='{icon_icns}',""" if icon_icns else ""}
        bundle_identifier='com.bilvantis.genie-githooks',
        info_plist={{
            'CFBundleName': 'Genie- Commit Review',
            'CFBundleDisplayName': 'Genie- Commit Review',
            'CFBundleVersion': '2.0.0',
            'CFBundleShortVersionString': '2.0.0',
            'NSHighResolutionCapable': 'True',
            'LSBackgroundOnly': 'False',
            'NSPrincipalClass': 'NSApplication',
            'NSRequiresAquaSystemAppearance': 'False',
            'LSApplicationCategoryType': 'public.app-category.developer-tools',
            'NSHumanReadableCopyright': '2025 Bilvantis. All rights reserved.'
        }}
    )
'''

# Write the spec file
with open('genie-commit-review.spec', 'w') as f:
    f.write(spec_content)

print("✅ PyInstaller spec file generated: genie-commit-review.spec")

if icon_ico:
    print(f"📎 Using Windows icon: {icon_ico}")
else:
    print("⚠️  No icon.ico found - using default icon for Windows")
    
if icon_icns:
    print(f"📎 Using macOS icon: {icon_icns}")
else:
    print("⚠️  No icon.icns found - using default icon for macOS") 