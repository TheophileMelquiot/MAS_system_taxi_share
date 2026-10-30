# Correspondance entre le cahier, le code et les vérifications

Référence : cahier PDF de 48 pages, décisions consolidées jusqu'à U71, actualisées par la décision utilisateur
du 30 octobre 2026 autorisant les demi-tours et le routage entre cellules.
Les numéros ci-dessous sont les sections du cahier. Les tests cités se trouvent
dans `tests/test_scenario.py` et `tests/test_simulation.py`.

Cette matrice est une traçabilité des règles, pas une preuve formelle pour toutes
les configurations possibles. Les assertions complètent les scénarios de test
pendant chaque exécution. Les anciennes descriptions de code ne sont pas traitées
comme des contraintes actuelles.

| Section du cahier | Implémentation ou décision | Vérification principale |
| --- | --- | --- |
| 1. Provenance et priorités | Règles U actuelles, clarifications utilisateur et conventions séparées dans `technical-decisions.md` | Relecture des deux PDF ; historique non importé |
| 2. Objectif et périmètre | `planning.py`, `taxi.py` : multi-passagers, insertions, un taxi par voyage, un seul monde | Partage, capacité réutilisable, cas par défaut |
| 3. Plateforme et outils | `Model`, `Agent`, `AgentSet`, `MultiGrid`, `DataCollector` ; interface Tk locale | Version Mesa installée inspectée, tests et ouverture de l'interface |
| 4. Paramètres et invariants | `Config` et `model.assert_invariants` | Configurations invalides paramétrées, assertions à chaque pas |
| 5. Carte | `draw_axes`, `City` : axes complets, cadre, espacement | Génération par défaut, coins, connexité et accès |
| 6. Bâtiments et accès | Tirage sans remise, accès lexicographique fixe, hors carrefours | Accès et placements invalides, dépassement des emplacements disponibles |
| 7. Orientation | `Move`, orientation visuelle conservée, voisins routiers | Demi-tours après arrêt et frontière de cellule ; portion engagée préservée |
| 8. Routage et validation | `path_to`, BFS entre cellules en cache, `validate_accessibility` | Chemins directs, arrêt sur place, impasse admise, réseau déconnecté refusé |
| 9. Voyages | `generate` : origine uniforme, destination conditionnelle, accès distincts | Rejet d'accès identiques et validation de chaque scénario |
| 10. Apparitions | Calendrier entier de 0 à la borne inclusive ; publication à échéance | Demande future empêchant l'arrêt et invisible aux taxis avant échéance |
| 11. Flotte initiale | Positions distinctes hors carrefours, orientations d'arrivée légales | Génération, nombre excessif refusé, placement invalide refusé |
| 12. Reproductibilité | Quatre flux SHA-256, scénario JSON complet exporté ; chargement retiré à la demande utilisateur | Isolation des flux, export et génération identique, rejeu en mémoire |
| 13. Capacité | Occupation prévisionnelle et réelle, réservations distinctes des places | Trois engagements avec capacité deux, réutilisation capacité un, capacité quatre |
| 14. D0 personnel | `reference_distance` entre accès, sauvegardé dans `Trip` | Distance directe indépendante du sens initial ; référence nulle sur place |
| 15. Budget à bord | `PlanningContext.ridden`, budgets cumulés, contrôle par client | Budget déjà consommé non réinitialisé, budget nul compatible avec partage exact |
| 16. Protection d'approche | Odomètre de confirmation et limite conservés pour chaque engagement | Approche consommée non réinitialisée, assertion à la montée |
| 17. Construction des offres | Insertion pickup/drop sans permutation des anciens arrêts ; distance minimale | Capacité réutilisable, approche directe avec demi-tour, budgets et préfixe cumulés |
| 18. Demandes et messages | `MessageBus`, méthodes séparées des agents, CFP unique | Boîtes indépendantes, appels simultanés, demandes persistantes |
| 19. Validité des offres | Identité incluant le tick, expiration à clôture | Acceptation périmée refusée, offres retirées après ronde |
| 20. Choix client | Début estimé, score maximal, identifiant | Test de classement, vitesse libre et reste d'opération |
| 21. Concurrence | Tri ancienneté/identifiant, revalidation puis engagement cohérent | Acceptations simultanées, capacité, absence de double affectation |
| 22. Horloge et phases | `model.step` délègue neuf phases ; compteur entier | Frontières exactes, absence de double progression, actions indépendantes |
| 23. Durées et arrêts | 36 pas libres, 10 par opération ; descente avant montée | Course de 40 s, place libérée après descente, opération non redémarrée |
| 24. Congestion | `traffic_snapshot`, puis `advance_action` sur les mêmes vitesses | Trois taxis même sens, sens opposé, ordre d'activation inversé |
| 25. Taxis libres | Pas d'action sans engagement, position et orientation conservées | Prise en charge sur place avec inversion du sens initial ; diagnostic de gel défensif |
| 26. Fin et interruptions | Livraison après descente, état figé, plafond | Zéro demande, demande future, fin normale, gel et plafond incomplets |
| 27. Mesures clients | `passenger_rows` : dates, durées, distances, valeurs absentes | Identité des temps, export partiel, attente réellement nulle |
| 28. Mesures taxis | Catégories exclusives 0 à capacité, taux par sommes | Conservation des distances et taux de partage |
| 29. Congestion et pollution | Décomposition circulation/congestion/quantification, sans CO2 | Identité temporelle, cas de congestion non nulle |
| 30. Responsabilités | Deux types d'agents ; géométrie, bus, observation et circulation séparés | Messages explicites, rendu sans effet sur les décisions |
| 31. Qualité du code | Fonctions ciblées, docstrings et commentaires anglais, paramètres centralisés | Tests, compilation et assertions exécutés |
| 32. Interface | `app.py` et `visualization.py`, un monde local | Contrôle visuel, pas manuel, démarrage, pause, rejeu |
| 33. Exports | JSON, CSV, PNG, empreintes source et environnement | Exports partiels et complets, conservation des entrées du scénario |
| 34. Vérifications | Suite pytest et assertions métier | Voir `validation.md` pour les résultats exécutés |
| 35. Comparaisons initialement reportées, ajout minimal autorisé ensuite | `run_experiments.py` : capacités 1 et 3 sur les mêmes entrées, exécutions successives ; interface à un monde | `tests/test_experiments.py` : entrées appariées, paires incomplètes exclues et statistiques des différences |
| 36. Exigences professeur | Bibliothèque Mesa, CFP/réponses, MultiGrid, visualisation et exports | Exécution complète du programme ; rapport académique distinct |
| 37. Principes du cours | États, perceptions, décisions, effets et ordonnancement explicites | Reproductibilité et invariance à l'ordre physique testé |
| 38. Cahier de l'équipier | Uniquement les apports adoptés dans la cible U71 | Pas d'abandon, relance périodique, limite de deux clients ou délai de collecte |
| 39. Programme historique | Absent du dossier ; nouvelle implémentation | Aucune prétention à réutiliser des fichiers absents |
| 40. Organisation historique | Organisation actuelle décrite dans README | Modules indépendants inspectables |
| 41. Documentation | README, décisions, traçabilité et validation | Résultats exécutés distingués des intentions |
| 42. Commandes historiques | Nouvelles commandes réelles documentées | CLI et interface lancées dans `.venv` |
| 43. Anciennes règles | Non réintroduites | Matrice et liste des conventions actuelles |
| 44. Points ouverts | Conventions techniques fixées dans `technical-decisions.md` | Autorisation utilisateur ; choix documentés et testés |
| 45. Collaboration | Français pour explications ; code/commentaires anglais | Pas de modification des PDF sources |

## Limites intentionnelles

Les décisions métier sont respectées par la politique implémentée. Le routage
n'est pas une optimisation globale de flotte et un état figé n'est pas une preuve
d'impossibilité universelle. Le modèle n'inclut pas de feux, files physiques,
trafic extérieur, transferts, marche ou émissions. L'analyse de réalisme urbain
et le rapport final du professeur ne sont pas remplacés par la réussite des tests.
