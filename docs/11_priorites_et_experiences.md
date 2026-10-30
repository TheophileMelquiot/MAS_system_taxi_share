# Priorités et expériences proposées

> Actualisation du 30 octobre 2026 : ce document conserve une description historique. Le code actif se trouve à la racine de ce dépôt. Les demi-tours aux frontières de cellules sont désormais autorisés, avec congestion séparée par sens et actions engagées préservées. Les comparaisons capacité 1 / 3 sont implémentées. Lire les [décisions techniques actuelles](technical-decisions.md) et la [validation](validation.md).


> Statut au 28 octobre 2026 : ce plan conserve les recommandations historiques du 27 octobre, dont plusieurs questions ont ensuite été résolues. Pour les règles et paramètres courants, lire la [synthèse](04_canevas_conception.md) et les décisions jusqu'à U71 dans le [registre](10_decisions_et_reprise_llm.md). Les correspondances restent exclues, les comparaisons reportées et les émissions non modélisées pour la version courante. Ce plan ne constitue pas une nouvelle liste de décisions à prendre.

> Priorité actuelle, U21 et U22 : développer une seule simulation avec des états et délais indépendants pour chaque taxi. Un taxi qui attend ne bloque pas les autres. Les modes à un passager et les comparaisons sont reportés ; les descriptions de deux simulations ci-dessous concernent l'existant ou des travaux ultérieurs, sans imposer une exécution simultanée. Aucun code n'a été modifié lors de cette clarification.


> Objectif final clarifié le 27 octobre 2026 (U14) : la version individuelle et le partage à deux sans détour sont des démonstrations intermédiaires. La cible finale est élargie, notamment aux détours et à une progression vers les niveaux avancés du sujet. Les règles ci-dessous décrivant la version actuelle ne fixent pas le périmètre final. Voir le [registre des décisions](10_decisions_et_reprise_llm.md).


Date : 27 octobre 2026. Statut : recommandations de l'assistant à discuter. Aucun changement du simulateur, aucune expérience exécutée et aucune nouvelle décision fonctionnelle de l'utilisateur dans ce document.

## Diagnostic au regard du barème

L'énoncé demande une étude par simulation, avec une conception simple, des observables et des résultats analysés. Les cinq catégories valent chacune 20 %. La documentation décrit déjà un périmètre répondant aux attentes Mesa : agents, MultiGrid, messages directs et visualisation. Cette couverture documentaire ne prouve pas que le programme fonctionne sur un autre ordinateur.

Aucun rapport final ou fichier de résultats n'a été repéré dans les fichiers examinés au moment du nettoyage. Il faut donc produire ou retrouver les preuves expérimentales avant d'affirmer que la partie analyse est terminée. Les tests précédemment rapportés ne sont pas une nouvelle vérification.

## Priorités expérimentales pour une étape ultérieure, selon U21

| Priorité | Amélioration proposée | Motif et critère de réussite | Rapport au professeur |
| --- | --- | --- | --- |
| 1 | Produire des comparaisons répétées sur les mêmes scénarios | Figures et tableaux issus d'exécutions complètes ; résultats reproductibles et dispersion visible | Analyse et variables observables explicitement demandées ; répétitions proposées |
| 1 | Rédiger un rapport court expliquant la question, les règles, les résultats et les limites | Chaque conclusion renvoie à une mesure ; chaque simplification importante est justifiée | Rapport, conception et présentation demandés |
| 1 | Vérifier une installation et un lancement suivant uniquement le README | Interface utilisable, comparaison exportée et scénario rejoué ; noter l'environnement testé | Le professeur annonce qu'il exécutera les programmes |
| 2 | Mesurer si le partage a effectivement lieu | Lire la distance partagée et les parcours des passagers ; distinguer faible opportunité et absence d'effet du mécanisme | Diagnostic proposé pour interpréter les résultats |
| 2 | Examiner l'interdiction d'un second engagement pendant l'approche, L07 | Cas contrôlé : deux demandes de même origine et destination pendant l'approche ; documenter le comportement avant de décider une modification | Convention révisable du projet, aucune obligation du professeur |
| 2 | Tester la sensibilité au seuil de congestion | Comparer K=1, 2 et 4 sur les mêmes scénarios ; vérifier si les conclusions dépendent surtout de cette hypothèse | Justification du modèle ; congestion optionnelle dans l'énoncé, retenue par l'utilisateur |
| 3 | Améliorer les indicateurs de synthèse si nécessaire | Ajouter après examen des exports un taux de partage défini et une durée élevée, par exemple le 90e percentile | Extension d'analyse proposée, pas une exigence |

