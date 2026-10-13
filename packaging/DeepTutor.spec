# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path

ROOT = Path('/Users/f/deeptutor')

datas = [
    (str(ROOT / 'deeptutor_web/.next/static'), './deeptutor_web/.next/static'),
    (str(ROOT / 'deeptutor_web/.next/server'), './deeptutor_web/.next/server'),
    (str(ROOT / 'deeptutor_web/public'), './deeptutor_web/public'),
    (str(ROOT / 'deeptutor_web/node_modules'), './deeptutor_web/node_modules'),
    (str(ROOT / 'deeptutor_web/server.js'), './'),
    (str(ROOT / 'deeptutor_web/package.json'), './deeptutor_web/package.json'),
    (str(ROOT / 'deeptutor_web/BUILD_INFO'), './deeptutor_web/BUILD_INFO'),
]
hiddenimports = [
    'deeptutor',
    'deeptutor_cli',
    'deeptutor.agents.research.meta_analysis',
    'deeptutor.agents.research.meta_analysis.capability',
    'deeptutor.agents.research.meta_analysis.request_config',
]

a = Analysis(
    [str(ROOT / 'deeptutor_cli/main.py')],
    pathex=[str(ROOT)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='DeepTutor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='DeepTutor',
)
app = BUNDLE(
    coll,
    name='DeepTutor.app',
    icon=str(ROOT / 'deeptutor_web/public/logo.png'),
    info_plist={
        'CFBundleIdentifier': 'ai.local.deeptutor',
        'CFBundleName': 'DeepTutor',
        'CFBundleDisplayName': 'DeepTutor',
        'CFBundlePackageType': 'APPL',
        'CFBundleShortVersionString': '1.6.11',
        'CFBundleVersion': '1',
        'LSMinimumSystemVersion': '13.0',
        'NSHighResolutionCapable': True,
    },
    bundle_identifier='ai.local.deeptutor',
)
