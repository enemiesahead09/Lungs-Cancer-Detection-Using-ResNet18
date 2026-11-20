@echo off
title PulmoScan AI - Lung Disease Detection System
echo ==============================================================
echo           PulmoScan AI - Lung Cancer Detection System
echo            Multi-Class CT Classification with Grad-CAM
echo ==============================================================
echo.
echo Launching web application in your default browser...
echo.

cd /d "%~dp0"
call "C:\Users\shaur\anaconda3\Scripts\activate.bat" spam-detection
streamlit run app.py

pause
