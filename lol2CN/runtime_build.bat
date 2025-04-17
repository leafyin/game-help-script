@echo off

jlink --module-path F:\jdks\openjdk21\jmods --add-modules java.base,java.desktop --output myruntime -v

pause