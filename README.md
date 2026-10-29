# TaxiShare : simulation multi-agents avec Mesa

Simulation locale de taxis partagés, implémentée à partir du cahier des règles
U01 à U71 et des clarifications de cette conversation. Les agents `Passenger`
et `Taxi` sont des agents Mesa. Ils décident par messages adressés, avec une
horloge commune de 0,2 seconde et des actions physiques indépendantes.

## Lancer l'application

Depuis ce dossier dans PowerShell, l'environnement est déjà installé :

```powershell
.\.venv\Scripts\python.exe app.py
```

Sur un autre ordinateur, avec Python 3.12 recommandé :

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

L'interface permet de démarrer, mettre en pause, avancer de 0,2 s, rejouer,
charger un scénario, modifier les paramètres de génération et exporter.
Modifier un champ ne change pas le monde courant : cliquer sur
« Générer avec ces paramètres » applique ces valeurs à un nouveau scénario.
Une même graine et les mêmes paramètres reproduisent la même génération.
Le nombre de pas par rafraîchissement change la cadence de l'animation,
sans modifier la durée du pas ni les décisions.

Les clients attendant au même accès sont affichés en ligne, un point par personne :
rouge pour une recherche en cours, bleu pour une réservation confirmée. Un trait
relie la ligne à l'accès réel. Les taxis sont gris lorsqu'ils sont vides et libres,
orange lorsqu'ils sont vides avec une réservation, et verts lorsqu'ils ont des
passagers (même s'ils ont aussi des réservations futures). Les taxis sont des
triangles orientés dans leur sens de circulation, y compris pendant les arrêts.
Deux légendes distinctes, « Taxis » et « Clients », apparaissent sous la carte.
Les décalages graphiques ne déplacent pas les agents.

Le scénario courant de l'interface est sauvegardé avant exécution dans
`output/gui/scenario.json`. Un export de résultats comprend aussi sa propre
copie complète du scénario. Rejouer remet ce scénario à son état initial.

## Exécution sans interface

```powershell
.\.venv\Scripts\python.exe run_simulation.py --output output/default
.\.venv\Scripts\python.exe run_simulation.py --seed 17 --capacity 4 --output output/seed17
.\.venv\Scripts\python.exe run_simulation.py --scenario output/default/scenario.json --output output/replay
```

Tous les paramètres de `Config` sont disponibles en ligne de commande,
avec des tirets à la place des underscores. `--help` les liste.
`--config fichier.json` accepte un objet avec les champs de `Config`.
`--trace-messages` ajoute le journal détaillé des messages.
`--no-figure` désactive seulement la génération de l'image finale.

Une exécution normale renvoie le code 0. Un arrêt incomplet renvoie le code 2
et conserve les résultats partiels. Le chargement d'un scénario ne peut pas
être mélangé avec des options de génération : ses entrées sauvegardées font foi.

## Organisation et parcours de lecture

| Fichier | Responsabilité |
| --- | --- |
| `taxishare/config.py` | Paramètres, unités, constantes physiques et validations |
| `taxishare/scenario.py` | Quatre flux aléatoires, génération et JSON rejouable |
| `taxishare/city.py` | Routes, accès et graphe orienté sans demi-tour |
| `taxishare/contracts.py` | Données explicites : voyages, offres, arrêts, engagements, actions |
| `taxishare/messaging.py` | Boîtes de réception individuelles et transport des messages |
| `taxishare/passenger.py` | Appel initial, choix, confirmation et notifications de transport |
| `taxishare/taxi.py` | Réception, offres, revalidation, engagements et actions physiques |
| `taxishare/planning.py` | Insertion des arrêts et contrôles des contraintes |
| `taxishare/traffic.py` | Charges et vitesses par portion dirigée |
| `taxishare/model.py` | Les neuf phases de l'horloge et les assertions globales |
| `taxishare/metrics.py` | Mesures individuelles, statistiques et exports |
| `taxishare/visualization.py` | Affichage en lecture seule |
| `app.py` | Commandes de l'interface locale Tkinter |
| `run_simulation.py` | Exécution d'un scénario sans interface |

Pour comprendre les comportements, lire d'abord `passenger.py` et `taxi.py`,
puis `model.py` pour leur ordre d'activation et `planning.py` pour les contraintes.
Le modèle coordonne les phases ; il ne choisit pas un taxi à la place d'un client.
Les identifiants, commentaires et docstrings sont en anglais conformément au cahier.

## Règles essentielles implémentées

- Ville finie à axes complets et cadre extérieur ; accès fixes hors carrefours.
- Position et orientation conservées ; aucun demi-tour, même à l'arrêt.
- Une demande par personne, persistante, avec un CFP initial copié dans chaque
  boîte de taxi. Les agents ne lisent pas les données privées des autres.
- Offres valables une ronde ; choix par début de montée estimé, puis score
  maximal de budget, puis identifiant du taxi.
- Confirmation après revalidation, priorité à l'ancienneté puis à l'identifiant.
- Insertion préservant les anciens arrêts, les budgets cumulatifs et toutes
  les distances d'approche promises. Une offre seule ne réserve aucune place.
- Capacité de 1 à 4, place occupée dès le début de montée et libérée à la fin
  de descente. Les engagements futurs peuvent être plus nombreux que les places.
- Portion de 100 m en 7,2 s à vitesse libre ; chaque opération dure 2 s.
- Congestion par sens, recalculée pour tous à partir du même instantané.
- Fin normale après la dernière descente ; état figé et plafond technique
  produisent des résultats incomplets, jamais des livraisons fictives.

## Tests

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
```

Les assertions métier sont actives par défaut. Ne pas lancer Python avec `-O`
si l'on souhaite les conserver. Les erreurs de configuration sont des exceptions
explicites et restent contrôlées même si les assertions Python sont désactivées.
`requirements-lock.txt` consigne les versions réellement installées sur la machine
de validation ; `requirements.txt` fixe les deux dépendances principales.

## Fichiers exportés

| Fichier | Contenu |
| --- | --- |
| `scenario.json` | Configuration, axes, bâtiments, accès, flotte, orientations, voyages et dates |
| `summary.json` | Statut, cause d'arrêt, mesures globales, effectifs et clients non livrés |
| `passengers.csv` | Une ligne par client prévu, y compris futur ou non livré |
| `taxis.csv` | Une ligne par taxi, distances par occupation et décomposition des temps |
| `timeline.csv` | Observation globale à chaque frontière de pas traitée |
| `provenance.json` | Versions de l'environnement et empreintes du code et des PDF sources |
| `dashboard.png` | Carte et graphiques de l'exécution |
| `messages.csv` | Journal optionnel des messages, activé avec `--trace-messages` |

Les durées et dates sont en secondes, les distances en mètres. Les valeurs
inconnues sont `null` en JSON et vides en CSV. Les moyennes de voyages terminés
portent uniquement sur les clients livrés, avec leur effectif affiché.
Les compteurs de messages comptent les livraisons dans les boîtes : 60 CFP
diffusés à 8 taxis donnent 480 messages CFP, sans répétition des appels.

Les exports écrivent dans le dossier choisi. Utiliser des dossiers distincts
pour conserver plusieurs exécutions.

## Documentation de conformité

- [Décisions techniques](docs/technical-decisions.md)
- [Correspondance entre cahier, code et tests](docs/rules-coverage.md)
- [Vérifications effectuées et résultats](docs/validation.md)

La comparaison individuel/partagé, le multi-hop entre taxis et le modèle
d'émissions ne font pas partie de la cible courante. Les distances ne sont pas
des quantités de CO2. Le rapport d'analyse demandé par le professeur demeure
un livrable distinct ; les exports fournissent les données nécessaires à sa préparation.
