@echo off
setlocal enabledelayedexpansion

mkdir "P序列标准mid" 2>nul

for %%f in (%*) do (
    set "input=%%~f"
    set "output=P序列标准mid\%%~nf_P.mid"
    echo 正在处理: "!input!"
    py PtoMid.py "!input!" "!output!" || echo 处理失败: "!input!"
)

pause