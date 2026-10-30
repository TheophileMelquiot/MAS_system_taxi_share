# Cours commenté : session 4, simulation

**Mise à jour du dossier, 19 octobre 2026** : le sujet et les exigences sont maintenant disponibles dans la [session 5 commentée](08_projet_session5.md). Le présent document conserve la lecture de la session 4 ; les phrases sur ce qu'elle ne précise pas décrivent uniquement ce support.

Source : [support de Nicolas Sabouret](sources/session-4.pdf), Université Paris-Saclay, M1 DKAI, « Foundations of Agent-based systems », couverture datée de septembre 2026. Cette lecture couvre les 38 diapositives. Le [texte intégral](slides/texte_integral.md) conserve les détails anglais et les exemples tels qu'extraits. Les [figures](06_analyse_visuelle.md) complètent la lecture.

## Diapo 1, page 1 : présentation

La session 4 traite de simulation. La couverture contient une capture NetLogo du modèle Wolf Sheep Predation, avec une grille, des paramètres et des courbes de populations. Elle introduit la simulation spatiale et l'observation des résultats.

## Diapo 2, page 2 : calendrier

| Date annoncée | Séance et répartition |
| --- | --- |
| 7 septembre 2026 | Introduction : 1 h 30 de cours sur les bases des MAS, 30 min de modélisation, 1 h de pratique MAS en Java |
| 14 septembre 2026 | Communication et plateformes : 1 h de cours, 1 h de pratique Java, 1 h de tutoriel JADE |
| 28 septembre 2026 | Séance pratique JADE |
| 5 octobre 2026 | MABS : 1 h de théorie et 2 h de TP Mesa |
| 12 octobre 2026 | Séance pratique : projet MABS |
| 19 octobre 2026 | Agentic AI : séance pratique |

La flèche met en évidence la séance du 5 octobre. Le calendrier décrit une progression entre systèmes multi-agents, simulation et IA agentique.

## Diapo 3, page 3 : thème

La séance s'intitule « MultiAgent Based Simulation », abrégé MABS.

## Diapo 4, page 4 : plan

Le cours présente la simulation, la simulation multi-agents et la plateforme Mesa. Le TP porte sur les bases de Mesa avec le modèle monétaire, puis sur la visualisation avec Solara ou une interface pygame.

## Diapo 5, page 5 : définition d'une simulation

La définition attribuée à Shannon (1977) associe la conception d'un modèle d'un système réel à des expériences sur ce modèle. Le but peut être de comprendre son comportement ou d'évaluer différentes stratégies de fonctionnement.

Le schéma montre une abstraction de la réalité vers le modèle, une simulation du modèle donnant un résultat, puis une révision du modèle à partir du résultat. Les objectifs cités sont le test d'hypothèses, l'étude des situations stables et l'étude de la résilience.

## Diapo 6, page 6 : simulation informatique

La démarche attribuée à Fishwick (1997) est itérative : concevoir le modèle d'un système physique, l'exécuter sur un ordinateur, analyser les sorties. Une image météorologique illustre un système dynamique spatial.

## Diapo 7, pages 7 et 8 : systèmes dynamiques et boîte noire

La majorité des systèmes étudiés évoluent dans le temps. Le comportement externe, notamment les réactions aux entrées, peut être observable alors que la structure interne et la dynamique restent inconnues. Le dessin représente une entrée, un état interne et une sortie. Un agent est lui-même un système dynamique.

La simulation informatique permet de produire une spécification formelle, mais le manque de connaissances internes limite la modélisation. Le choix du formalisme contraint également ce qui peut être observé. La page 8 ajoute visuellement ces limites à la page 7.

## Diapo 8, pages 9 à 15 : méthodologie de modélisation et simulation

La diapositive construit progressivement un schéma à quatre éléments et deux relations :

1. **Système source** : le système à modéliser, dont proviennent les données observables.
2. **Cadre expérimental** : ce que l'on veut étudier, avec les objectifs et les conditions de simulation.
3. **Modèle** : les spécifications censées reproduire le comportement étudié.
4. **Simulateur** : le système informatique qui exécute le modèle.
5. **Relation de modélisation** : validité du modèle par rapport au système physique.
6. **Relation de simulation** : correction de l'implémentation par rapport au modèle.

La page 9 n'affiche que le titre. Les pages suivantes introduisent les éléments successifs. Le diagramme complet apparaît page 15. Il distingue deux questions essentielles : le modèle représente-t-il correctement ce que l'on étudie, et le programme exécute-t-il correctement ce modèle ?

## Diapo 9, page 16 : définition de MABS

Un système multi-agents simule un système dynamique. Les agents correspondent aux entités physiques étudiées. Leurs actions et interactions représentent les comportements.

