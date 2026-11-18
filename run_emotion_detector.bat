@echo off
chcp 65001 > nul
title Szakdolgozat Kiserlet: Valos Ideju Arckifejezes es Erzelemfelismero (100%% Ingyenes)
echo =======================================================
echo   Szakdolgozat: Arckifejezes es Erzelemfelismero Modul
echo   Modell: YOLOv8 fej-detekcio + FERPlus ONNX (Helyi CPU)
echo   Hardver: AMD Ryzen 5 CPU (100%% Helyi, 0 Ft koltseg)
echo =======================================================
echo.
python src\face_emotion_detector.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [HIBA] A program futasa leallt.
    pause
)
