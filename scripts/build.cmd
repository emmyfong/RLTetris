@echo off
setlocal

rem Visual Studio 2022 Community: compiler environment, CMake and Ninja.
set "VS=C:\Program Files\Microsoft Visual Studio\2022\Community"
call "%VS%\VC\Auxiliary\Build\vcvars64.bat" >nul || exit /b 1
set "PATH=%VS%\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin;%VS%\Common7\IDE\CommonExtensions\Microsoft\CMake\Ninja;%PATH%"

cd /d "%~dp0.."
set "PY=%CD%\venv\Scripts\python.exe"
for /f "delims=" %%i in ('"%PY%" -m pybind11 --cmakedir') do set "PYBIND11_DIR=%%i"

cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release ^
    -DPython_EXECUTABLE="%PY%" -Dpybind11_DIR="%PYBIND11_DIR%" || exit /b 1
cmake --build build || exit /b 1
