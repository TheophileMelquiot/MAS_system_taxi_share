# Consignes du prof et conséquences pour la conception

Sources : [session 4](sources/session-4.pdf) et [session 5](sources/session-5.pdf). Mise à jour : 19 octobre 2026. **Cours** désigne les principes de S4 ; **Projet S5** désigne l'énoncé ; **Proposition** désigne un choix suggéré. Les diapos non préfixées dans la suite concernent S4.

## Exigences du projet (session 5)

| Référence | Consigne explicite |
| --- | --- |
| S5 p. 4 | Groupe de 1 ou 2 ; 6 h de travail par étudiant (3 h en séance, 3 h à la maison) |
| S5 p. 4 | Python + Mesa ou Java + JADE ; autres plateformes MAS et MAS maison sans bibliothèque interdits |
| S5 p. 4 | Remise dimanche 25 octobre 2026 à 23 h 59 CET |
| S5 p. 5 | Code source et rapport, formulation « 5-10 pages max » |
| S5 p. 6 | Étudier le partage de taxis, le trafic, les temps de trajet et l'acceptabilité |
| S5 p. 6 | Concevoir par incréments, identifier tôt les paramètres et variables observables, simplifier |
| S5 p. 7 | Acceptabilité et embouteillages explicitement optionnels |
| S5 p. 8, Mesa | `MultiGrid` recommandé ; communication directe minimale requise, CFP et réponses ; visualisation dès le début |
| S5 p. 9, JADE | Pas d'interface, journalisation et tableur ; agents quartiers, temporisations, contrôle CPU |

### Barème sur 20

| Critère | Poids |
| --- | --- |
| Choix de conception expliqués dans le rapport | 20 % |
| Implémentation et bon usage de la bibliothèque | 20 % |
| Fonctionnalités et utilisabilité, programme exécuté par le professeur | 20 % |
| Analyse des résultats dans le rapport | 20 % |
| Présentation, organisation du rapport, commentaires du code | 20 % |

Les quatre niveaux de partage de S5 p. 6 sont une progression donnée en exemple, sans obligation explicite d'implémenter tous les niveaux. La grille n'a pas à représenter une carte détaillée. Les sauts entre cellules avec un compteur de durée sont autorisés. Aucun LLM n'est imposé. Voir [l'énoncé commenté](08_projet_session5.md) pour la lecture complète.

## Les pratiques explicitement critiquées

| Référence | Ce que le prof critique | Pourquoi cela pose problème | Proposition pour le projet |
| --- | --- | --- | --- |
| Diapo 22, page 30 | Lire directement l'état interne d'un autre agent | L'agent dispose d'informations qu'il n'a pas nécessairement perçues ni reçues | Définir les observations autorisées et passer par une perception, une information publique ou un message |
| Diapo 23, page 31 | Mettre tout le comportement dans `step()` sans séparer les phases | La perception et les effets des actions deviennent difficiles à identifier | Garder une boucle courte avec `perceive()`, `decide()` et `act(action)` |
| Diapo 23, page 31 | Masquer une perception globale dans une somme sur tous les agents | Elle peut contourner les limites de connaissance et coûter O(N²) sur un tour complet | Justifier toute connaissance globale, utiliser un voisinage ou un calcul partagé quand le modèle l'autorise |
| Diapo 23, page 31 | Exécuter deux actions dans le même tour dans l'exemple présenté | Le budget d'action et les règles temporelles deviennent ambigus | Écrire ce qu'un agent peut effectuer pendant une activation, puis vérifier cette règle |
| Diapo 25, page 33 | Effectuer un calcul long dans la boucle procédurale | Pendant ce calcul, les autres agents ne s'exécutent pas | Réduire le calcul, précalculer ou gérer le traitement externe depuis l'environnement si nécessaire |

Une observation globale n'est pas intrinsèquement interdite pour l'instrumentation. Le calcul d'un indicateur par l'observateur et l'affichage de richesses sont présents dans les exemples. La critique porte sur une information utilisée par un agent sans perception définie. Cette distinction est une **interprétation de conception**, cohérente avec les diapos 22, 23, 31 et 37.

## Les pratiques explicitement recommandées

