@echo off
echo ========================================
echo Cabbage Detector - Environment Check
echo ========================================
echo.

REM Check NVIDIA driver
where nvidia-smi >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ NVIDIA driver NOT found
    goto end
) else (
    echo ✔ NVIDIA driver found
)

REM Check CUDA
where nvcc >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ CUDA Toolkit NOT found
    goto end
) else (
    echo ✔ CUDA Toolkit found
)

REM Check Python environment
if not exist "venv\Scripts\python.exe" (
    echo ❌ Python environment missing
    echo venv folder not found
    goto end
) else (
    echo ✔ Python environment found
)

REM Check TensorRT via Python (CORRECT WAY)
venv\Scripts\python.exe -c "import tensorrt as trt; print('✔ TensorRT:', trt.__version__)"
if %errorlevel% neq 0 (
    echo ❌ TensorRT NOT available
    goto end
)

REM Check Torch + CUDA
venv\Scripts\python.exe -c "import torch; print('✔ Torch:', torch.__version__); print('✔ CUDA available:', torch.cuda.is_available())"
if %errorlevel% neq 0 (
    echo ❌ Torch/CUDA error
    goto end
)

echo.
echo ========================================
echo Environment OK
echo You may proceed to engine setup
echo ========================================

:end
echo.
pause
