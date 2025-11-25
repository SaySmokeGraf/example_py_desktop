@echo off
echo Конвертация ui в py...

pyuic5 ui/mainGUI.ui -o ui/mainGUI.py
pyuic5 ui/previewGUI.ui -o ui/previewGUI.py

echo Конвертация завершена!
pause
