# encoding=utf-8
"""
打包脚本 — 使用 PyInstaller 将项目打包为单个 exe

使用方法：
    python build.py                    # 全量打包（含语音识别）
    python build.py --image-only       # 仅打包划区识图翻译

注意：
    - 需要在 Windows 上运行（PyInstaller 仅支持打包为当前系统的可执行文件）
    - 需要提前安装 Tesseract-OCR，或把 tesseract.exe 放在 src/Tesseract-OCR/ 下
    - 语音识别模型体积很大，首次运行时会自动下载
"""

import os
import sys
import shutil
import subprocess
import argparse

# ============================================================
# 项目路径
# ============================================================
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(PROJECT_ROOT, 'src')
DIST_DIR = os.path.join(PROJECT_ROOT, 'dist')
BUILD_DIR = os.path.join(PROJECT_ROOT, 'build')
SPEC_FILE = os.path.join(PROJECT_ROOT, 'lol_cwa.spec')


def check_prerequisites():
    """检查打包前置条件"""
    print("=" * 60)
    print("检查前置条件...")
    print("=" * 60)

    # 检查 Python
    py = shutil.which('python') or shutil.which('python3')
    if not py:
        print("[✗] 未找到 Python，请先安装 Python 3.8+")
        sys.exit(1)
    print(f"[✓] Python: {py}")

    # 检查 PyInstaller
    try:
        import PyInstaller
        print(f"[✓] PyInstaller: {PyInstaller.__version__}")
    except ImportError:
        print("[···] 未安装 PyInstaller，正在安装...")
        subprocess.check_call([py, '-m', 'pip', 'install', 'pyinstaller'])
        print("[✓] PyInstaller 安装完成")

    # 检查 Tesseract-OCR
    tess_exe = os.path.join(SRC_DIR, 'Tesseract-OCR', 'tesseract.exe')
    if not os.path.exists(tess_exe):
        print(f"[!] 未找到 Tesseract-OCR: {tess_exe}")
        print("    ├─ 请下载 Tesseract-OCR 并解压到 src/Tesseract-OCR/")
        print("    └─ 下载地址: https://github.com/UB-Mannheim/tesseract/wiki")
        print("    （打包会继续，但 exe 运行时会找不到 tesseract.exe）")
    else:
        print(f"[✓] Tesseract-OCR: {tess_exe}")

    # 检查 tessdata
    tessdata_dir = os.path.join(SRC_DIR, 'tessdata')
    if not os.path.exists(tessdata_dir) or not os.listdir(tessdata_dir):
        print(f"[!] tessdata 目录为空或不存在: {tessdata_dir}")
        print("    └─ 请将 eng.traineddata / chi_sim.traineddata 等文件放入 src/tessdata/")
    else:
        files = [f for f in os.listdir(tessdata_dir) if f.endswith('.traineddata')]
        print(f"[✓] tessdata: {len(files)} 个语言包 ({', '.join(files)})")

    return py


def get_hidden_imports(image_only: bool) -> list:
    """
    获取 PyInstaller 需要显式指定的隐藏导入
    PyInstaller 有时无法自动发现某些动态导入的模块
    """
    imports = [
        'tkinter',
        'tkinter.ttk',
        'PIL',
        'PIL.Image',
        'PIL.ImageGrab',
        'pytesseract',
        'requests',
        'hashlib',
        'random',
    ]
    if not image_only:
        imports += [
            'modelscope',
            'funasr',
            'numpy',
            'pyaudio',
            'keyboard',
        ]
    return imports


def get_data_files() -> list:
    """
    返回需要打包进 exe 的额外数据文件
    格式: [(源路径, 目标目录)]
    """
    data_files = []

    # tessdata 目录
    tessdata_src = os.path.join(SRC_DIR, 'tessdata')
    if os.path.exists(tessdata_src):
        data_files.append((tessdata_src, 'tessdata'))

    # Tesseract-OCR 目录（整个目录塞进去）
    tess_ocr_src = os.path.join(SRC_DIR, 'Tesseract-OCR')
    if os.path.exists(tess_ocr_src):
        data_files.append((tess_ocr_src, 'Tesseract-OCR'))

    return data_files


def build(image_only: bool):
    """执行打包"""
    print("\n" + "=" * 60)
    print("开始打包..." + ("（仅划区识图翻译）" if image_only else "（全量含语音识别）"))
    print("=" * 60)

    py = check_prerequisites()
    hidden_imports = get_hidden_imports(image_only)
    data_files = get_data_files()

    # 构建 PyInstaller 命令
    cmd = [
        py, '-m', 'PyInstaller',
        '--clean',
        '--noconfirm',
        '--onefile',                    # 单个 exe
        '--windowed',                   # 无控制台窗口（GUI 模式）
        '--name', '火花工具箱',
        '--distpath', DIST_DIR,
        '--workpath', BUILD_DIR,
        '--specpath', PROJECT_ROOT,
        '--add-data', f'{os.path.join(SRC_DIR, "tessdata")}{os.pathsep}tessdata',
    ]

    # 添加隐藏导入
    for mod in hidden_imports:
        cmd.extend(['--hidden-import', mod])

    # 添加数据文件（Tesseract-OCR）
    tess_ocr_src = os.path.join(SRC_DIR, 'Tesseract-OCR')
    if os.path.exists(tess_ocr_src):
        cmd.extend(['--add-data', f'{tess_ocr_src}{os.pathsep}Tesseract-OCR'])

    # 主入口
    main_entry = os.path.join(SRC_DIR, 'main.py')
    cmd.append(main_entry)

    print("\n执行命令:")
    print(" ".join(cmd))
    print()

    # 运行 PyInstaller
    result = subprocess.run(cmd, cwd=PROJECT_ROOT)

    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("[✓] 打包成功！")
        print(f"    输出目录: {DIST_DIR}")
        # 找到生成的 exe
        exe_name = '火花工具箱.exe'
        exe_path = os.path.join(DIST_DIR, exe_name)
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"    文件: {exe_path} ({size_mb:.1f} MB)")
        print("=" * 60)
    else:
        print(f"\n[✗] 打包失败，错误码: {result.returncode}")
        sys.exit(result.returncode)


def clean():
    """清理打包中间产物"""
    print("清理打包中间产物...")
    for d in [BUILD_DIR]:
        if os.path.exists(d):
            shutil.rmtree(d)
            print(f"  删除: {d}")
    spec = os.path.join(PROJECT_ROOT, '火花工具箱.spec')
    if os.path.exists(spec):
        os.remove(spec)
        print(f"  删除: {spec}")
    print("[✓] 清理完成")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='打包 火花工具箱 为 exe')
    parser.add_argument('--image-only', action='store_true', help='仅打包划区识图翻译（不含语音识别）')
    parser.add_argument('--clean', action='store_true', help='清理打包中间产物')
    args = parser.parse_args()

    if args.clean:
        clean()
    else:
        build(image_only=args.image_only)
