@echo off
setlocal enabledelayedexpansion

mkdir "P序列标准编码" 2>nul

for %%f in (%*) do (
    set "input=%%~f"
    set "output=P序列标准编码\%%~nf_eP.txt"
    echo 正在处理: "!input!"
    py P序列编码.py "!input!" "!output!" || echo 处理失败: "!input!"
)
pause