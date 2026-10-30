> Archive de préparation du 19 octobre 2026, conservée le 27 octobre 2026. Ce document contient des propositions remplacées. Consulter les documents de référence dans le dossier parent pour l'état actuel. Les liens locaux ont été adaptés au dossier d'archive.

# Fiche de conception : taxis partagés

**Statut : exigences reçues et propositions de conception**, mises à jour le 19 octobre 2026. Les exigences viennent de la [session 5](../08_projet_session5.md). Les choix proposés ci-dessous sont une base simple à valider, sans simulation exécutée ni résultat disponible. Les diapos sans préfixe renvoient aux principes de la session 4.

## 1. Sujet et exigences reçues

- Sujet : impact d'un service de taxis partagés sur le trafic et les temps de trajet ; acceptabilité optionnelle (S5 p. 6 et 7).
- Énoncé : `session-5.pdf`, 10 pages, couverture septembre 2026.
- Plateformes autorisées : Python + Mesa ou Java + JADE. Proposition pour ce dossier : Mesa, version à figer ; aucune version imposée.
- Livrables : code source et rapport (« 5-10 pages max »), dimanche 25 octobre 2026 à 23 h 59 CET.
- Évaluation : conception, implémentation, fonctionnalités et utilisabilité, analyse, présentation, 20 % chacun.
- Groupe : 1 ou 2 étudiants, 6 h annoncées par étudiant. Aucune donnée réelle fournie.

## Base de modèle proposée

Cette section préremplit les décisions utiles ; les sections suivantes servent à détailler et réviser cette base. Les valeurs numériques sont des valeurs de démarrage proposées, pas des consignes du professeur ni une calibration.

| Décision | Proposition |
| --- | --- |
| Question | À demande et flotte identiques, partager un taxi à deux réduit-il la distance totale des taxis, et quel est le coût en attente et temps de trajet ? |
| Référence | Un passager maximum par taxi |
| Variante | Deux passagers, second embarquement seulement sur l'itinéraire restant, sans détour |
| Ville | `MultiGrid` de 4 x 4 quartiers, bords non toriques ; plusieurs occupants par cellule |
| Distance et trajet | Distance de Manhattan, trajet déterministe : axe x puis axe y ; chaque cellule représente un quartier |
| Temps | Un tour abstrait, un déplacement entre quartiers voisins par tour ; embarquement d'un tour sans déplacement ; pas d'unité réelle revendiquée |
| Flotte et demande | Démarrage avec 8 taxis et 40 demandes pré-générées entre les tours 0 et 49, origines et destinations distinctes |
| Horizon | Arrêter les nouvelles demandes au tour 50, puis terminer quand tous sont livrés, ou au plafond de 200 tours |
| Extensions exclues du noyau | Marche, correspondances, détours, embouteillages, modèle d'émissions et acceptabilité détaillée |

### Agents et environnement proposés

- **Passager** : identifiant, origine, destination, date de demande et état parmi prévu, en attente, réservé, à bord, livré. Il envoie un CFP, choisit une offre selon l'attente annoncée puis l'identifiant du taxi en cas d'égalité, et attend une confirmation. Dates de prise en charge et d'arrivée conservées.
- **Taxi** : position, capacité, manifeste des passagers, réservations, itinéraire et délai d'embarquement. Il répond aux demandes admissibles, confirme la réservation si une place reste libre et avance selon l'itinéraire. Perception limitée aux messages et aux informations de service définies.
- **Environnement** : grille, calendrier de demandes, livraison des messages, déplacements autorisés, temps simulé et collecte des mesures. L'observateur peut calculer des totaux sans transmettre ces informations aux agents.
- **Passager à bord** : position dérivée de celle du taxi, exclu de la grille jusqu'à la dépose. Cela évite deux positions physiques contradictoires. La visualisation représente aussi les passagers en attente et la charge des taxis.

### Partage sans changement d'itinéraire

Pour un taxi déjà engagé, une seconde demande est admissible si son origine puis sa destination figurent dans cet ordre sur l'itinéraire restant. Le trajet spatial du premier passager reste identique ; l'arrêt supplémentaire peut augmenter sa durée. Le taxi ne change donc pas de route, mais peut ajouter un délai d'embarquement. Les réservations comptent dans la capacité.

### Communication et temps proposés

Le minimum CFP et réponses est une **exigence S5 p. 8**. Proposition de protocole : `CFP`, `OFFER`, `ACCEPT`, `CONFIRM` ou `REJECT`. Chaque message porte l'identifiant de demande, l'émetteur et le destinataire. Une offre seule ne vaut pas réservation. Le taxi revalide place et itinéraire lors de l'acceptation, traite les demandes dans un ordre déterministe et refuse les conflits. Un passager n'a qu'une réservation confirmée ; les autres offres expirent.

