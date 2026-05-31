@echo off
setlocal enabledelayedexpansion
mkdir "Mid标准XML2筛选" 2>nul

for %%f in (%*) do (
    set "input=%%~f"
    set "output=Mid标准XML2筛选\%%~nf_XML筛.xml"
    echo 正在处理: "!input!"
    py MIDtoXML2筛选音符.py "!input!" "!output!" || echo 处理失败: "!input!"
)

pause