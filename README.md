# RLTetris


## Build (Windows, Visual Studio 2022)

    git submodule update --init
    python -m venv .venv
    .venv\Scripts\python.exe -m pip install -r requirements.txt
    cmd /c scripts\build.cmd
    .venv\Scripts\python.exe -m pytest
