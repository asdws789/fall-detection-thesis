@echo off
chcp 65001 > nul
title Szakdolgozati Webkamera Teszt (YOLOv8-Pose)
echo =======================================================
echo   Szakdolgozat: YOLOv8-Pose Webkamera Teszt Inditasa
echo   Hardver: AMD Ryzen 5 CPU
echo =======================================================
echo.
python src\webcam_test.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [FIGYELEM] A futtatas hibaval leallt.
    echo Gyozodj meg rola, hogy a kovetkezo parancs lefutott:
    echo pip install ultralytics opencv-python
    echo.
    pause
)
