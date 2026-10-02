# -*- mode: python ; coding: utf-8 -*-

import sys

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets/fonts', 'assets/fonts'),
        ('core/prompt.txt', 'core'),
        ('.env.example', '.'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ARGUS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ARGUS',
)
app = BUNDLE(
    coll,
    name='ARGUS.app',
    icon=None,
    bundle_identifier='com.argus.desktop',
    info_plist={
        'CFBundleName': 'Argus',
        'CFBundleShortVersionString': '0.1.0',
        'CFBundleVersion': '0.1.0',
    },
) if sys.platform == 'darwin' else coll
