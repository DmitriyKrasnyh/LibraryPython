# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['build.py'],
    pathex=[],
    binaries=[],
    datas=[('index.html', '.'), ('theory.html', '.'), ('practice.html', '.'), ('testing.html', '.'), ('reference.html', '.'), ('admin.html', '.'), ('admin.js', '.'), ('styles.css', '.'), ('chapter1.pdf', '.'), ('chapter2.pdf', '.'), ('chapter3.pdf', '.'), ('chapter4.pdf', '.'), ('chapter5.pdf', '.'), ('chapter6.pdf', '.'), ('chapter7.pdf', '.'), ('chapter8.pdf', '.'), ('chapter9.pdf', '.'), ('chapter10.pdf', '.'), ('lab1.pdf', '.'), ('lab2.pdf', '.'), ('spravka.pdf', '.'), ('вопросики', '.'), ('requirements.txt', '.')],
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
    a.binaries,
    a.datas,
    [],
    name='build',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
