@echo off

chcp 65001

@rem 编译
javac -d src\out src\gui\LOL_2_Chinese.java

@rem jar包
jar cvfm src\out\target\LOL_2_Chinese.jar src\META-INF\MANIFEST.MF -C src\out .

jpackage --name lol2Chinese --input E:\game-help-script\lol2CN\src\out\target --main-jar LOL_2_Chinese.jar --main-class gui.LOL_2_Chinese --type app-image --runtime-image myruntime --verbose

@rem package
copy 常见问题.html lol2Chinese\
tar -a -c -f "LOL外服语言切换工具.zip" "lol2Chinese"
tar -a -c -f "LOL_LanguageChanger.zip" "lol2Chinese"

pause