# -*- mode: python ; coding: utf-8 -*-
# Auto-generated spec file for Genie GitHooks

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
    hooksconfig={},
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
    name='GenieGitHooks',
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
    entitlements_file=None,
)

# Create app bundle on macOS
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='GenieGitHooks.app',
        bundle_identifier='com.bilvantis.genie-githooks',
        info_plist={
            'CFBundleName': 'Genie GitHooks',
            'CFBundleDisplayName': 'Genie GitHooks',
            'CFBundleVersion': '2.0.0',
            'CFBundleShortVersionString': '2.0.0',
            'NSHighResolutionCapable': 'True',
            'LSBackgroundOnly': 'False',
            'NSPrincipalClass': 'NSApplication',
            'NSRequiresAquaSystemAppearance': 'False',
            'LSApplicationCategoryType': 'public.app-category.developer-tools',
            'NSHumanReadableCopyright': '© 2024 Bilvantis. All rights reserved.'
        }
    )
