@echo off

chcp 65001
setlocal enabledelayedexpansion

set filepath=C:\ProgramData\Riot Games\Metadata\league_of_legends.live
set filename=C:\ProgramData\Riot Games\Metadata\league_of_legends.live\league_of_legends.live.product_settings.yaml
set output_file=D:\league_of_legends.live.product_settings.yaml

echo 重置权限
set lang_tw=    locale: "zh_TW"
set lang_us=    locale: "en_US"
set lang_jp=    locale: "ja_JP"
set lang_kr=    locale: "ko_KR"
set replace_line=    locale: "zh_CN"

if not exist "%filename%" (
    echo "文件 %filename% 不存在。"
    goto :EOF
)

> "%output_file%" (
    for /f "delims=" %%i in ('type "%filename%"') do (
        set line=%%i
        if "!line!"=="%lang_tw%" (
            echo %replace_line%
        ) else if "!line!"=="%lang_us%" (
            echo %replace_line%
        ) else if "!line!"=="%lang_jp%" (
            echo %replace_line%
        ) else if "!line!"=="%lang_kr%" (
            echo %replace_line%
        ) else (
            echo !line!
        )
    )
)

copy /y "%output_file%" "%filepath%"
del "%output_file%"
echo 汉化完成！
pause