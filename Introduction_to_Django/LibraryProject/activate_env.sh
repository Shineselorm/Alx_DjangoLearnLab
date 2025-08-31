#!/bin/bash
# Activation script for the LibraryProject virtual environment
# Run this script to activate the virtual environment: source activate_env.sh

echo "Activating virtual environment for LibraryProject..."
source venv/bin/activate
echo "Virtual environment activated!"
echo "Django version: $(python -c 'import django; print(django.get_version())')"
echo "To run Django commands, use: python manage.py <command>"