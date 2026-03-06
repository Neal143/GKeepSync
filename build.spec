# -*- mode: python ; coding: utf-8 -*-
"""
GKeepSync PyInstaller Build Spec
Build command: pyinstaller build.spec
"""

import os
import importlib.metadata
import customtkinter

block_cipher = None

# Get customtkinter data path
ctk_path = os.path.dirname(customtkinter.__file__)

# Collect dist-info metadata for packages that need it
def get_dist_info(pkg_name):
    """Get the dist-info directory path for a package."""
    try:
        dist = importlib.metadata.distribution(pkg_name)
        return (str(dist._path), str(dist._path.name))
    except Exception:
        return None

# Packages that need their metadata included
metadata_packages = ['gpsoauth', 'gkeepapi', 'future', 'requests', 'pycryptodomex']
metadata_datas = []
for pkg in metadata_packages:
    info = get_dist_info(pkg)
    if info:
        metadata_datas.append(info)

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        (ctk_path, 'customtkinter/'),
    ] + metadata_datas,
    hiddenimports=[
        'gkeepapi',
        'gpsoauth',
        'customtkinter',
        'pycryptodomex',
        'Cryptodome',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='GKeepSync',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
