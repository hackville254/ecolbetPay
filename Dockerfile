# Utilisation d'une image de base Alpine Linux optimisée pour Python
FROM python:3.10-alpine

# Définir des variables d'environnement pour éviter les avertissements Python lors de l'exécution en mode non interactif
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Créer et définir le répertoire de travail dans le conteneur
WORKDIR /ecolebetPay

# Copier le fichier requirements.txt dans le conteneur
COPY ./requirement.txt /ecolebetPay/

# Installer les dépendances Python
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirement.txt \ 
 && pip install -i https://test.pypi.org/simple/ cinetpay-sdk==0.1.1

# Copier le code de l'application Django dans le conteneur
COPY . /ecolebetPay/


# Exposer le port sur lequel l'application Django écoute
EXPOSE 8923

# Commande pour démarrer l'application Django
CMD ["gunicorn", "--bind", "0.0.0.0:8923", "ecolbetPay.wsgi:application"]
