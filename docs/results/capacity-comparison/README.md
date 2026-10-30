# Résultats disponibles : capacité 1 contre capacité 3

Ces fichiers sont une copie des exports de `output/comparison-uturns/`, ajoutée
à la documentation pour être disponible avec le code. L’import documentaire
ne relance pas les expériences. Les résultats ont été produits le 30 octobre
2026, après l’autorisation des demi-tours aux frontières de cellules.

## Protocole effectivement exécuté

- Cinq graines fixées : 2026, 2027, 2028, 2029 et 2030.
- Huit taxis, 60 demandes apparaissant entre 0 et 300 s, carte 21 × 21.
- Une génération par graine, réutilisée pour les capacités 1 et 3.
- Même géométrie, bâtiments, accès, flotte initiale, demandes et horaires dans
  chaque paire ; seule la capacité change.
- Dix simulations complètes, chacune avec 60 clients livrés sur 60.
- Différences calculées par graine : partagé moins individuel. Écart-type
  d’échantillon sur ces cinq différences ; cinq paires utilisables par mesure.

## Fichiers

| Fichier | Utilisation |
| --- | --- |
| [study.json](study.json) | Configuration complète, graines et conventions statistiques |
| [comparison.csv](comparison.csv) | Valeurs par graine et par capacité, écarts et effectifs |
| [summary.csv](summary.csv) | Moyennes, moyenne des écarts et dispersion |
| [provenance.json](provenance.json) | Versions et empreintes du code lors des exécutions |

Les dix fichiers de provenance des exports détaillés étaient identiques ; une
seule copie est conservée ici. Les fichiers détaillés par client, par taxi et
par pas restent dans les exports locaux et peuvent être régénérés par le script.
Les changements ultérieurs de commentaires et d’affichage changent les empreintes
des fichiers source ; la provenance conservée décrit les exécutions d’origine.

## Tableau de lecture

| Mesure | Individuel | Partagé | Moyenne des écarts | Écart-type des écarts |
| --- | ---: | ---: | ---: | ---: |
| Distance totale de flotte (m) | 129 760 | 90 500 | -39 260 | 11 225,33 |
| Attente moyenne par passager (s) | 427,47 | 250,20 | -177,27 | 47,95 |
| Temps total moyen par passager (s) | 532,05 | 360,57 | -171,49 | 46,93 |
| Fraction de distance avec au moins deux passagers | 0 | 0,24005 | +0,24005 | 0,05726 |

Les CSV conservent les valeurs non arrondies. Les fractions sont entre 0 et 1.
Les cinq graines et une seule configuration principale permettent une comparaison
limitée à ces entrées. Elles ne prouvent pas une amélioration générale du trafic
ou une réduction chiffrée des émissions. Les résultats antérieurs sans demi-tour
sont historiques et ne doivent pas être mélangés avec cette étude.

## Régénérer les résultats

Depuis la racine du dépôt dans PowerShell :

```powershell
.\.venv\Scripts\python.exe run_experiments.py --seeds 2026 2027 2028 2029 2030 --output output/comparison-report-check
```

Le dossier distinct préserve les exports existants. Pour la méthode et les
limites, consulter la [validation](../../validation.md), les
[décisions techniques](../../technical-decisions.md) et le
[README du projet](../../../README.md).
