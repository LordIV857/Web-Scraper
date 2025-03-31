#!/bin/bash

# Mettre à jour le système et installer les dépendances nécessaires pour Playwright
apt-get update && apt-get install -y \
    libsoup-3.0-0 \
    libgstreamer-gl1.0-0 \
    libgstreamer-plugins-bad1.0-0 \
    libenchant-2-2 \
    libsecret-1-0 \
    libmanette-0.2-0 \
    libgles2

# Vérifier si pip est installé, sinon l'installer
if ! command -v pip &> /dev/null
then
    echo "pip n'est pas installé. Installation en cours..."
    apt-get install -y python3-pip
fi

# Installer Playwright et ses navigateurs
pip install --upgrade pip
pip install playwright
python -m playwright install

# Lancer le script Python en arrière-plan et enregistrer les logs
python app.py > app.log 2>&1 &
echo "Lancement de app.py en arrière-plan. Voir app.log pour les détails."
