@echo off

@rem 编译
javac -d src\out src\gui\LOL_2_Chinese.java

@rem jar包
jar cvfm LOL_2_Chinese.jar src\META-INF\MANIFEST.MF -C src\out .

jpackage --name lol2Chinese --input E:\game-help-script\build_result --main-jar E:\game-help-script\exe\LOL_2_Chinese.jar --main-class gui.LOL_2_Chinese.Main --type app-image --runtime-image myruntime --verbose

pause