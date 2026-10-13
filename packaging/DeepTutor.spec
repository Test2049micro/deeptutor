# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

#: Repo root, relative to this spec so the build works from any clone.
#: Override with DEEPTUTOR_SPEC_ROOT to build an out-of-tree checkout.
#: PyInstaller injects SPECPATH (the spec file's directory) into the namespace.
SPEC_PATH = Path(globals().get('SPECPATH') or Path.cwd())
ROOT = Path(os.environ.get('DEEPTUTOR_SPEC_ROOT', SPEC_PATH.resolve().parent))

datas = [
    (str(ROOT / 'deeptutor_web/.next'), './deeptutor_web/.next'),
    (str(ROOT / 'deeptutor_web/public'), './deeptutor_web/public'),
    (str(ROOT / 'deeptutor_web/node_modules'), './deeptutor_web/node_modules'),
    (str(ROOT / 'deeptutor_web/server.js'), './deeptutor_web/'),
    (str(ROOT / 'deeptutor_web/package.json'), './deeptutor_web/package.json'),
    (str(ROOT / 'deeptutor_web/BUILD_INFO'), './deeptutor_web/BUILD_INFO'),
    # Default LLM pool + system settings, seeded into a fresh runtime home.
    (str(ROOT / 'packaging/default-settings'), './packaging/default-settings'),
    # Prompt/template data (yaml/md/json) inside the deeptutor package.
    *collect_data_files('deeptutor'),
]
hiddenimports = [
    'deeptutor',
    'deeptutor_cli',
    'deeptutor.agents.research.meta_analysis',
    'deeptutor.agents.research.meta_analysis.capability',
    'deeptutor.agents.research.meta_analysis.request_config',
    'deeptutor.api.main',
    'deeptutor.runtime.worker_process',
    'deeptutor.runtime.update_worker',
    'uvicorn',
    'uvicorn.logging',
    'uvicorn.loops',
    'uvicorn.loops.auto',
    'uvicorn.protocols',
    'uvicorn.protocols.http',
    'uvicorn.protocols.http.auto',
    'uvicorn.protocols.websockets',
    'uvicorn.protocols.websockets.auto',
    'uvicorn.lifespan',
    'uvicorn.lifespan.on',
    'runpy',
] + collect_submodules('deeptutor')

a = Analysis(
    [str(ROOT / '_run.py')],
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
