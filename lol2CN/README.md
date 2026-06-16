# LOL 外服语言切换工具 / League of Legends Language Selector

![Version](https://img.shields.io/badge/version-1.8-blue)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)
![Java](https://img.shields.io/badge/java-17%2B-orange)

一个用于切换 **英雄联盟（League of Legends）** 外服客户端语言的桌面工具。

> 无论你玩的是哪个地区的服务器（美服、日服、欧服、东南亚服等），都可以通过本工具将客户端语言切换为你的母语。

---

## 📸 界面预览 / Preview

![主界面](screenshot.png)

简洁的 Java Swing GUI 界面，支持语言一键切换。

---

## ✨ 功能特性 / Features

- **多语言切换** — 支持 27 种语言（简体中文、繁体中文、英语、日语、韩语、法语、德语等）
- **正式服 & PBE 支持** — 同时支持正式服（Live）和测试服（PBE）的配置文件
- **开机自启** — 可选开机自动启动，自动检测并切换语言
- **配置持久化** — 自动保存语言、PBE 模式、开机自启等设置
- **版本检查** — 内置版本更新检测，一键获取最新版本
- **绿色免安装** — 打包为独立 exe，无需安装运行环境

---

## 🚀 快速开始 / Quick Start

### 下载

从 [Releases](../../releases) 页面下载最新版本的 `LOL外服语言切换工具.zip` 或 `LOL_LanguageSelector.zip`，解压即可使用。

### 直接运行

解压后双击 `lol2Chinese.exe` 即可启动。

---

## 🔧 使用说明 / Usage

1. 启动工具后，界面如下：
   - **开机自启**：勾选后将自动添加注册表启动项
   - **PBE（测试服）**：勾选后将修改 PBE 客户端语言而非正式服
   - **当前客户端语言**：显示当前 LOL 客户端的语言
   - **选择语言**：下拉选择你想要切换的目标语言

2. 选择语言后自动生效，重启 LOL 客户端即可看到效果。

### 语言列表 / Supported Languages

| 语言 | Language Code |
|------|--------------|
| 简体中文 | zh_CN |
| 繁体中文 | zh_TW |
| 英语（美国） | en_US |
| 英语（英国） | en_GB |
| 日语 | ja_JP |
| 韩语 | ko_KR |
| 法语 | fr_FR |
| 德语 | de_DE |
| ... 共 27 种语言 | ... |

---

## 📁 项目结构 / Project Structure

```
lol2CN/
├── build.bat              # 构建脚本（编译 → jar → exe → zip）
├── runtime_build.bat       # 运行时镜像构建脚本
├── 2Chinese.bat            # 辅助脚本
├── lol2Chinese.bat         # 辅助脚本
├── 常见问题.html           # FAQ 帮助页面（随 exe 一同打包）
├── conf/
│   └── config.properties   # 配置文件（语言、PBE 模式、开机自启）
└── src/
    ├── META-INF/
    │   └── MANIFEST.MF     # Jar 清单文件
    ├── gui/
    │   ├── Home.java       # 主窗口（Swing UI）
    │   └── OutputArea.java # 日志输出组件
    ├── controller/
    │   ├── LanguageController.java  # 语言切换核心逻辑
    │   └── SettingController.java   # 系统设置（开机自启注册表）
    └── util/
        ├── PropertiesConfig.java    # 配置文件读写
        ├── VersionControl.java      # 版本号 & 更新 URL
        └── Debugger.java            # 调试开关
```

---

## 🛠️ 自行构建 / Build from Source

### 前置要求 / Prerequisites

- JDK 17+
- 已在环境变量中配置 `javac`、`jar`、`jpackage`

### 构建步骤

```bash
# 1. 一键构建（编译 → 打包 jar → 生成 exe → 打包 zip）
build.bat

# 2. 或分步执行
# 编译
javac -d src\out -sourcepath src src\gui\Home.java

# 打包 jar
jar cvfm src\out\target\Home.jar src\META-INF\MANIFEST.MF -C src\out .

# 生成 exe（需要 jpackage）
jpackage --name lol2Chinese --input src\out\target --main-jar Home.jar ^
         --main-class gui.Home --type app-image --runtime-image myruntime ^
         --vendor "火花spk" --copyright "copyright 2025" --app-version 1.8
```

构建产物：
- `LOL外服语言切换工具.zip` — 中文名版本
- `LOL_LanguageSelector.zip` — 英文名版本

---

## ⚙️ 工作原理 / How It Works

本工具通过修改 Riot 客户端的语言配置文件来实现语言切换：

```
C:\ProgramData\Riot Games\Metadata\league_of_legends.live\league_of_legends.live.product_settings.yaml
```

或 PBE 路径：

```
C:\ProgramData\Riot Games\Metadata\league_of_legends.pbe\league_of_legends.pbe.product_settings.yaml
```

修改文件中的 `default_locale` 和 `locale` 字段为目标语言代码。

---

## ❓ 常见问题 / FAQ

详见打包在程序目录下的 [`常见问题.html`](常见问题.html)。

**Q: 双击 exe 一闪而过打不开？**
A: 请确保已安装 JDK 17+ 或 JRE，并检查 Windows 用户文件夹是否为中文名（可能导致路径问题）。

**Q: 切换语言后没生效？**
A: 请完全关闭 LOL 客户端后重新启动。

---

## 📄 许可证 / License

本项目仅供学习交流使用，请遵守 Riot Games 的相关条款。

Copyright © 2025 火花spk

---

## 🙏 致谢 / Acknowledgements

- 感谢所有使用和反馈问题的玩家
- 图标及素材版权归 Riot Games 所有
