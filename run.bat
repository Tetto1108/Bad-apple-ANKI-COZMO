@echo off
echo ===============================
echo  Cozmo Animation Player - RUN
echo ===============================
echo.

REM --- BUSCAR VERSIONES COMPATIBLES ---
set PYTHON_EXE=

echo Buscando Python compatible (3.10, 3.11, 3.12)...

for %%V in (3.10 3.11 3.12) do (
    for %%P in (
        "C:\Program Files\Python%%V\python.exe"
        "C:\Program Files\Python%%V\Scripts\python.exe"
        "C:\Program Files\Python%%V\pythonw.exe"
        "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python%%V\python.exe"
        "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python%%V\pythonw.exe"
    ) do (
        if exist %%P (
            set PYTHON_EXE=%%P
            goto FOUND_PYTHON
        )
    )
)

:FOUND_PYTHON

if "%PYTHON_EXE%"=="" (
    echo.
    echo ERROR: No se encontro Python 3.10, 3.11 o 3.12.
    echo PyCozmo NO es compatible con Python 3.13 o 3.14.
    echo.
    echo Descarga Python 3.11 desde:
    echo https://www.python.org/downloads/windows/
    echo.
    pause
    exit /b
)

echo Python encontrado: %PYTHON_EXE%
echo.

echo Ejecutando animacion...
"%PYTHON_EXE%" main.py

echo.
pause
