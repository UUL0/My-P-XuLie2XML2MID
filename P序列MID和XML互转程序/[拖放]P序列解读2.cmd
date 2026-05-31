@echo off
setlocal enabledelayedexpansion

mkdir "P序列标准解读2" 2>nul

for %%f in (%*) do (
    set "input=%%~f"
    set "output=P序列标准解读2\%%~nf_解读2.txt"
    echo 正在处理: "!input!"
    py P序列解读2.py "!input!" "!output!" || echo 处理失败: "!input!"
)
pause