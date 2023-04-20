# -*- mode: python ; coding: utf-8 -*-
import shutil

from PyInstaller.utils.hooks import copy_metadata

block_cipher = None
datas = [
    *copy_metadata('numpy'),
    (shutil.which('ffmpeg'), '.'),
    ('asset/*', 'asset'),
    ]


a = Analysis(['ear/gui.py'],
             pathex=["./ear"],
             binaries=[],
             datas=datas,
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          name='ear',
          icon='asset/ear.png',
            exclude_binaries=True,
            debug=True,
            bootloader_ignore_signals=False,
            strip=False,
            upx=True,
            console=True,
            disable_windowed_traceback=False,
            argv_emulation=False,
            target_arch=None,
            codesign_identity=None,
            entitlements_file=None,
          )

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='ear',
)
app = BUNDLE(
    coll,
    name='ear.app',
    icon='./asset/ear.icns',
    bundle_identifier='jun.jiang.ear',
    version='0.0.1',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSHighResolutionCapable': 'True',
        'NSMicrophoneUsageDescription': 'Allow ear to capture audio from your microphone.'
    }
)
