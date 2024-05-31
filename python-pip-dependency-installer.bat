@echo off

REM Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python not found. Installing Python...

    REM Download Python installer
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe -OutFile python-installer.exe"

    REM Install Python
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1

    REM Clean up installer
    del python-installer.exe

    echo Python installed successfully.
) ELSE (
    echo Python is already installed.
)

REM Check if pip is available
pip --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Pip not found. Installing Pip...

    REM Download get-pip.py
    powershell -Command "Invoke-WebRequest -Uri https://bootstrap.pypa.io/get-pip.py -OutFile get-pip.py"

    REM Install Pip
    python get-pip.py

    REM Clean up get-pip.py
    del get-pip.py

    echo Pip installed successfully.
) ELSE (
    echo Pip is already installed.
)

REM Create virtual environment
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate

REM Create requirements.txt
echo selenium > requirements.txt
echo requests >> requirements.txt

REM Install dependencies
pip install -r requirements.txt

echo Virtual environment created and dependencies installed.
echo To activate the virtual environment, run:
echo     call venv\Scripts\activate
