@echo off
setlocal enabledelayedexpansion
mkdir "标准P序列" 2>nul


for %%f in (%*) do (
    set "input=%%~f"
    set "output=标准P序列\%%~nf_P序列.txt"
    echo 正在处理: "!input!"
    py xmlToP.py "!input!" "!output!" || echo 处理失败: "!input!"
)
pause