Proposition d'un tour : activer les demandes prévues, livrer les messages du tour précédent, percevoir/décider/agir, appliquer les déplacements et embarquements, collecter. Tous les nouveaux messages sont livrés au tour suivant, sans activation répétée d'un même agent dans le tour. En l'absence d'offre ou après refus, le passager relance une demande au tour suivant. Définir avant codage la validité des offres, par exemple 3 tours, et la libération de toute réservation abandonnée.

### Indicateurs proposés

| Mesure | Définition |
| --- | --- |
| Distance totale taxis | Somme de tous les déplacements, à vide ou occupés, en unités de quartier |
| Distance par passager livré | Distance totale divisée par le nombre livré ; non définie si aucun livré |
| Attente | Prise en charge moins date de demande |
| Temps à bord | Arrivée moins prise en charge |
| Temps total passager | Arrivée moins date de demande, attente comprise |
| Service | Nombre et proportion de demandes livrées, réservées, à bord et en attente à l'arrêt |
| Occupation | Passagers à bord par taxi et par tour, avec convention explicite d'agrégation |

Rapporter moyenne et dispersion des durées des passagers livrés, mais aussi les non-livrés et leur attente courante : exclure silencieusement les non-livrés biaiserait la comparaison. La distance est un indicateur indirect de trafic et de pollution, sans prétendre mesurer des émissions ou une congestion réelle.

### Expériences et vérifications proposées

Comparer capacités 1 et 2 avec les mêmes demandes, positions initiales et graines appariées. Pré-générer les demandes évite qu'une politique modifie les futurs tirages de demande. Commencer avec 5 graines, puis augmenter si la dispersion empêche de conclure. Faire varier ensuite la flotte (4, 8, 12) ou la demande (20, 40, 80), un facteur à la fois. Ces nombres sont des propositions ajustables au budget de 6 h.

Vérifier : capacité respectée en incluant les réservations, une seule affectation confirmée par passager, prise en charge avant livraison, aucun déplacement pendant l'embarquement, distance nulle pour un taxi immobile, absence de passager dupliqué dans le manifeste. Tester un passager, deux demandes compatibles, deux incompatibles, deux offres concurrentes et une acceptation devenue impossible. Conserver les non-livrés au plafond d'exécution.

### Construction progressive proposée

1. Modèle Mesa minimal, `MultiGrid`, un taxi et un passager, visualisation spatiale et premier graphique dès cette étape.
2. CFP et réponses, réservation, transport individuel et mesures.
3. Partage à deux sans changement de route, contrôle de capacité et comparaison avec la référence.
4. Exécutions répétées et analyse ; extensions seulement si le noyau est terminé.

Répartition indicative des 6 h par étudiant : 1 h de conception, 2 h de noyau avec visualisation, 1 h de partage et contrôles, 1 h d'expériences, 1 h de rapport et vérification du lancement. Ce budget n'est pas imposé par le professeur.

## Canevas détaillé à finaliser

## 2. Question et cadre expérimental

Formuler une question à laquelle les résultats de simulation pourront répondre. Exemple de forme : « Dans quelles conditions une règle locale R améliore-t-elle la mesure M par rapport à une règle de référence B ? » Cet exemple est une structure de formulation, pas un sujet choisi.

| Élément | Description à remplir |
| --- | --- |
| Système source | Ce que l'on représente et les observations disponibles |
| Question | Ce que l'expérience cherche à établir |
| Hypothèse | Effet attendu d'un mécanisme ou paramètre |
| Référence | Configuration ou politique à laquelle comparer |
| Mesures | Indicateurs, unités et moment de collecte |
| Conditions | Initialisation, paramètres explorés, horizon et arrêt |
| Résultat contradictoire | Observation qui ferait réviser l'hypothèse |
| Domaine de validité | Conditions dans lesquelles le modèle peut informer la question |

## 3. Hypothèses et granularité

Décrire ce que représente un agent, une unité de ressource, une cellule éventuelle et un pas de temps. Lister les mécanismes conservés, les simplifications et leurs conséquences attendues.

| Hypothèse | Justification | Limite introduite | Moyen de l'examiner |
| --- | --- | --- | --- |
| À compléter | À compléter | À compléter | À compléter |

Les paramètres du simulateur ne doivent pas recevoir artificiellement des unités réelles. Si aucune calibration n'existe, les présenter comme des valeurs abstraites.

## 4. Comportement des agents

Copier cette fiche pour chaque type d'agent :

| Élément | Définition |
| --- | --- |
| Type et rôle | Entité active représentée |
| État interne | Variables, valeurs possibles, invariants |
| Informations publiques | Ce que l'agent rend observable et à qui |
| Perception | Sources consultables, portée, visibilité, délai |
| Mémoire | Informations conservées entre activations |
| Décision | Règle, priorités, tirages éventuels |
| Actions possibles | Ensemble des actions autorisées |
| Budget d'action | Ce que permet une activation, y compris les actions composées |
| Effets | Changements demandés au monde |
| Échec ou conflit | Comportement si l'action n'est plus réalisable |
| Naissance et sortie | Règles de création, retrait ou désactivation |

