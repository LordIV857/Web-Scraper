#!/bin/bash

# Installer Playwright et ses navigateurs
pip install playwright
python -m playwright install

# Lancer votre script Python
python app.py