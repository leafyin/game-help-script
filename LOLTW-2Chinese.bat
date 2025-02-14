@echo off

chcp 65001
setlocal enabledelayedexpansion

set filepath=C:\ProgramData\Riot Games\Metadata\league_of_legends.live
set filename=C:\ProgramData\Riot Games\Metadata\league_of_legends.live\league_of_legends.live.product_settings.yaml
set output_file=D:\league_of_legends.live.product_settings.yaml

set /p user_input=请选择需要汉化的语言(0.繁体中文，1.日语，2.韩文，3.英文):
set search_line=    locale: "zh_TW"
if "%user_input%"=="1" (
    set search_line=    locale: "ja_JP"
)
if "%user_input%"=="2" (
    set search_line=    locale: "ko_KR"
)
if "%user_input%"=="3" (
    set search_line=    locale: "en_US"
)
echo %search_line%
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