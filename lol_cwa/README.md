# 火花spk工具箱

划区识图翻译 + 语音识别翻译，双功能桌面工具。

---

## 功能

### 🖼️ 划区识图翻译
1. 用半透明窗口覆盖游戏/屏幕中需要翻译的区域
2. 自动循环截图 → OCR 文字识别 → 百度翻译 → 显示译文
3. 相同/相似内容自动去重，不重复翻译
4. 翻译缓存，相同文本避免重复调用 API

### 🎤 语音识别翻译
1. 加载 FunASR 语音识别模型，实时识别麦克风输入
2. 自动翻译为指定语言
3. 浮动翻译窗口，支持按键绑定

---

## 项目结构

```
├── build.py                      # 打包脚本（PyInstaller）
├── requirements.txt              # Python 依赖
├── README.md
│
└── src/
    ├── main.py                   # 🚀 入口
    │
    ├── ui/                       # 🎨 UI 层
    │   ├── main_window.py        #   主窗口（标签页导航）
    │   ├── image_translate_view.py   #   划区识图翻译界面
    │   └── speech_translate_view.py  #   语音识别翻译界面
    │
    ├── service/                  # ⚙️ 业务逻辑层
    │   ├── config.py             #   配置持久化
    │   ├── translator.py         #   百度翻译 API + 语言映射 + 缓存
    │   ├── ocr.py                #   OCR 文字识别（pytesseract）
    │   ├── image_capture.py      #   屏幕截图
    │   └── speech_recognizer.py  #   语音识别模型 + 音频监听
    │
    ├── tessdata/                 # 📖 Tesseract 语言包
    │   ├── eng.traineddata
    │   ├── chi_sim.traineddata
    │   ├── jpn.traineddata
    │   └── kor.traineddata
    │
    └── utils.py                  # 🔧 通用工具
```

---

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

> **macOS 额外步骤**：`pyaudio` 可能需要 `brew install portaudio`
>
> **Tesseract-OCR**：需手动安装，下载后放入 `src/Tesseract-OCR/` 目录
> - Windows: https://github.com/UB-Mannheim/tesseract/wiki
> - macOS: `brew install tesseract`
> - 并确保 `src/tessdata/` 下有对应的 `.traineddata` 语言包

### 2. 运行

```bash
cd src
python main.py
```

### 3. 打包为 exe

```bash
# 全量打包（含语音识别）
python build.py

# 仅打包划区识图翻译
python build.py --image-only

# 清理中间产物
python build.py --clean
```

> 打包需要在 **Windows** 上运行（PyInstaller 只能打包当前系统的可执行文件）。

---

## 技术栈

| 模块 | 技术 |
|---|---|
| UI 框架 | tkinter / ttk |
| OCR 识别 | pytesseract + Tesseract-OCR |
| 文本翻译 | 百度翻译 API |
| 语音识别 | FunASR (funasr + modelscope) |
| 屏幕截图 | PIL (ImageGrab) |
| 打包工具 | PyInstaller |

---

## 注意事项

- **百度翻译 API**：代码中内置了测试用的 `appid` 和 `private_key`，建议替换为你自己的（在 `service/translator.py` 中修改 `APP_ID` 和 `PRIVATE_KEY`）
- **语音识别模型**：首次使用需在界面中选择模型保存路径并点击"下载"，模型约几百 MB
- **OCR 语言包**：`tessdata/` 已包含英/中/日/韩文包，如需其他语言请自行下载
