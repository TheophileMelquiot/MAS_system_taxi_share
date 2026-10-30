# Vérifications effectuées

## Demi-tours autorisés et routage simplifié, 30 octobre 2026

Commande exécutée dans l'environnement du dépôt :

```powershell
.\.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider
```

Résultat : **57 tests réussis en 14,83 s**. Le contrôle couvre les chemins
entre cellules, l'arrêt sur place, les demi-tours après montée ou stationnement,
la fin obligatoire d'une portion engagée, son reste d'approche et son coût pour
les passagers déjà à bord. Les quatre bornes de revalidation sont exercées
séparément. Capacité, budgets cumulés, protection des approches, opérations,
messages, rendu, rejeu et exports restent testés.

La congestion demeure séparée pour les deux sens : le test d'instantané vérifie
un ralentissement pour trois taxis dans un sens et la vitesse libre pour le taxi
en sens opposé. Un test complet vérifie aussi une congestion non nulle et
l'indépendance de l'ordre d'activation. Aucun changement de `traffic.py`.

Le diagnostic d'état figé reste défensif. Son test force l'absence d'offre pour
vérifier l'arrêt incomplet ; l'ancien cas de taxi mal orienté est désormais
couvert par une livraison réussie avec demi-tour.

Comparaison réexécutée :

```powershell
.\.venv\Scripts\python.exe -B run_experiments.py --output output/comparison-uturns
```

Cinq graines fixées de 2026 à 2030, capacités 1 et 3, huit taxis et 60 demandes
entre 0 et 300 s. **Les dix simulations sont complètes : 60/60 clients livrés
chacune, cinq paires utilisables.** Les JSON exportés ont été comparés : seule
la capacité diffère dans chaque paire. Les scénarios des cinq graines sont
également identiques aux précédents exports sans demi-tour.

| Mesure | Moyenne individuel | Moyenne partagé | Moyenne des écarts | Écart-type des écarts |
| --- | ---: | ---: | ---: | ---: |
| Distance totale (m) | 129 760 | 90 500 | -39 260 | 11 225,33 |
| Attente moyenne (s) | 427,47 | 250,20 | -177,27 | 47,95 |
| Temps total moyen (s) | 532,05 | 360,57 | -171,49 | 46,93 |
| Fraction de distance partagée | 0 | 0,24005 | +0,24005 | 0,05726 |

Les écarts sont partagé moins individuel. Ces résultats caractérisent ces
entrées et cette politique, sans garantie pour une ville réelle. Les anciens
exports `output/comparison/` sont préservés et correspondent à l'interdiction
des demi-tours. Les tableaux plus anciens ci-dessous restent historiques.

Avant migration, 930 couples ordonnés d'accès distincts de la carte par défaut
ont été comparés : D0 orientée avec meilleure direction initiale et distance
entre cellules étaient identiques. La nouvelle définition conserve ces valeurs.

`city.py` et `planning.py` passent ensemble de 325 à 250 lignes physiques.
`State`, `successors`, `paths_to`, `Label`, `_visit` et `_prune` sont retirés ou
remplacés. Les comptes par passager et la recherche des insertions restent
présents. Aucune mesure comparative de performance n'a été faite : les durées
de tests ne permettent pas d'annoncer un facteur d'accélération.

Le commit local `d488533` conserve l'état avant migration. Son push vers
`origin/yanis` est bloqué par GitHub : erreur 403, droits d'écriture absents
pour le compte `Yanicse`. Aucun succès de publication n'est annoncé.

L'interface Tk n'a pas fait l'objet d'un nouveau contrôle visuel ; le rendu et
ses exports ont été exercés par la suite automatique.


## Simplification et comparaison minimale, 30 octobre 2026

Suite complète dans l'environnement du dépôt : **51 tests réussis en 16,43 s**.
Les sept nouveaux cas vérifient la génération unique et les entrées communes,
l'exclusion des paires incomplètes, les différences appariées et leur écart-type,
les statistiques absentes sans demande et le refus de listes de graines invalides.

Le script a été exécuté avec ses paramètres par défaut : cinq graines de 2026 à
2030, capacités un et trois, huit taxis et 60 demandes entre 0 et 300 s.
**Les dix simulations sont complètes, avec 60 clients livrés chacune.** Les
fichiers exportés confirment que seule la capacité diffère entre les deux entrées
de chaque paire. Les exports se trouvent dans `output/comparison/`.

| Mesure | Moyenne individuel | Moyenne partagé | Moyenne des écarts | Écart-type des écarts |
| --- | ---: | ---: | ---: | ---: |
| Distance totale (m) | 168 100 | 109 220 | -58 880 | 21 446,61 |
| Attente moyenne (s) | 618,50 | 358,17 | -260,32 | 92,17 |
| Temps total moyen (s) | 725,44 | 468,14 | -257,31 | 91,31 |
| Fraction de distance partagée | 0 | 0,19375 | +0,19375 | 0,04306 |

Les écarts sont partagé moins individuel, avec cinq paires utilisables par mesure.
Ces résultats sont des vérifications d'exécution sur ces entrées, sans prétention
de validité pour une ville réelle. Les règles de circulation n'ont pas changé.

Un contrôle de l'interface Tk a vérifié les cinq champs, la conservation de
paramètres masqués modifiés (largeur, détour et plafond), le pas manuel et le
rejeu en mémoire. La fenêtre a ensuite été inspectée visuellement sur Windows.
Sa taille initiale tient désormais compte de l'écran et de sa mise à l'échelle ;
la marge des légendes a été agrandie pour que les deux légendes restent visibles.
Leurs bornes ont aussi été vérifiées dans le canevas.

