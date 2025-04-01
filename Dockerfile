# Utilisation d'une image de base officielle de Python
FROM python:3.11-slim

# Mise à jour des paquets et installation des dépendances système requises pour Playwright
RUN apt-get update && apt-get install -y \
    libgtk-4.0-0 \
    libgraphene-1.0-0 \
    libgstgl-1.0-0 \
    libgstcodecparsers-1.0-0 \
    libavif15 \
    libenchant2-2 \
    libsecret-1-0 \
    libmanette-0.2-0 \
    libgles2-mesa \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier de configuration et les fichiers de l'application
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install -r requirements.txt

# Installer Playwright et ses dépendances
RUN playwright install

# Copier l'application Flask
COPY . .

# Exposer le port 5000
EXPOSE 5000

# Lancer l'application Flask
CMD ["python", "app.py"]