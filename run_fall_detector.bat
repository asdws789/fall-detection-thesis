@echo off
chcp 65001 > nul
title Szakdolgozat: Valos Ideju Esesdetektalo Baseline
echo =======================================================
echo   Szakdolgozat: Esesdetektalo Baseline Program
echo   Modell: YOLOv8-Pose + Kinematikai Allapotgep
echo   Hardver: AMD Ryzen 5 CPU
echo =======================================================
echo.
python src\simple_fall_detector.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [HIBA] A program futasa leallt.
    pause
)
