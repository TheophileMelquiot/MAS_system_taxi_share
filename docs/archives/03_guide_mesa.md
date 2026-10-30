> Archive de préparation du 19 octobre 2026, conservée le 27 octobre 2026. Ce document contient des propositions remplacées. Consulter les documents de référence dans le dossier parent pour l'état actuel. Les liens locaux ont été adaptés au dossier d'archive.

# Guide Mesa pour le projet de taxis partagés

Ce guide contient des **compléments officiels** et des **propositions techniques**. Les références au cours utilisent ses numéros de diapositives. Consultation : 11 octobre 2026. Aucun environnement de projet Mesa n'a été installé ou testé à ce stade.

## Priorité aux consignes de la session 5

Mise à jour du 19 octobre 2026 : l'[énoncé](../08_projet_session5.md) recommande **`MultiGrid`**, demande une **communication directe minimale** (CFP et réponses) et une **visualisation dès le début**. Ces choix précisent la préparation générique de la session 4. L'absence d'espace et l'absence de messages ne sont donc pas les choix proposés pour ce projet Mesa.

`MultiGrid` appartient à `mesa.space` et permet plusieurs agents par cellule. Cet espace est en maintenance dans la documentation stable consultée ; sa présence dans les consignes justifie son usage ici. Garder une version qui expose cette classe et vérifier son import avant de développer. Ne pas remplacer silencieusement `MultiGrid` par `CellAgent` et `mesa.discrete_space` : ce sont deux API spatiales différentes. [Source officielle : espaces Mesa](https://mesa.readthedocs.io/stable/apis/space.html).

```python
from mesa.space import MultiGrid

# Dans le constructeur du modèle, après super().__init__(seed=seed) :
self.grid = MultiGrid(width=4, height=4, torus=False)
```

Cet extrait illustre seulement le choix d'espace, pas une classe complète. Les agents sont placés avec `place_agent`, puis déplacés avec `move_agent`. Les propositions de quartiers et de distances sont détaillées dans le [canevas](../04_canevas_conception.md).

Pour un trajet simplifié, conserver une destination et un compteur de tours restant, puis appliquer le déplacement à l'arrivée. Ne pas confondre une coordonnée de cellule et la durée d'un trajet. Une file de messages horodatés peut porter CFP, offres et confirmations. Définir la livraison au tour suivant et revalider les places à la confirmation évite des réservations concurrentes incohérentes. Ce protocole détaillé est une proposition, au-delà du minimum CFP et réponses imposé.

La première version visualisable doit montrer les taxis, les passagers en attente et une mesure temporelle. Le lancement local et les dépendances doivent être documentés, puisque le professeur exécutera le programme. Aucun fichier de simulateur ni résultat de test Mesa n'est fourni par cette préparation documentaire.

## Version et installation

Lors de la consultation, PyPI affiche **Mesa 3.5.1** comme version stable et **4.0.0a0** comme préversion. Le paquet affiché exige **Python 3.12 ou supérieur**. Les extras `rec` et `viz` ajoutent les dépendances recommandées ou de visualisation. [Source : PyPI](https://pypi.org/project/Mesa/).

**Proposition** : utiliser d'abord la version imposée dans le notebook ou l'énoncé. À défaut, Mesa 3.5.1 constitue une base compatible avec les API récentes montrées dans le cours. Ne pas prendre une préversion pour un TP sans raison précise. Les URL `latest` du cours peuvent suivre une version de développement. Les pages `stable` peuvent également évoluer : consigner la version réellement installée.

Commandes PowerShell proposées, si Python 3.12 est installé et si aucune version différente n'est imposée :

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install "mesa[rec]==3.5.1"
.\.venv\Scripts\python.exe -c "import sys, mesa; print(sys.version); print(mesa.__version__)"
```

L'appel direct au Python de `.venv` permet de travailler sans dépendre de l'activation PowerShell. Pour un notebook local, ajouter `jupyterlab` et `ipykernel` dans ce même environnement, puis sélectionner son kernel. Figer ensuite les dépendances réellement retenues dans un fichier de requirements. Le notebook du prof reste la référence de compatibilité dès qu'il est disponible.

## Les composants à connaître

Mesa sépare la modélisation, l'analyse et la visualisation. Un `Model` organise le monde simulé. Les `Agent` représentent les entités actives. Leurs activations passent par `model.agents`, un `AgentSet`. Les espaces décrivent les positions et voisinages. [Source : vue d'ensemble officielle](https://mesa.readthedocs.io/stable/overview.html).

La création des agents appelle le constructeur parent, qui les enregistre. Les identifiants sont gérés par Mesa. L'API documente `model.random` pour les tirages de type Python et `model.rng` pour NumPy. Elle accepte `seed` ou `rng`, avec une seule de ces entrées à la fois. [Source : API Mesa](https://mesa.readthedocs.io/stable/mesa.html).

**Proposition** : faire passer les tirages par l'aléatoire du modèle et conserver les paramètres et versions de chaque expérience. Un appel indépendant à l'aléatoire global rend le contrôle d'une graine insuffisant.

## Activation et temps simulé

Dans les API actuelles, `agents.do("step")` active selon l'ordre de l'ensemble, et `agents.shuffle_do("step")` mélange l'ordre avant l'activation. Depuis Mesa 3.5, `run_for()` et `run_until()` permettent d'avancer le temps. Pour les modèles standards, `run_for(10)` correspond à dix activations du modèle. [Source : guide de migration](https://mesa.readthedocs.io/stable/migration_guide.html).

**Proposition** : choisir entre deux sémantiques et l'expliquer :

- **Activation séquentielle avec effets immédiats** : un agent peut percevoir les changements produits par les agents déjà activés. Le mélange réduit un biais d'ordre fixe sans créer de simultanéité.
- **Décisions sur un même état initial** : tous les agents perçoivent un instantané, proposent une action, puis l'environnement résout les conflits et applique les effets. Cette variante nécessite des règles de résolution explicites.

Dans les deux cas, la boucle de l'agent doit rendre visibles les responsabilités de perception, décision et action demandées par le prof. Éviter de modifier l'ordre ou le budget d'action implicitement lors d'un ajout de fonctionnalité.

## Espace et ressources

Le module `mesa.discrete_space` représente des cellules connectées. Une cellule peut porter des propriétés, suivre ses occupants, limiter leur nombre et donner accès à un voisinage. `CellAgent` représente un agent mobile dans cet espace. Des grilles de Moore ou de von Neumann permettent notamment huit ou quatre voisins. [Source : ajout de l'espace](https://mesa.readthedocs.io/stable/tutorials/4_adding_space.html).

**Proposition générale du cours** : choisir et justifier l'espace pour la question étudiée. **Application au projet S5** : retenir `MultiGrid` comme recommandé, puis définir les bords, la signification des cellules, les durées de déplacement et la portée de perception. La capacité d'un taxi est distincte du nombre d'occupants d'une cellule. Une grille torique relie ses bords opposés ; la base proposée pour la ville est non torique.

## Instrumentation et modèle monétaire

Le tutoriel initial décrit des agents possédant chacun une unité de monnaie. À chaque pas, un agent disposant de monnaie donne une unité à un autre. Il illustre comment des règles simples produisent une distribution collective. [Source : premier modèle officiel](https://mesa.readthedocs.io/stable/tutorials/0_first_model.html).

`DataCollector` enregistre des mesures au niveau du modèle et des agents, puis permet de récupérer des DataFrames. Le tutoriel collecte notamment le coefficient de Gini et la richesse individuelle. [Source : collecte de données](https://mesa.readthedocs.io/stable/tutorials/5_collecting_data.html).

**Proposition** : distinguer les données accessibles à un agent de celles accessibles à l'observateur scientifique. Choisir un moment de collecte, par exemple l'état initial puis la fin de chaque tour, et documenter ce choix. Pour un modèle d'échange sans création de monnaie, contrôler la conservation du total et la non-négativité des richesses. Pour des populations, contrôler plutôt les naissances, décès et effectifs selon les règles du sujet.

## Visualisation

Le tutoriel officiel actuel emploie `AgentPortrayalStyle`, `SpaceRenderer`, `SolaraViz` et `make_plot_component`. Il indique une incompatibilité avec Colab pour cette visualisation et demande des paramètres de modèle nommés. Un fichier contenant la page se lance avec `solara run app.py`. [Source : visualisation de base](https://mesa.readthedocs.io/stable/tutorials/6_visualization_basic.html).

**Proposition** : commencer par Solara, la méthode standard présentée dans le cours. Utiliser l'alternative `mesa_graphics` si ses fichiers et sa version compatible sont disponibles. Ne pas recopier un numéro d'onglet de cette interface dans Solara sans vérifier son API.

Un portrayal doit seulement traduire un état en forme, taille et couleur. Un graphique temporel explique une trajectoire. Un histogramme montre une distribution à un instant donné. Le rendu ne devrait pas provoquer de tirage aléatoire ni modifier le modèle : activer l'interface changerait alors les résultats de simulation.

## Corrections à connaître dans le support

| Référence | Écriture ou limite observée | Correction ou lecture proposée |
| --- | --- | --- |
| Diapo 18, page 26 | `mesa.discretespace` | Utiliser le nom documenté `mesa.discrete_space` |
| Diapo 22, page 30 | Liste `others`, puis `choice(cellmates)` | Coquille de variable. Même corrigé, ce contre-exemple reste une pratique critiquée |
| Diapo 23, page 31 | `self.model.schedule.agents` | Exemple de style ancien. Le cours utilise `self.model.agents` dans ses exemples positifs |
| Diapo 23, page 31 | Affectation à `self.x`, puis argument `x` | `x` n'est pas défini dans le fragment visible. Ne pas reprendre ce code comme exemple fonctionnel |
| Diapo 27, page 35 | `...` et `read_messages()` non définie | Schéma à compléter, avec règles de lecture et de livraison |
| Diapo 31, page 39 | `portrayal.update(("color", ...), ("size", ...))` | Préférer une construction explicite d'`AgentPortrayalStyle` avec les valeurs voulues, conforme à l'exemple officiel |
| Diapo 34, page 42 | `rederer` | Harmoniser en `renderer` |
| Diapo 36, page 45 | `SolaraViz/MesaGraphics(...)` | Choisir une classe. La barre oblique exprime une alternative pédagogique |
| Diapo 37, page 46 | L'API objet présentée comme solution aux problèmes de threads | Elle évite l'état global de pyplot, mais ne garantit pas la sûreté en concurrence |

La FAQ Matplotlib indique explicitement que la bibliothèque n'est pas sûre en concurrence et que l'accès aux objets graphiques doit être sérialisé si des threads interviennent. Les interfaces graphiques requièrent souvent le thread principal. [Source : FAQ Matplotlib](https://matplotlib.org/stable/users/faq.html#work-with-threads).

Le code extrait du PDF perd des espacements et de l'indentation. Utiliser l'image de la page pour départager une coquille visible d'une erreur d'extraction. Les fragments décrits ici n'ont pas fait l'objet d'un test d'exécution avec Mesa.

## Extension facultative avec un LLM

Cette section est une **proposition conditionnelle**, extérieure aux exigences de S5. Aucun LLM n'est demandé pour les taxis partagés ; cette extension n'est pas retenue dans le noyau proposé. Si elle est ajoutée, garder une politique simple sans LLM comme point de comparaison. Donner au modèle de langage uniquement les perceptions autorisées, lui demander une action issue d'un ensemble défini, et vérifier cette action dans l'environnement. Mesurer séparément les résultats de simulation, la latence et le coût des appels.

Prévoir un comportement lorsque la réponse arrive trop tard ou ne respecte pas le format. Gérer les appels depuis un composant dédié si leur durée bloque la boucle. Une graine Mesa ne garantit pas à elle seule la reproductibilité d'un service externe : conserver aussi les entrées et réponses utilisées pour une expérience rejouable.
