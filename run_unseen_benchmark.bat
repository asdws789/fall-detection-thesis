@echo off
title Szakdolgozat: Erintetlen Uj Adathalmaz Kiertekelo
cd /d "%~dp0"

echo ========================================================================
echo   Szakdolgozati Rendszer - Erintetlen Uj Adathalmaz Kiertekelo
echo ========================================================================
echo.
echo Celmappa: data\raw\unseen_benchmark\
echo.
echo [1/2] Inditas: C:\Python313\python.exe src\test_unseen_benchmark.py ...
echo.

C:\Python313\python.exe src\test_unseen_benchmark.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [HIBA] A program futasa leallt. Hibakod: %ERRORLEVEL%
    pause
)
