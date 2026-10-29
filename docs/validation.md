# Vérifications effectuées

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

Les exports et le chargement JSON sont aussi testés par les fonctions utilisées
par l'interface. Ces tests ne constituent pas un parcours automatisé exhaustif
de toutes les boîtes de dialogue Windows.

## Portée des vérifications

Les tests vérifient les règles sur des scénarios déterministes et les assertions
sur les exécutions réalisées. Ils ne prouvent ni l'absence de tout bug pour toute
configuration, ni le réalisme d'un réseau urbain réel, ni l'optimalité du partage.
Le rapport académique et les expériences comparatives restent des travaux distincts.
