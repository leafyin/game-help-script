@echo off

chcp 65001

set version=1.7

@rem clean
dir /b *.zip >nul 2>&1
if errorlevel 1 (
    echo no file to clean !
) else (
    attrib -R lol2Chinese\* /S /D
    del /f /s /q lol2Chinese\* *.zip
    rd /s /q lol2Chinese
    echo file has been cleaned !
)

@rem 编译
javac -d src\out -sourcepath src src\gui\Home.java

@rem jar
jar cvfm src\out\target\Home.jar src\META-INF\MANIFEST.MF -C src\out .

@rem exe
jpackage --name lol2Chinese --input E:\game-help-script\lol2CN\src\out\target --main-jar Home.jar --java-options "-Djpackager.useUPX=false" --main-class gui.Home --type app-image --runtime-image myruntime --vendor "火花spk" --copyright "copyright 2025" --app-version %version% --verbose

@rem zip
copy 常见问题.html lol2Chinese\
tar -a -c -f "LOL外服语言切换工具.zip" "lol2Chinese"
tar -a -c -f "LOL_LanguageChanger.zip" "lol2Chinese"

pause