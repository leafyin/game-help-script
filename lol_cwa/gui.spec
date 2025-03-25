import os
from PyInstaller.utils.hooks import collect_submodules, collect_data_files
from PyInstaller.building.build_main import Analysis, EXE, COLLECT, PYZ
funasr_path = 'C:\\Users\\Administrator.DESKTOP-GUATU1P\\AppData\\Local\\Programs\\Python\\Python39\\Lib\\site-packages\\funasr'

# 收集 funasr 和 modelscope 相关依赖
hidden_imports = collect_submodules('funasr') + collect_submodules('modelscope')

# 添加 funasr 整个目录到 datas，确保所有文件都打进去
data_files = collect_data_files('funasr') + collect_data_files('modelscope') + [(funasr_path, "funasr")]

a = Analysis([
        "gui.py"  # 主入口文件
    ],
    pathex=["."],
    hiddenimports=hidden_imports,
    datas=data_files,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name="SpeechTranslator",
    debug=False,
    strip=False,
    upx=True,
    console=True,  # GUI 应用程序
    icon=None,  # 如果有图标，可以设置
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name="SpeechTranslator"
)
