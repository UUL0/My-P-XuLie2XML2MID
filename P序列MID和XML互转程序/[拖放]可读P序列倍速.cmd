@echo off
setlocal enabledelayedexpansion

mkdir "可读P序列倍速" 2>nul

for %%f in (%*) do (
    set "input=%%~f"
    set "output=可读P序列倍速\%%~nf_P倍乘.txt"
    echo 正在处理: "!input!"
    py 可读P序列倍速.py "!input!" -c 3 -s " " -m 0.5 -o "!output!" || echo 处理失败: "!input!"
)
pause