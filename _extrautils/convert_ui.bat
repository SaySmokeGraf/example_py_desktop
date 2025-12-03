@echo off
echo Converting ui to py...

pyuic5 ui/loadingGUI.ui -o ui/loadingGUI.py
pyuic5 ui/mainGUI.ui -o ui/mainGUI.py
pyuic5 ui/previewGUI.ui -o ui/previewGUI.py

echo Converting completed!
pause