Les exemples cités comprennent la simulation sociale (opinions, circulation, ménages), les phénomènes physiques (météorologie, géologie, pandémies) et les systèmes techniques (réseau électrique). Les images montrent une simulation sur carte et une interface de simulation d'activités et de consommation d'un ménage.

## Diapo 10, page 17 : intérêt des MABS

Lorsque des équations ne capturent pas tous les aspects d'un système complexe, on peut représenter des sous-systèmes plus simples puis les combiner. L'objectif est d'étudier les phénomènes émergents issus des choix individuels et de trouver des régions de paramètres où apparaissent des situations stables.

Le prof cite l'analyse microscopique comme aide à l'explication, une modélisation proche de la réalité, et la possibilité de calcul distribué ou de simulations parallèles. Les MABS complètent les modèles à équations. Cette possibilité générale de parallélisation ne signifie pas que l'activation Mesa présentée plus loin exécute les agents en parallèle.

## Diapo 11, page 18 : exemple proies-prédateurs

Le but est d'étudier l'évolution des deux populations dans le temps. Le modèle à équations, attribué dans le support à « Voltera, 1926 », utilise `x` pour les proies et `y` pour les prédateurs :

```text
dx(t)/dt = a*x(t) - b*x(t)*y(t)
dy(t)/dt = c*x(t)*y(t) - d*y(t)
```

Le support décrit `a` et `c` comme des taux de reproduction, `b` et `d` comme des taux de mortalité. La lecture des équations précise le rôle des termes : `a*x` augmente les proies, `b*x*y` représente les pertes par rencontre avec les prédateurs, `c*x*y` augmente les prédateurs grâce à ces rencontres, `d*y` représente leur mortalité. Cette interprétation mathématique détaille le raccourci du support.

La figure de droite associe une capture NetLogo et des courbes périodiques. Les proies, en bleu, culminent avant les prédateurs, en orange pointillé. Les axes indiquent le temps et la population, sans unités physiques précises ni paramètres du tracé.

## Diapo 12, page 19 : comparaison avec les équations

Les modèles à équations représentent les variations globales de populations et leur interdépendance. Ils ne décrivent pas explicitement chaque individu et chaque interaction. Leurs nombreux paramètres peuvent être difficiles à comprendre ou manipuler.

Les MABS mettent les entités et leurs interactions au premier plan, ce qui facilite l'étude des comportements individuels. L'émergence du phénomène global reste parfois difficile à anticiper et les paramètres peuvent aussi être nombreux.

## Diapo 13, pages 20 et 21 : proies-prédateurs en MABS

Les proies peuvent se déplacer, se reproduire, fuir et mourir, éventuellement manger. Les prédateurs peuvent se déplacer, se reproduire, chasser et manger, puis mourir. L'environnement est une grille spatiale, éventuellement complétée par la croissance de l'herbe.

La page 21 révèle la difficulté principale : trouver les paramètres reproduisant le phénomène global attendu, appelé « fait stylisé ». Les comportements locaux seuls ne garantissent donc pas une dynamique globale donnée.

## Diapo 14, page 22 : conception incrémentale

Le prof demande de réutiliser la méthode de conception MAS et de travailler progressivement. Pour les agents : lister les entités actives, identifier les actions, choisir la granularité, définir les interactions et, si nécessaire, l'organisation.

Pour l'environnement : inventorier les ressources partagées, y compris l'espace, se demander s'il est discret, dynamique ou ouvert, puis traiter la question technique de la synchronisation.

## Diapo 15, page 23 : quatre aspects de conception

Les quatre aspects sont le comportement (délibération des agents), l'environnement (objets et dynamique physiques), l'ordonnancement (évolution du temps et entrelacement des activations), et l'interaction (résultat des actions).

Le schéma attribué à W. Ouerdane précise que l'ordonnancement contrôle les comportements, l'environnement et les interactions. Les comportements et l'environnement génèrent les interactions. Le lien entre comportement et environnement définit les conditions de perception et d'action.

## Diapo 16, page 24 : transition

Cette page introduit la partie Mesa.

## Diapo 17, page 25 : plateforme Mesa

