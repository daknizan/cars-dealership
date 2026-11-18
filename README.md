# Cars Dealership — Capstone Full-Stack

Application web full-stack pour **Cars Dealership**, un concessionnaire national de voitures aux États-Unis.
Elle affiche les succursales (dealers) et permet aux utilisateurs de consulter et de soumettre des avis.

## Stack technique
- **Backend** : Django (Python) — API REST pour les concessionnaires, avis, authentification et analyse de sentiment
- **Frontend** : React — interface responsive (pages Dealers, Dealer detail, Login, Register, Post Review, About, Contact)
- **Base de données** : SQLite (dev) / Cloudant (optionnel)
- **DevOps** : Docker, GitHub Actions (CI/CD), IBM Cloud Code Engine (déploiement)

## Structure du projet
```
server/
  manage.py
  server/            # projet Django (settings, urls)
  djangoapp/         # application (models, vues, urls)
  frontend/          # application React + fichiers statiques
.github/workflows/   # CI/CD GitHub Actions
```

## Lancer en local
```bash
cd server
pip install -r requirements.txt
python manage.py makemigrations && python manage.py migrate
python manage.py createsuperuser   # user: root
python manage.py runserver
```

Frontend (dev) :
```bash
cd server/frontend
npm install
npm start
```

Build production :
```bash
npm run build
```

## Points d'API principaux
| Méthode | Endpoint | Description |
|---|---|---|
| POST | /djangoapp/login | Connexion utilisateur |
| GET  | /djangoapp/logout | Déconnexion |
| POST | /djangoapp/registration | Inscription |
| GET  | /djangoapp/get_dealers | Tous les concessionnaires |
| GET  | /djangoapp/get_dealers/<state> | Concessionnaires par état |
| GET  | /djangoapp/dealer/<id> | Détail d'un concessionnaire |
| GET  | /djangoapp/reviews/dealer/<id> | Avis d'un concessionnaire |
| POST | /djangoapp/add_review | Ajouter un avis |
| GET  | /djangoapp/sentiment/<text> | Analyse de sentiment |

## Déploiement
L'application est conteneurisée avec Docker et déployable via IBM Cloud Code Engine.
