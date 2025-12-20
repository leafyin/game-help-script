@echo off
chcp 65001
setlocal enabledelayedexpansion

:: 设置文件路径
set filepath=C:\ProgramData\Riot Games\Metadata\league_of_legends.live
set filename=C:\ProgramData\Riot Games\Metadata\league_of_legends.live\league_of_legends.live.product_settings.yaml
set output_file=D:\league_of_legends.live.product_settings.yaml
set log_file=D:\lol_hanhua_log.txt

:: 所有需要替换的语言
set lang_tw=    locale: "zh_TW"
set lang_us=    locale: "en_US"
set lang_jp=    locale: "ja_JP"
set lang_kr=    locale: "ko_KR"
set lang_ar_ae=    locale: "ar_AE"
set lang_id_id=    locale: "id_ID"
set lang_cs_cz=    locale: "cs_CZ"
set lang_de_de=    locale: "de_DE"
set lang_el_gr=    locale: "el_GR"
set lang_en_au=    locale: "en_AU"
set lang_en_gb=    locale: "en_GB"
set lang_en_ph=    locale: "en_PH"
set lang_en_sg=    locale: "en_SG"
set lang_es_ar=    locale: "es_AR"
set lang_es_es=    locale: "es_ES"
set lang_es_mx=    locale: "es_MX"
set lang_fr_fr=    locale: "fr_FR"
set lang_hu_hu=    locale: "hu_HU"
set lang_it_it=    locale: "it_IT"
set lang_pl_pl=    locale: "pl_PL"
set lang_pt_br=    locale: "pt_BR"
set lang_ro_ro=    locale: "ro_RO"
set lang_ru_ru=    locale: "ru_RU"
set lang_th_th=    locale: "th_TH"
set lang_tr_tr=    locale: "tr_TR"
set lang_vi_vn=    locale: "vi_VN"
set lang_zh_my=    locale: "zh_MY"

:: 替换为简体中文
set replace_line=    locale: "zh_CN"

title 英雄联盟自动汉化工具 - 每5秒检测
cls
echo ========================================
echo     英雄联盟自动汉化保护工具
echo ========================================
echo 模式: 持续监控和锁定
echo 间隔: 每5秒检测一次
echo 目标: 自动汉化并设为只读
echo 支持: 28种语言自动转为简体中文
echo 日志: %log_file%
echo ========================================
echo 按 Ctrl+C 停止程序
echo.

:: 初始化日志
echo ======================================== > "%log_file%"
echo 自动汉化工具启动: %date% %time% >> "%log_file%"
echo 监控文件: %filename% >> "%log_file%"
echo ======================================== >> "%log_file%"

:main_loop
:: 记录开始时间
set "loop_time=%time%"

:: 检查文件是否存在
if not exist "%filename%" (
    echo [%time%] 错误: 文件不存在，等待...
    echo [%time%] 文件不存在 >> "%log_file%"
    timeout /t 5 /nobreak >nul
    goto main_loop
)

:: 创建临时文件
set temp_file=%temp%\lol_temp_%random%.yaml
set modified=0