Écrire le déroulement d'une activation en langage naturel avant de l'implémenter : ce qui est perçu, comment l'action est choisie et quels effets peuvent être produits.

## 5. Environnement

- Représentation de l'espace et raison de ce choix : à compléter.
- Ressources partagées, unités et capacité : à compléter.
- Frontières spatiales, obstacles et déplacements : à compléter.
- Dynamique autonome de l'environnement : à compléter.
- Agents ou ressources pouvant entrer et sortir : à compléter.
- Contrats d'observation : à compléter.
- Contrats d'application des actions : à compléter.
- Invariants du monde : à compléter.

**Proposition d'interface** : séparer l'observation d'un agent (`observe`), la vérification d'une action (`validate_action`) et l'application de ses effets (`apply_action`). Les noms restent libres. Ils doivent exprimer un contrat clair et respecter les règles d'information.

## 6. Temps et ordonnancement

| Décision | Choix à documenter |
| --- | --- |
| Unité temporelle | Ce que représente un tour |
| Fréquence | Quels agents s'activent et à quelle fréquence |
| Ordre | Fixe, mélangé, par type ou par événement |
| État observé | Courant ou instantané commun en début de tour |
| Effets | Immédiats ou appliqués en fin de phase |
| Conflits | Règle d'accès à une ressource disputée |
| Dynamique du monde | Moment où les ressources et événements évoluent |
| Mesures | Collecte avant ou après les actions |
| Arrêt | Horizon, convergence, extinction ou autre condition définie |

**Proposition** : vérifier un exemple avec deux agents et une ressource. Faire varier l'ordre de passage et expliquer les différences éventuelles. Cela détecte les ambiguïtés temporelles avant de lancer de grandes simulations.

## 7. Interactions et communication

Décrire les interactions spatiales, les échanges de ressources, les conflits ou les messages utiles au sujet.

Pour ce projet Mesa, les messages CFP et réponses sont requis (S5 p. 8). Documenter :

- Structure : performatif, contenu, émetteur, destinataire et identifiant éventuel.
- Livraison : immédiate, au tour suivant ou selon un délai défini.
- Lecture : phase de perception, ordre et nombre maximal de messages traités.
- Consommation : retrait des messages lus ou conservation explicite.
- Cas particuliers : destinataire retiré, absence de réponse ou doublon.

La session 4 présente le transport personnalisé comme une possibilité ; la session 5 exige une communication directe minimale pour appeler les taxis. Une interaction uniquement implicite par lecture de variables de l'environnement ne suffit donc pas au périmètre proposé ici.

## 8. Mesures, vérification et validation

| Mesure | Définition et unité | Niveau | Moment de collecte | Utilité pour la question |
| --- | --- | --- | --- | --- |
| À compléter | À compléter | Agent ou modèle | À compléter | À compléter |

**Vérification de l'implémentation** : définir les propriétés mécaniques qui doivent rester vraies, puis les cas courts permettant de les contrôler. Exemple conditionnel : pour un échange sans création de monnaie, le total doit rester constant.

**Validation du modèle** : identifier une observation réelle, un résultat analytique ou un fait stylisé à comparer. Si aucune donnée réelle n'est disponible, qualifier les conclusions de résultats sur le modèle et préciser la limite de validité.

## 9. Plan d'expériences

| Expérience | Référence | Paramètre ou mécanisme modifié | Réplications prévues | Mesures comparées |
| --- | --- | --- | --- | --- |
| À compléter | À compléter | À compléter | À compléter | À compléter |

**Proposition** : utiliser plusieurs graines, conserver chaque résultat et montrer la dispersion. Ajuster le nombre de réplications après une exploration courte. Séparer les exécutions qui servent à choisir les paramètres de celles qui servent à apprécier le résultat final.

Pour chaque exécution, prévoir un enregistrement de la version de code, des dépendances, des paramètres, de l'initialisation aléatoire, de la condition d'arrêt et des mesures.

## 10. Construction progressive

1. Une classe d'agent minimale et un environnement limité aux ressources nécessaires.
2. Une interaction traçable sur un cas très court.
3. Le choix explicite du temps, des perceptions et des conflits.
4. Les mesures et contrôles utiles à la question.
5. Les expériences répétées et l'analyse.
6. La visualisation des comportements et résultats.

Ordre proposé pour réduire les ambiguïtés. Le prof demande une progression incrémentale, sans imposer cette liste précise.

## 11. Organisation possible des futurs fichiers

```text
README.md
requirements.txt
src/
    agents.py
    model.py
    metrics.py
    app.py
experiments/
    run_experiments.py
results/
docs/
    conception.md
    hypotheses.md
    analyse.md
```

Cette arborescence est une proposition à adapter. Ne créer un module de messages, de politiques ou d'appels externes que si le sujet le justifie. Le notebook peut servir à l'analyse. Respecter les consignes du dossier : le relire régulièrement et fournir les cellules dans le chat, sans modifier directement un notebook existant sans demande explicite.