Le cours présente Mesa comme une plateforme Python de systèmes multi-agents orientée simulation. Elle fournit des composants pour la grille, l'activation et la gestion des graines aléatoires. L'API Python permet d'utiliser les outils d'analyse de données de cet écosystème. La visualisation web rappelle NetLogo. Le prof souligne le développement très actif et renvoie à [la documentation Mesa](https://mesa.readthedocs.io/).

## Diapo 18, page 26 : composants

Les agents héritent de `mesa.Agent`. L'environnement général est porté par `mesa.Model`. Le runtime associe `AgentSet` et `Model`. Les classes spatiales appartiennent au module présenté comme `mesa.discretespace` dans cette diapositive. Le nom documenté et utilisé ailleurs dans le cours est `mesa.discrete_space`.

Le dessin relie `Model`, `Grid`, `Random`, `AgentSet`, `Agent`, `Cell` et `CellAgent`. `CellAgent` hérite d'`Agent` et représente un agent situé dans une cellule. Le modèle organise les agents, l'espace et l'aléatoire.

## Diapo 19, page 27 : modèle et exécution

Le modèle hérite de `mesa.Model`. Son constructeur initialise la classe parente avec une graine, montrée sous la forme `super().__init__(seed=None)`. Il crée les agents avec `SomeAgentClass.create_agents(model=self, n=...)`.

Sa méthode `step()` active les agents avec `self.agents.shuffle_do("procedural_loop")`. On instancie ensuite le modèle et on exécute `model.run_for(number_of_turns)`. Les noms d'agent et les points de suspension sont des éléments de présentation, à remplacer dans une application.

## Diapo 20, page 28 : agent et boucle procédurale

L'agent hérite de `mesa.Agent`, reçoit le modèle au constructeur et appelle `super().__init__(model)`. Sa boucle procédurale s'appelle généralement `step` et ne reçoit pas d'autres paramètres. Le prof indique trois étapes : percevoir, délibérer, agir.

## Diapo 21, page 29 : exemple minimal

Le programme importe Mesa, crée `MyAgent` dont `step()` affiche `hello world`, puis `MyModel` qui crée `n_agents` agents et les active avec `shuffle_do("step")`. L'exemple instancie cinq agents et lance `run_for(1)`.

Il illustre le fonctionnement de base de la plateforme. Le simple affichage ne constitue pas un modèle complet d'un phénomène.

## Diapo 22, page 30 : encapsulation

Python n'impose pas les restrictions d'accès des langages à modificateurs public/privé. Un agent peut donc lire une variable interne d'un autre agent. Le prof qualifie cette pratique de mauvaise.

L'exemple choisit un autre agent et récupère sa variable `my_secret_variable`. Le code visible contient aussi une coquille : il construit `others`, puis appelle `choice(cellmates)`. Le message pédagogique porte sur l'accès indu à un état interne, pas sur une recette à exécuter.

## Diapo 23, page 31 : boucle mal structurée

Mesa autorise n'importe quel contenu dans `step()` sans imposer la séparation perception, délibération, action. Le prof critique une somme sur les variables des autres agents suivie d'appels à deux méthodes agissant sur le système.

Les défauts explicitement indiqués sont une perception cachée, une complexité quadratique et deux actions en un tour. Une recherche globale de coût O(N), répétée par N agents, conduit à O(N²). Le snippet présente aussi `self.model.schedule.agents`, une écriture à replacer dans le contexte des anciennes API, et utilise `x` après une affectation à `self.x`.

## Diapo 24, page 32 : boucle recommandée

Le prof recommande cette organisation :

```python
def step(self):
    self.perceive()          # Met à jour l'état interne.
    action = self.decide()   # Sélectionne une action.
    self.act(action)        # Exécute cette action.
```

Les méthodes doivent être définies pour le modèle choisi. Ce fragment est une structure de conception, pas une classe complète exécutable.

## Diapo 25, page 33 : exécution synchrone

Une activation longue bloque les autres agents pendant l'exécution de `step()`. Le prof recommande d'éviter les calculs longs dans la boucle procédurale. Si nécessaire, il propose des appels externes à un thread, de préférence gérés dans l'environnement.

Il faut distinguer cette exécution séquentielle des règles d'observation du temps simulé : des agents exécutés successivement peuvent voir des états déjà modifiés par les agents précédents.

## Diapo 26, page 34 : communication

Le cours indique l'absence d'un mécanisme de communication directe fourni dans la présentation de Mesa. Les communications passent par les variables de l'environnement, donc le modèle.

## Diapo 27, page 35 : transport de messages personnalisé

Le prof montre qu'un mécanisme peut être ajouté. Une classe `Message` contient un performatif et un contenu, avec les constantes `REQUEST = 1`, `REQUEST_DO = 2`, `INFORM = 3`. Un `MessageReceiver`, héritant de `mesa.discrete_space.CellAgent`, possède une liste `messages`.

Sa méthode `notify(message, sender)` ajoute le couple message et émetteur. L'agent lit les messages pendant `perceive()`, par exemple avec `read_messages()`. Cette dernière méthode reste à écrire. Le support ne définit pas le délai de livraison, la suppression des messages lus ni la gestion des conflits.

## Diapo 28, page 36 : transition vers le TP

La page annonce les travaux pratiques.

## Diapo 29, page 37 : bases de Mesa

Le prof demande d'ouvrir `session4_notebook.ipynb`. Le TP s'appuie sur les tutoriels de premier modèle, d'ajout de l'espace et de collecte de données. Le programme peut s'exécuter en local ou sur Colab. Pour une installation locale, le prof exige un environnement virtuel.

Le modèle monétaire est une simulation simple de l'émergence d'inégalités dans la société, selon le principe KISS. Les règles précises du notebook ne sont pas accessibles dans le dossier fourni. Les liens actuels vers les tutoriels sont regroupés dans [les sources](07_sources.md).

## Diapo 30, page 38 : principes de visualisation

Il faut définir la représentation visuelle des agents, définir les paramètres du modèle (taille de grille et curseurs), puis instancier le renderer. Le prof indique que la visualisation présentée ne fonctionne pas sur Google Colab et demande une installation locale, dans Jupyter ou de préférence en programme autonome.

## Diapo 31, page 39 : représentation des agents

Une fonction `agent_portrayal(agent)` retourne un `AgentPortrayalStyle`. Dans l'exemple, les agents sont des points orange de taille 50. Ceux dont `wealth > 0` deviennent bleus et de taille 100.

Le prof propose `marker="^"` pour changer la forme, `alpha=0.8` pour la transparence et `zorder=2` pour gérer l'ordre visuel des superpositions. Cette lecture de `wealth` sert au rendu par l'observateur. Elle ne donne pas automatiquement à chaque agent le droit d'utiliser la richesse de tous les autres pour décider.

## Diapo 32, page 40 : renderer de grille

Le code crée `MoneyModel(n=50, width=10, height=10)`, importe `SpaceRenderer` et configure un rendu `matplotlib` avec `.setup_agents(agent_portrayal).render()`. Le renderer représente l'espace du modèle.

## Diapo 33, page 41 : paramètres

Le dictionnaire `model_params` contient `n`, `width` et `height`. Le nombre d'agents utilise un `SliderInt`, initialisé à 50, de minimum 10, maximum 100 et pas 1. Les dimensions de la grille valent 10 chacune.

Le support indique que cela permet de changer le modèle à l'exécution. Il ne détaille pas quels changements nécessitent une réinitialisation.

## Diapo 34, page 42 : serveur Solara

Solara est présenté comme la méthode de visualisation Mesa par défaut. Après définition du modèle, du portrayal, des paramètres et du renderer, on construit `page = SolaraViz(mm, renderer, model_params=model_params, name="Boltzmann Wealth Model")`.

La commande de lancement est `solara run this_file.py`. Le support écrit aussi `rederer` à un endroit, une coquille à corriger en `renderer` dans un programme réel.

## Diapo 35, page 43 : interface pygame locale

L'alternative est une solution de l'Université Paris-Saclay attribuée à Niccolo Angeli (2026), dans [Erocr/mesa_graphics](https://github.com/Erocr/mesa_graphics). Le support l'annonce comme limitée à Windows, en raison d'un bug de `pygame.font` sous Linux.

Les instructions sont de récupérer le dossier `mesa_graphics`, installer pygame et lancer un fichier Python normal. `MesaGraphics` reçoit le modèle, le renderer, les paramètres et le nom d'affichage, comme dans l'exemple Solara. Le statut actuel de ce dépôt n'a pas pu être vérifié lors de cette préparation.

## Diapo 36, pages 44 et 45 : graphiques dynamiques

Les courbes s'appuient sur les données collectées. Pour Mesa, `make_plot_component` vient de `mesa.visualization`. Pour l'interface locale, les imports proviennent de `mesa_graphics`, avec `FigureMatplotlib` et `matplotlib.figure.Figure`.

La page 45 ajoute un exemple de coefficient de Gini dans le temps : `GiniPlot = make_plot_component("Gini")`, puis `components=[GiniPlot]` dans la visualisation choisie. La notation `SolaraViz/MesaGraphics` dans le support désigne deux alternatives et ne constitue pas une expression Python à recopier.

## Diapo 37, page 46 : histogramme des richesses

La fonction `Histogram(model)` crée `fig = Figure()`, obtient `ax = fig.subplots()`, collecte les `agent.wealth`, puis exécute `ax.hist(wealth_vals, bins=10)`. Elle retourne `FigureMatplotlib(fig)` pour l'interface locale.

Le composant est ajouté à `MesaGraphics` par `components=[(Histogram, 2)]`, afin de l'afficher dans l'onglet 2. Le prof insiste sur l'API objet Matplotlib plutôt que sur `plt.figure()` et `plt.hist()`, pour les questions de threads. Le guide technique précise la limite de cette recommandation : l'API objet ne rend pas à elle seule Matplotlib sûre en concurrence.

## Diapo 38, page 47 : séance suivante

Le support annonce une séance pratique MABS avec Mesa ou JADE. Il ne fournit pas lui-même le sujet ou le barème. La [session 5](08_projet_session5.md), ajoutée au dossier le 19 octobre 2026, précise désormais le projet de taxis partagés, les livrables et l'évaluation.
