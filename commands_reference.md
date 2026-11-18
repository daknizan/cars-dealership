# Référence des commandes pour le devoir

> Exécutez ces commandes contre votre serveur local (`python manage.py runserver`, port 8000)
> et enregistrez chaque sortie dans le fichier demandé par la tâche.

## Préparation (une seule fois)
```bash
cd server
python manage.py migrate
python manage.py createsuperuser      # créez le compte root (Tâches 12-13)
```

## Tâche 2 — fichier django_server
La sortie affichée au démarrage :
```
System check identified no issues (0 silenced).
Django version 4.2.x, using settings 'server.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

## Tâche 5 — fichier loginuser
```bash
curl -X POST -H "Content-Type: application/json"   -d '{"userName":"testuser","password":"testpass123"}'   http://localhost:8000/djangoapp/login
# Sortie attendue : {"userName": "testuser", "status": "Authenticated"}
```
(Créez d'abord l'utilisateur : `python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_user('testuser', password='testpass123')"`)
IMPORTANT : la session utilise les cookies Django. Pour les tâches 6 et 22, sauvegardez les cookies :
`curl -c cookies.txt ...` puis réutilisez `-b cookies.txt`.

## Tâche 6 — fichier logoutuser
```bash
curl -b cookies.txt http://localhost:8000/djangoapp/logout
# Sortie attendue : {"userName": ""}
```

## Tâche 8 — fichier getdealerreviews
```bash
curl http://localhost:8000/djangoapp/reviews/dealer/1
```

## Tâche 9 — fichier getalldealers
```bash
curl http://localhost:8000/djangoapp/get_dealers
```

## Tâche 10 — fichier getdealerbyid
```bash
curl http://localhost:8000/djangoapp/dealer/1
```

## Tâche 11 — fichier getdealersbyState
```bash
curl http://localhost:8000/djangoapp/get_dealers/Kansas
```

## Tâches 14-15 — fichier getallcarmakes
```bash
curl http://localhost:8000/djangoapp/get_cars
```

## Tâche 16 — fichier analyzereview
```bash
curl "http://localhost:8000/djangoapp/sentiment/Services fantastiques"
# Sortie attendue : {"text": "Services fantastiques", "sentiment": "positive"}
```

## Tâche 22 — ajout d'un avis connecté
```bash
curl -b cookies.txt -X POST -H "Content-Type: application/json"   -d '{"dealership":1,"review":"Services fantastiques","car_make":"Toyota","car_model":"Camry","car_year":2025,"purchase":true,"purchase_date":"2026-11-18"}'   http://localhost:8000/djangoapp/add_review
```

## Captures d'écran (Tâches 12-13, 17-22, 25-28)
Ouvrez dans le navigateur :
- http://localhost:8000/admin/ → login root (Tâche 12), logout (Tâche 13)
- http://localhost:3000/ → dealers avant/après login (Tâches 17-18)
- http://localhost:3000/ + filtre "Kansas" (Tâche 19)
- http://localhost:3000/dealer/1 (Tâche 20)
- http://localhost:3000/postreview/1 (Tâche 21), puis la page dealer avec le nouvel avis (Tâche 22)
