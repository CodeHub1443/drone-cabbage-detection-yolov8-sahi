@echo off
cd /d "%~dp0"

echo ========================================
echo Cabbage Detector - TensorRT Engine Setup
echo ========================================
echo.

REM Check venv python
if not exist "venv\Scripts\python.exe" (
    echo ERROR: venv not found.
    echo Make sure the full project folder was copied correctly.
    pause
    exit /b 1
)

echo Using local Python from venv...
echo.

REM Build engine using ultralytics inside venv
venv\Scripts\python.exe -m ultralytics export ^
  model=best.pt ^
  format=engine ^
  imgsz=640 ^
  dynamic=True ^
  batch=8 ^
  device=0

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Engine build failed.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Engine generation finished successfully.
echo ========================================
echo.

pause
