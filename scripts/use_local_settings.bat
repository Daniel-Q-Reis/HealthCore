@echo off

REM Switch to local development settings
echo Switching to local development settings...

REM Backup the current development.py file
copy "healthcore\\settings\\development.py" "healthcore\\settings\\development.py.docker.bak"

REM Update the development.py file to use localhost instead of 'db' for PostgreSQL
powershell -Command "(gc healthcore\\settings\\development.py) -replace \"'HOST': 'db'\", \"'HOST': 'localhost'\" | Out-File -encoding ASCII healthcore\\settings\\development.py"

echo Successfully switched to local development settings.
echo To switch back to Docker settings, run scripts\\use_docker_settings.bat