## Protocole expérimental proposé, reporté selon U21

Conserver la carte, les constantes physiques et la politique d'affectation. Pour chaque configuration, comparer individuel et partagé avec exactement le même scénario et la même liste de graines. Ne pas sélectionner uniquement les scénarios favorables.

| Série | Taxis | Demandes | Fenêtre d'apparition | K | But |
| --- | --- | --- | --- | --- | --- |
| Référence | 8 | 30 | 300 s | 2 | Point de départ actuel |
| Demande accrue | 8 | 60 | 300 s | 2 | Effet d'une demande plus élevée à flotte constante |
| Flotte réduite | 4 | 30 | 300 s | 2 | Effet de la disponibilité des taxis |
| Demande concentrée | 8 | 30 | 60 s | 2 | Effet de demandes plus rapprochées |

Ces nombres sont des propositions de départ, sans calibration. Commencer avec cinq graines identiques entre séries, puis augmenter si les effets varient fortement. Les options documentées permettent par exemple :

```powershell
.\.venv\Scripts\python.exe run_experiments.py --seed 42 --replications 5 --taxis 8 --requests 30 --window 300 --threshold 2 --output results/study/reference
.\.venv\Scripts\python.exe run_experiments.py --seed 42 --replications 5 --taxis 8 --requests 60 --window 300 --threshold 2 --output results/study/demand
.\.venv\Scripts\python.exe run_experiments.py --seed 42 --replications 5 --taxis 4 --requests 30 --window 300 --threshold 2 --output results/study/fleet
.\.venv\Scripts\python.exe run_experiments.py --seed 42 --replications 5 --taxis 8 --requests 30 --window 60 --threshold 2 --output results/study/window
```

Ces commandes n'ont pas été exécutées pour cette mise à jour. Vérifier et consigner la liste effective des graines utilisée par les réplications. Le README présente aussi un scénario chargé à 20 taxis et 90 demandes : utile en démonstration, il modifie plusieurs facteurs et ne suffit donc pas à isoler une cause.

Pour la sensibilité à K, garder les autres paramètres de la référence et produire de nouveaux scénarios avec K=1 et K=4. Un JSON chargé remplace les options de génération : modifier seulement `--threshold` tout en rechargeant le même JSON ne change pas K.

## Analyse attendue

Pour chaque paire complète, relever distance totale, attente moyenne, temps total moyen, retard de congestion, distance partagée et nombre de passagers livrés. Calculer d'abord la différence partagé moins individuel pour chaque scénario, puis résumer ces différences entre graines avec leur dispersion. Une différence négative est favorable pour distance, attente et durées. Si la référence vaut zéro, ne pas calculer un pourcentage de variation.

Examiner aussi la distribution des temps par passager dans les exports : une moyenne peut masquer quelques attentes élevées. La proportion de distance partagée peut se calculer comme distance partagée divisée par distance totale si cette dernière est non nulle. Ce ratio ne mesure pas la proportion de passagers partageant un taxi.

Si aucun partage ou ralentissement n'apparaît, le signaler et examiner les opportunités de regroupement et les charges. Un scénario contrôlé avec demandes compatibles démontre un mécanisme ; il ne remplace pas l'analyse de scénarios générés.

## Progression vers la cible finale, clarification U14

Pour la démonstration actuelle, un candidat est L07 : permettre éventuellement de réserver deux passagers compatibles pendant l'approche du premier. Cette modification répondrait aux occasions manquées possibles pour des départs identiques. Elle exige de revalider capacité et trajet et de comparer avant/après sur les mêmes scénarios. Elle n'est pas appliquée ici.

La formule de congestion mérite une sensibilité documentée avant de la complexifier. Conserver l'expression « ralentissement par charge » et expliquer l'absence de files, de feux et de trafic extérieur. L'acceptabilité peut rester hors périmètre, en le disant dans le rapport. La recommandation précédente de conserver le périmètre initial est remplacée par U14. La cible finale comprend les détours. Il faut ensuite préciser les étapes avancées, notamment le sens de multi-hop et la capacité finale, sans les confondre avec les fonctionnalités déjà réalisées.

## Étapes suivantes proposées pour la cible finale

