@echo off

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
IF EXIST "requirements.in" (
    echo "Compiling requirements.txt from requirements.in..."
    .\.venv\Scripts\pip-compile requirements.in > NUL 2>&1
) ELSE (
    echo "requirements.in file not found. Skipping compilation."
)

:: Install all dependencies from requirements.txt
IF EXIST "requirements.txt" (
    echo "Installing dependencies from requirements.txt..."
    .\.venv\Scripts\pip install -r requirements.txt
) ELSE (
    echo "requirements.txt file not found. Skipping dependency installation."
)

echo "Setup completed successfully."

:: Check if tox is installed in the virtual environment
.\.venv\Scripts\tox --version 2>NUL
IF ERRORLEVEL 1 (
    echo "Tox is not installed in the virtual environment. Installing tox..."
    .\.venv\Scripts\pip install tox
) ELSE (
    echo "Tox is already installed in the virtual environment."
)

:: Run tox with the correct path to tox.ini
echo "Running tox with custom tox.ini path..."
.\.venv\Scripts\tox -c tox.ini

:: Inform the user to activate the virtual environment manually if needed
echo "To activate the virtual environment manually, run: .\.venv\Scripts\activate"
