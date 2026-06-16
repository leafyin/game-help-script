# 游戏帮助脚本、工具

> 游戏辅助工具箱，包含截图翻译和语音翻译（Python）、LOL外服语言切换（Java）等多个实用工具。

---

## 📦 项目一览

| 项目 | 说明 | 技术栈 |
|------|------|--------|
| `lol_cwa/` | 火花spk工具箱 — 划区识图翻译 + 语音识别翻译 | Python / tkinter |
| `lol2CN/` | LOL外服语言切换 — 一键切换英雄联盟客户端语言 | Java / Swing |

---

## 🪄 lol_cwa — 火花spk工具箱

### 功能

#### 🖼️ 划区识图翻译
1. 用半透明窗口覆盖游戏/屏幕中需要翻译的区域
2. 自动循环截图 → OCR 文字识别 → 百度翻译 → 显示译文
3. 相同/相似内容自动去重，不重复翻译
4. 翻译缓存，相同文本避免重复调用 API

#### 🎤 语音识别翻译
1. 加载 FunASR 语音识别模型，实时识别麦克风输入
2. 自动翻译为指定语言
3. 浮动翻译窗口，支持按键绑定和回车快速发送译文

### 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 运行
cd src && python main.py
```

> **macOS 额外步骤**：`pyaudio` 可能需要 `brew install portaudio`
>
> **Tesseract-OCR**：需手动安装，详见 `lol_cwa/README.md`

### 打包 exe

```bash
python build.py              # 全量打包（含语音识别）
python build.py --image-only # 仅打包划区识图翻译
```

> 打包需在 **Windows** 上运行。

### 支持翻译的语言

中文、繁体中文、英语、粤语、文言文、日语、韩语、法语、西班牙语、泰语、阿拉伯语、俄语、葡萄牙语、德语、意大利语、希腊语、荷兰语、波兰语、保加利亚语、爱沙尼亚语、丹麦语、芬兰语、捷克语、罗马尼亚语、斯洛文尼亚语、瑞典语、匈牙利语、越南语

> 详尽的说明请移步 `lol_cwa/README.md`

---

## 🌐 lol2CN — LOL 外服语言切换工具

英雄联盟外服客户端语言切换工具（Java桌面应用），编译需要 **JDK 17+**。

### 功能简介

- 一键切换 LOL 外服客户端语言（支持 27 种语言）
- 支持 **正式服（Live）** 和 **PBE 测试服**
- 开机自启，自动检测并切换语言
- 配置持久化，内置版本检查更新

### 使用方法

1. 从 Releases 下载最新版，解压运行 `lol2Chinese.exe`
2. 选择语言后自动生效，重启 LOL 客户端即可看到效果

> **macOS 用户**：请打开 Terminal 执行以下命令启动游戏并汉化：
> ```bash
> open /Applications/League\ of\ Legends.app --args --locale=zh_CN
> ```
> 也可下载 [快捷指令](https://www.icloud.com/shortcuts/883b5848b84b4e7089beb903d05af3df) 快速启动

### 自行构建

```bash
cd lol2CN
build.bat
```

> 详尽的说明请移步 `lol2CN/README.md`
