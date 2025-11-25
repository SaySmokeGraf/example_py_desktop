@echo off
echo Converting UI files to Python...

pyuic5 ui/mainGUI.ui -o ui/mainGUI.py
pyuic5 ui/previewGUI.ui -o ui/previewGUI.py

echo Conversion complete!
pause
