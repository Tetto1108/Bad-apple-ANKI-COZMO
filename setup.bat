@echo off
echo ===============================
echo Instalando dependencias para Cozmo...
echo ===============================
python --version
echo.

pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Instalación completa.
pause
