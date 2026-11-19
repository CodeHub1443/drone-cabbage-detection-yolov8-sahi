@echo off
echo ================================
echo Cabbage Detector - Environment Test
echo ================================
echo.

call venv\Scripts\activate.bat

python -c "import torch; import ultralytics; print('TORCH:', torch.__version__); print('ULTRALYTICS:', ultralytics.__version__)"

echo.
echo Environment OK.
pause
