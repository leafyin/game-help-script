# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.building.datastruct import Tree


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
src_root = os.path.join(project_root, 'src')

hiddenimports = []
hiddenimports += collect_submodules('funasr')
hiddenimports += collect_submodules('modelscope')
hiddenimports += [
    'pytesseract',
    'PIL.Image',
    'PIL.ImageGrab',
    'PIL.ImageTk',
    'PIL._tkinter_finder',
    'huggingface_hub',
    'fastapi',
    'uvicorn',
    'torch',
    'torchaudio',
]

datas = [
    (os.path.join(project_root, 'config.json'), '.'),
    Tree(os.path.join(src_root, 'tessdata'), prefix='tessdata'),
]

# 如果项目中包含 Tesseract-OCR 目录，也一起打包进去
tesseract_dir = os.path.join(src_root, 'Tesseract-OCR')
if os.path.exists(tesseract_dir):
    datas.append(Tree(tesseract_dir, prefix='Tesseract-OCR'))


a = Analysis(
    [os.path.join(src_root, 'gui.py')],
    pathex=[src_root],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
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
    name='gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
app = BUNDLE(
    exe,
    name='gui.app',
    icon=None,
    bundle_identifier=None,
)
