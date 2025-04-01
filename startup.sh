#!/bin/bash

# Installer Playwright et ses dépendances manuellement
pip install --no-cache-dir -r requirements.txt
playwright install chromium

# Installer les dépendances manquantes pour Playwright
apt-get update && apt-get install -y \
    libgtk-4-1 \
    libgraphene-1.0-0 \
    libgstgl-1.0-0 \
    libgstcodecparsers-1.0-0 \
    libavif15 \
    libenchant-2-2 \
    libsecret-1-0 \
    libmanette-0.2-0 \
    libgles2-mesa