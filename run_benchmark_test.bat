@echo off
title Benchmark Video Kiertekelo
echo ===================================================================
echo   Szakdolgozat: Benchmark Kiertekelo Alkalmazas
echo   Inditas folyamatban...
echo ===================================================================
echo.
cd /d "C:\uni_stuff\anti_thesis"
C:\Python313\python.exe "src\test_benchmark_video.py"
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [HIBA] A program leallt (Hibakod: %ERRORLEVEL%).
    pause
)
