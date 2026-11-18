@echo off
title Szakdolgozat: ST-GCN Graf Esesdetektalo Rendszer
echo =======================================================
echo   Szakdolgozat: ST-GCN Graf Esesdetektalo Rendszer
echo   Modell: YOLOv8-Pose + Ter-Idobeli Grafkonvolucio ONNX
echo   Hardver: AMD Ryzen 5 CPU (100%% Helyi Inferencia)
echo =======================================================
echo.
cd /d "C:\uni_stuff\anti_thesis"
C:\Python313\python.exe "src\stgcn_fall_detector.py"
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [HIBA] A program futasa leallt.
    pause
)
