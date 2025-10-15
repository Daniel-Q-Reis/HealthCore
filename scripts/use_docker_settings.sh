#!/bin/bash

# Switch to Docker settings
echo "Switching to Docker settings..."

# Check if backup file exists
if [ -f "healthcore/settings/development.py.docker.bak" ]; then
    # Restore the Docker settings from backup
    cp healthcore/settings/development.py.docker.bak healthcore/settings/development.py
    rm healthcore/settings/development.py.docker.bak
    echo "Successfully switched to Docker settings."
else
    # Update the development.py file to use 'db' instead of localhost for PostgreSQL
    sed -i "s/'HOST': 'localhost'/'HOST': 'db'/g" healthcore/settings/development.py
    echo "Successfully switched to Docker settings."
fi