| Référence | Recommandation du cours | Application proposée |
| --- | --- | --- |
| Diapos 5 et 6, pages 5 et 6 | Modéliser, exécuter, analyser, puis réviser de façon itérative | Faire évoluer le modèle à partir des expériences et conserver les raisons des changements |
| Diapo 8, pages 9 à 15 | Définir le système source et le cadre expérimental | Formuler la question étudiée, les conditions et ce qui permettrait d'y répondre |
| Diapo 8, page 15 | Distinguer validité du modèle et correction de son exécution | Séparer les arguments de réalisme des vérifications de code |
| Diapo 14, page 22 | Réutiliser la démarche MAS et travailler par incréments | Commencer par un noyau réduit, observer son fonctionnement, puis ajouter les mécanismes nécessaires |
| Diapo 14, page 22 | Lister les entités actives et leurs actions | Faire une fiche par type d'agent, avec état, observations et actions |
| Diapo 14, page 22 | Choisir la granularité | Préciser ce que représente un agent et ce que représente un pas de temps |
| Diapo 14, page 22 | Définir les interactions et éventuellement l'organisation | Décrire les échanges, règles collectives et conséquences des actions |
| Diapo 14, page 22 | Inventorier les ressources partagées et la spatialisation | Identifier les objets de l'environnement et leurs règles d'accès |
| Diapo 14, page 22 | Examiner discret, dynamique, ouvert et synchronicité | Documenter l'espace, l'évolution autonome et les entrées ou sorties d'agents |
| Diapo 15, page 23 | Traiter comportement, environnement, ordonnancement et interaction | Remplir les quatre parties du canevas de conception |
| Diapo 24, page 32 | Expliciter perception, décision et action | Relire la boucle d'agent avec ces trois responsabilités |
| Diapo 25, page 33 | Si nécessaire, utiliser un traitement externe, de préférence dans l'environnement | Centraliser les tâches lentes et définir quand leur résultat devient utilisable |
| Diapo 27, page 35 | Possibilité de créer son propre mécanisme de messages | Si des messages sont utiles, définir contenu, émetteur, destinataire et livraison |
| Diapo 29, page 37 | Utiliser un environnement virtuel pour l'installation locale | Isoler les dépendances du TP et consigner leurs versions |
| Diapo 29, page 37 | Utiliser un modèle simple selon KISS | Retenir les mécanismes nécessaires à la question posée |
| Diapo 30, page 38 | Définir portrayal, paramètres et renderer | Préparer une visualisation séparée du comportement des agents |
| Diapo 30, page 38 | Utiliser une installation locale pour la visualisation, de préférence autonome | Prévoir un fichier d'entrée pour l'interface lorsque le modèle sera prêt |
| Diapo 37, page 46 | Créer les figures avec l'API objet Matplotlib | Utiliser `Figure` et `ax.hist`, puis traiter séparément la synchronisation si des threads interviennent |

## Atouts et limites des méthodes selon le prof

- **Cours, diapos 7 et 8** : les sorties d'un système peuvent être connues sans que sa structure interne le soit. Le modèle doit alors expliciter ses hypothèses. Le formalisme choisi limite les observations possibles.
- **Cours, diapo 10** : les MABS aident à étudier l'émergence à partir de choix individuels, les situations stables et le niveau microscopique. Ils complètent les modèles à équations.
- **Cours, diapo 12** : les équations représentent bien les variations globales, mais sans individus explicites. Les MABS décrivent les entités et leurs interactions, mais leur comportement collectif reste parfois difficile à comprendre. Les deux approches peuvent avoir beaucoup de paramètres.
- **Cours, diapo 13, page 21** : trouver les paramètres qui reproduisent un fait stylisé constitue une difficulté de conception.
- **Cours, diapo 26** : le support ne présente pas de transport de messages fourni par défaut. La diapo suivante autorise à en écrire un. Il ne s'agit donc pas d'une interdiction de toute communication.
- **Cours, diapos 29 et 30** : l'exécution du modèle peut se faire dans Colab, mais la visualisation présentée nécessite une installation locale.
- **Cours, diapo 35** : l'interface `mesa_graphics` est annoncée comme limitée à Windows dans cette version du support. Ce statut actuel n'a pas pu être confirmé en ligne.

## Ce qu'il faut interpréter avec précision

### Une action par tour

Le prof critique explicitement deux actions dans le contre-exemple de la diapo 23. Le support ne définit pas une règle universelle pour tous les modèles. Les tutoriels Mesa officiels peuvent combiner déplacement et échange dans une activation. **Proposition** : décider si le déplacement et l'interaction sont deux actions distinctes ou les parties d'une action composée, puis rendre cette règle explicite. L'objectif pédagogique est de maîtriser le temps et les effets du comportement.

### Encapsulation et accès Python

Le fait qu'un attribut soit accessible en Python ne justifie pas sa consultation par un autre agent. **Proposition** : distinguer les états internes, les informations publiques et les observations autorisées. Une méthode publique peut elle aussi révéler trop d'informations. Son contrat doit respecter le modèle de perception.

### Calculs externes et threads

La diapo 25 conseille une externalisation si nécessaire. Elle ne garantit ni vitesse supérieure, ni déterminisme, ni absence de conflits d'accès. **Proposition** : définir un point de récupération des résultats et appliquer les changements du monde dans une phase maîtrisée. Un thread qui modifie la grille pendant l'activation introduirait une nouvelle sémantique à justifier.

## Précisions toujours absentes

La session 5 fixe le thème, les plateformes, les livrables, le groupe, l'échéance et le barème. Elle ne précise pas le nombre d'agents, les paramètres numériques, la version de Mesa, le canal de dépôt, le format d'archive, le traitement des annexes ou une éventuelle soutenance. Le professeur ne fixe pas les formules exactes des métriques. Le projet a retenu ses propres définitions, à expliquer et à justifier dans le rapport.

La [fiche de conception](04_canevas_conception.md) synthétise les décisions actuelles. Les formules retenues sont décrites dans [le modèle documenté](09_modele_implemente.md) ; leur justification expérimentale reste à apporter. Les propositions de la checklist restent distinctes des exigences et du barème annoncés.
