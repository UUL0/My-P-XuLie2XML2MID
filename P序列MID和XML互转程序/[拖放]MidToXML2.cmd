@echo off
setlocal enabledelayedexpansion

mkdir "Mid标准XML2" 2>nul

for %%f in (%*) do (
    set "input=%%~f"
    set "output=Mid标准XML2\%%~nf_XML.xml"
    echo 正在处理: "!input!"
    py MIDtoXML2.py "!input!" "!output!" || echo 处理失败: "!input!"
)
pause