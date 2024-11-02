@echo off

:: Get current working dir and set it as PYTHONPATH
SET PYTHONPATH="$(pwd)"

:: Check if Python is installed
python --version 2>NUL
IF ERRORLEVEL 1 (
    echo "Python is not installed. Please install Python version 3.12 or higher."
    exit /b 1
)

:: Check Python version (requires at least Python 3.12)
FOR /F "tokens=2 delims= " %%v IN ('python --version') DO SET PY_VERSION=%%v
FOR /F "tokens=1,2 delims=." %%a IN ("%PY_VERSION%") DO (
    SET MAJOR=%%a
    SET MINOR=%%b
)

:: Check major and minor version
IF %MAJOR% LSS 3 (
    echo "Python version must be at least 3.12. Please upgrade."
    exit /b 1
)

IF %MAJOR% EQU 3 IF %MINOR% LSS 12 (
    echo "Python version must be at least 3.12. Please upgrade."
    exit /b 1
)

echo "Python version is 3.12 or higher. Proceeding with setup..."

:: Create a virtual environment if it doesn't exist
IF NOT EXIST ".venv" (
    echo "Creating virtual environment..."
    python -m venv .venv
)

:: Ensure pip is installed and up-to-date
echo "Ensuring pip is up-to-date..."
.\.venv\Scripts\python -m ensurepip --upgrade
.\.venv\Scripts\python -m pip install --upgrade pip

:: Install pip-tools into the virtual environment
echo "Installing pip-tools..."
.\.venv\Scripts\pip install pip-tools

:: Compile dependencies from requirements.in
echo "Compiling requirements.txt from requirements.in..."
.\.venv\Scripts\pip-compile requirements.in

:: Install all dependencies from requirements.txt
echo "Installing dependencies from requirements.txt..."
.\.venv\Scripts\pip install -r requirements.txt

:: Inform user to activate the virtual environment manually
echo "To activate the virtual environment, run: .\.venv\Scripts\activate"

:: Activate the virtual environment
call .venv\Scripts\activate

:: Inform user of successful activation
echo "Virtual environment activated."

:: Get current working dir and set it as PYTHONPATH
SET PYTHONPATH=%cd%

:: Print PYTHONPATH
echo PYTHONPATH defined as: %PYTHONPATH%

echo "Setup completed successfully."