:: 处理文件内容
> "%temp_file%" (
    for /f "delims=" %%i in ('type "%filename%"') do (
        set line=%%i
        set original_line=%%i

        :: 检查并替换所有语言
        if "!line!"=="%lang_tw%" (
            echo %replace_line%
            set modified=1
            echo [%loop_time%] 替换: zh_TW -> zh_CN >> "%log_file%"
        ) else if "!line!"=="%lang_us%" (
            echo %replace_line%
            set modified=1
            echo [%loop_time%] 替换: en_US -> zh_CN >> "%log_file%"
        ) else if "!line!"=="%lang_jp%" (
            echo %replace_line%
            set modified=1
            echo [%loop_time%] 替换: ja_JP -> zh_CN >> "%log_file%"
        ) else if "!line!"=="%lang_kr%" (
            echo %replace_line%
            set modified=1
            echo [%loop_time%] 替换: ko_KR -> zh_CN >> "%log_file%"
        ) else if "!line!"=="%lang_ar_ae%" (
            echo %replace_line%
            set modified=1
            echo [%loop_time%] 替换: ar_AE -> zh_CN >> "%log_file%"
        ) else if "!line!"=="%lang_id_id%" (
            echo %replace_line%
            set modified=1
            echo [%loop_time%] 替换: id_ID -> zh_CN >> "%log_file%"
        ) else if "!line!"=="%lang_cs_cz%" (
            echo %replace_line%
            set modified=1
            echo [%loop_time%] 替换: cs_CZ -> zh_CN >> "%log_file%"
        ) else if "!line!"=="%lang_de_de%" (
            echo %replace_line%
            set modified=1
            echo [%loop_time%] 替换: de_DE -> zh_CN >> "%log_file%"
        ) else if "!line!"=="%lang_el_gr%" (
            echo %replace_line%
            set modified=1
            echo [%loop_time%] 替换: el_GR -> zh_CN >> "%log_file%"
        ) else if "!line!"=="%lang_en_au%" (
            echo %replace_line%
            set modified=1
            echo [%loop_time%] 替换: en_AU -> zh_CN >> "%log_file%"
        ) else if "!line!"=="%lang_en_gb%" (
            echo %replace_line%
            set modified=1
            echo [%loop_time%] 替换: en_GB -> zh_CN >> "%log_file%"
        ) else if "!line!"=="%lang_en_ph%" (
            echo %replace_line%
            set modified=1
            echo [%loop_time%] 替换: en_PH -> zh_CN >> "%log_file%"
        ) else if "!line!"=="%lang_en_sg%" (
            echo %replace_line%
            set modified=1
            echo [%loop_time%] 替换: en_SG -> zh_CN >> "%log_file%"
        ) else if "!line!"=="%lang_es_ar%" (
            echo %replace_line%
            set modified=1
            echo [%loop_time%] 替换: es_AR -> zh_CN >> "%log_file%"
        ) else if "!line!"=="%lang_es_es%" (
            echo %replace_line%
            set modified=1
            echo [%loop_time%] 替换: es_ES -> zh_CN >> "%log_file%"
        ) else if "!line!"=="%lang_es_mx%" (
            echo %replace_line%
            set modified=1
            echo [%loop_time%] 替换: es_MX -> zh_CN >> "%log_file%"
        ) else if "!line!"=="%lang_fr_fr%" (
            echo %replace_line%
            set modified=1
            echo [%loop_time%] 替换: fr_FR -> zh_CN >> "%log_file%"
        ) else if "!line!"=="%lang_hu_hu%" (
            echo %replace_line%
            set modified=1
            echo [%loop_time%] 替换: hu_HU -> zh_CN >> "%log_file%"
        ) else if "!line!"=="%lang_it_it%" (
            echo %replace_line%
            set modified=1
            echo [%loop_time%] 替换: it_IT -> zh_CN >> "%log_file%"
        ) else if "!line!"=="%lang_pl_pl%" (
            echo %replace_line%
            set modified=1
            echo [%loop_time%] 替换: pl_PL -> zh_CN >> "%log_file%"
        ) else if "!line!"=="%lang_pt_br%" (
            echo %replace_line%
            set modified=1
            echo [%loop_time%] 替换: pt_BR -> zh_CN >> "%log_file%"
        ) else if "!line!"=="%lang_ro_ro%" (
            echo %replace_line%
            set modified=1
            echo [%loop_time%] 替换: ro_RO -> zh_CN >> "%log_file%"
        ) else if "!line!"=="%lang_ru_ru%" (
            echo %replace_line%
            set modified=1
            echo [%loop_time%] 替换: ru_RU -> zh_CN >> "%log_file%"
        ) else if "!line!"=="%lang_th_th%" (
            echo %replace_line%
            set modified=1
            echo [%loop_time%] 替换: th_TH -> zh_CN >> "%log_file%"
        ) else if "!line!"=="%lang_tr_tr%" (
            echo %replace_line%
            set modified=1
            echo [%loop_time%] 替换: tr_TR -> zh_CN >> "%log_file%"
        ) else if "!line!"=="%lang_vi_vn%" (
            echo %replace_line%
            set modified=1
            echo [%loop_time%] 替换: vi_VN -> zh_CN >> "%log_file%"
        ) else if "!line!"=="%lang_zh_my%" (
            echo %replace_line%
            set modified=1
            echo [%loop_time%] 替换: zh_MY -> zh_CN >> "%log_file%"
        ) else (
            echo !line!
        )
    )
)

:: 检查是否需要替换文件
if %modified% equ 1 (
    :: 移除只读属性
    attrib -R "%filename%" >nul 2>&1

    :: 替换原文件
    copy /y "%temp_file%" "%filename%" >nul

    :: 设置只读属性
    attrib +R "%filename%" >nul 2>&1

    echo [%time%] 已汉化文件并设为只读
    echo [%loop_time%] 成功: 文件已汉化并锁定 >> "%log_file%"

    :: 清理临时文件
    del "%temp_file%" >nul 2>&1
) else (
    :: 检查文件是否已经是只读
    attrib "%filename%" | findstr /i "R" >nul
    if errorlevel 1 (
        :: 如果不是只读，设为只读
        attrib +R "%filename%" >nul 2>&1
        echo [%time%] 文件已设为只读
        echo [%loop_time%] 设置: 文件设为只读 >> "%log_file%"
    ) else (
        echo [%time%] 状态正常(已是zh_CN且只读)
    )

    :: 清理临时文件
    del "%temp_file%" >nul 2>&1
)

:: 在屏幕上显示状态
if %modified% equ 1 (
    echo [%time%] 状态: 已执行汉化操作
) else (
    echo [%time%] 状态: 无需修改
)

echo [%time%] 下次检查: 5秒后
echo.

:: 等待5秒
timeout /t 5 /nobreak >nul

:: 回到主循环
goto main_loop

:end
echo.
echo 程序已停止
echo 查看完整日志: %log_file%
pause