#!/bin/bash

# Installe les bibliothèques manquantes requises pour Playwright
apt-get update
apt-get install -y \
  libgtk-4.0-0 \
  libgraphene-1.0-0 \
  libgstgl-1.0-0 \
  libgstcodecparsers-1.0-0 \
  libavif15 \
  libenchant2-2 \
  libsecret-1-0 \
  libmanette-0.2-0 \
  libgles2-mesa

# Installer les dépendances Python
pip install -r requirements.txt

# Installer Playwright et ses dépendances
playwright install

# Lancer l'application Flask
python app.py