1. Développer une seule simulation ; reporter la construction des modes de référence et de comparaison selon U21.
2. Définir et ajouter le partage avec détour : insertion des prises en charge et déposes, respect de capacité, calcul du surtemps pour les passagers déjà engagés. Les limites de détour restent à décider.
3. Préciser multi-hop et le partage à plusieurs : correspondances entre taxis ou étapes d'itinéraire, capacité et règles de réservation. Aucun choix détaillé n'est encore confirmé.
4. Comparer les niveaux successifs sur des scénarios communs, avec mesures de distance, attente, temps total et congestion ; justifier le traitement de l'acceptabilité, optionnelle dans l'énoncé.

Ces étapes sont une proposition de progression en réponse à U14, pas une implémentation effectuée.

## Plan de rapport proposé, plafond pratique de dix pages

1. Question, objectifs et périmètre : environ une page.
2. Agents, espace, information, messages et temps : environ deux pages.
3. Implémentation, utilisation et vérifications : environ une page.
4. Protocole, figures et analyse des résultats : environ trois pages.
5. Discussion, limites et conclusion : environ une page.

Ce plan est proposé. Le professeur écrit « 5-10 pages max » sans préciser le traitement des annexes. Les limites doivent distinguer correction mécanique, robustesse des résultats et validité du modèle pour une ville réelle.


## Objectifs ajoutés par l'utilisateur : carte générée et priorité Mesa

**U15 : génération automatique conditionnée à la simplicité.** Étudier une génération de routes et bâtiments sans géométrie saisie à la main. Critères : réseau connecté, bâtiments accessibles, carte reproductible et sauvegardée, mêmes entrées pour tous les modes. La piste L20 propose des axes routiers qui se croisent ; elle reste à évaluer. Commencer par une seule carte commune pour comparer les politiques, puis comparer plusieurs cartes afin d'examiner la sensibilité à la géométrie.

**U16 : revue des outils disponibles avant toute réimplémentation.** Dresser pour chaque composant concerné une comparaison courte : besoin, outil Mesa compatible, éventuelle limite et choix motivé. Examiner en priorité collecte des mesures, exécutions répétées, aléatoire et visualisation, en plus des agents et de MultiGrid déjà utilisés. Ne pas annoncer de remplacement avant d'avoir vérifié les API de la version retenue.

Ces deux objectifs sont confirmés ; leur réalisation ne l'est pas. La génération ne doit pas absorber l'effort nécessaire aux détours, aux niveaux avancés et à l'analyse demandée.


## Lisibilité et fiabilité des comportements, U17

Revoir prioritairement les comportements volumineux : distinguer la réception et l'évaluation des demandes, les choix, les réservations et l'exécution physique lorsque ces responsabilités sont mêlées. Garder des blocs courts ayant chacun un rôle clair, sans morceler artificiellement le déroulement.

Conserver un environnement global cohérent. Des agents ou services complémentaires sont possibles si leur utilité est concrète. Cette orientation précise U08 et ne constitue pas une demande de multiplier les sous-étapes du modèle. Lors d'une future refonte interne, préserver les résultats des scénarios de référence ; documenter séparément toute évolution fonctionnelle, par exemple les détours. Le nombre de lignes seul ne démontre pas la robustesse.


## Réduction du codage en dur, U19

Lors de la prochaine revue du code, repérer les dépendances à la carte fixe, les constantes dispersées et les branches propres à un scénario. Classer chaque élément : paramètre à centraliser, donnée à générer ou charger, politique à isoler, invariant à conserver. Donner la priorité aux éléments qui bloquent les cartes générées, les détours ou la capacité finale. Ne pas transformer toutes les règles en options ; maintenir un modèle simple et documenter les choix fixes. Cette revue n'a pas été effectuée par la présente mise à jour documentaire.


## Éviter l'accumulation de rustines, U20

Les évolutions vers une carte générée, les détours et les niveaux avancés peuvent justifier le remplacement de composants conçus pour la démonstration. Ne pas forcer leur adaptation si elle exige un effort disproportionné ou dégrade la structure. Préférer alors une réécriture propre au périmètre pertinent, avec retrait du code remplacé et mise à jour des explications. Garder les scénarios de référence utiles pour vérifier ce qui doit rester identique et documenter les nouvelles règles séparément. Aucun remplacement n'est réalisé par cette mise à jour documentaire.

## Priorité immédiate selon U21 et U22

Construire une simulation unique cohérente, en conservant les objectifs de carte générée, détours et niveaux avancés. Garantir les états et délais individuels : un taxi en arrêt n'empêche pas un autre de circuler ou de répondre à une demande. Vérifier ce comportement sur un scénario court avant les futures comparaisons. Le protocole comparatif ci-dessus reste une proposition pour plus tard.
