# Utiliser une image officielle avec Playwright préinstallé
FROM mcr.microsoft.com/playwright/python:v1.51.0-jammy

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY . /app

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port Flask
EXPOSE 5000

# Lancer l’application
CMD ["python", "app.py"]