Les anciens fichiers `app.py`, `run_experiments.py`, `requirements.txt` et README
du dossier parent ont été déplacés dans `archives/ancienne_version/`. Leurs
empreintes SHA-256 avant et après déplacement sont identiques. Un nouveau README
du parent désigne le dépôt actif et son environnement. Les PDF, les notes et les
environnements virtuels sont restés à leur emplacement.

## Vérification de la branche yanis, 30 octobre 2026

Environnement isolé `.venv` : Windows, Python 3.12.2, Mesa 3.3.1,
Matplotlib 3.10.8 et pytest 8.4.2, installés à partir de `requirements-dev.txt`.

Commande exécutée : `.\.venv\Scripts\python.exe -m pytest -q`.
Résultat après retrait du chargement : **44 tests réussis en 9,87 s**,
dont l'exécution complète du scénario par défaut avec les assertions actives.
Les 12 cas propres au chargement JSON sont retirés avec la fonctionnalité.
Le test de sauvegarde vérifie maintenant la conservation de toutes les entrées
exportées et la génération identique avec les mêmes paramètres.

Le bouton « Load scenario », l'option `--scenario` et `Scenario.load` sont
supprimés à la demande de l'utilisateur. L'export et le rejeu du scénario courant
en mémoire sont conservés, ainsi que les commentaires explicatifs et la politique
de revalidation des offres. L'interface graphique n'a pas fait l'objet d'un
nouveau contrôle visuel pendant cette vérification.

Les résultats détaillés ci-dessous conservent leur date de validation initiale.

Date : 29 octobre 2026. Environnement testé : Windows, Python 3.12, Mesa 3.3.1,
Matplotlib 3.10.8. Les dépendances installées sont consignées dans
`requirements-lock.txt`.

## Suite automatique

Commande :

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Résultat exécuté : **44 tests réussis** (dernière exécution : 21,89 s).

Les tests comprennent les configurations invalides, le routage orienté, les
approches alternatives, le CFP unique, les offres périmées, les confirmations
concurrentes, la capacité pendant les opérations, les budgets cumulatifs,
les protections d'approche, la congestion, les frontières temporelles,
les résultats incomplets, les exports et le rejeu sans effet du rendu.
Le scénario par défaut est aussi exécuté avec les assertions actives.

## Exécution du scénario par défaut

Configuration : 21 × 21, cinq axes par direction, 32 bâtiments, huit taxis,
60 demandes entre 0 et 300 s, capacité trois, K = 2, graine 2026.

| Mesure | Résultat observé |
| --- | ---: |
| Statut | Complet |
| Clients livrés | 60 / 60 |
| Dernière descente terminée | 1 113,2 s |
| Distance totale de flotte | 90 400 m |
| Distance à vide | 29 700 m |
| Distance avec au moins deux passagers | 21 400 m |
| Taux de distance partagée | 23,67 % |
| Attente moyenne des 60 clients livrés | 277,53 s |
| Temps moyen à bord | 107,77 s |
| Temps total moyen | 389,31 s |
| Détour moyen | 20 m |
| Retard de congestion | 0 véhicule.s |

Ces résultats décrivent cette graine et cette politique. L'absence de congestion
dans ce scénario est possible avec K = 2 ; les tests contrôlés exercent un
ralentissement non nul. Ce tableau ne démontre pas une réduction de pollution
ou une amélioration par rapport à un mode individuel non exécuté.

Les exports correspondants sont dans `output/default/`. L'image a été inspectée
visuellement. Les résultats sont arrondis ici pour la lecture ; les CSV et JSON
conservent les valeurs numériques.

Trois exécutions supplémentaires ont été réalisées avec les assertions actives :

| Graine et configuration modifiée | Livrés | Fin (s) | Congestion (véhicule.s) |
| --- | ---: | ---: | ---: |
| 17, capacité 4 | 60 / 60 | 1 205,0 | 0 |
| 7, capacité 1, 12 demandes | 12 / 12 | 612,6 | 0 |
| 3, K = 0,5, 12 demandes | 12 / 12 | 1 058,2 | 2 786,4 |

Ces cas vérifient le fonctionnement sur d'autres entrées. Ils ne constituent pas
une expérience comparative contrôlée. Leurs exports sont dans les dossiers
`output/check-seed-*` et les résumés dans `output/verification-runs.json`.

## Interface locale

L'application a été ouverte sur Windows. La carte, les orientations, les
paramètres et les graphiques ont été inspectés. Le pas manuel a fait passer
l'horloge de 0,0 à 0,2 s. Le démarrage a fait progresser la simulation et
la pause l'a arrêtée sans modifier les entrées.

Les exports sont aussi testés par les fonctions utilisées par l'interface.
Le chargement JSON, vérifié dans la version initiale, a depuis été retiré.
Ces tests ne constituent pas un parcours automatisé exhaustif
de toutes les boîtes de dialogue Windows.

## Portée des vérifications

Les tests vérifient les règles sur des scénarios déterministes et les assertions
sur les exécutions réalisées. Ils ne prouvent ni l'absence de tout bug pour toute
configuration, ni le réalisme d'un réseau urbain réel, ni l'optimalité du partage.
Le rapport académique et les expériences comparatives restent des travaux distincts.
