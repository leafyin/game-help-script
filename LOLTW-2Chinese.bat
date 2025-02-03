@echo off

chcp 65001
setlocal enabledelayedexpansion

set filepath=C:\ProgramData\Riot Games\Metadata\league_of_legends.live
set filename=C:\ProgramData\Riot Games\Metadata\league_of_legends.live\league_of_legends.live.product_settings.yaml
set output_file=D:\league_of_legends.live.product_settings.yaml
set search_line=    locale: "zh_TW"
set replace_line=    locale: "zh_CN"

echo "确保你有D盘,该程序是用D盘存放临时文件"
pause

if not exist "%filename%" (
    echo "文件 %filename% 不存在。"
    goto :EOF
)

> "%output_file%" (
    for /f "delims=" %%i in ('type "%filename%"') do (
        set line=%%i
        if "!line!"=="%search_line%" (
            echo %replace_line%
        ) else (
            echo !line!
        )
    )
)
copy /y "%output_file%" "%filepath%"
del "%output_file%"
echo "汉化完成！"
pause