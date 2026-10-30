# Guide technique historique du projet Mesa

> Statut lors de l’import du 30 octobre 2026 : ce guide décrit une ancienne version (Mesa 3.0.3, pas de 1 s et carte 11 × 9). Le code actuel utilise Mesa 3.3.1, un pas de 0,2 s et une carte générée 21 × 21 par défaut. Les commandes et règles à appliquer sont dans le [README](../README.md) et les [décisions techniques](technical-decisions.md). Les paragraphes ci-dessous sont conservés pour leur valeur historique.

Mise à jour documentaire : 27 octobre 2026. Ce guide synthétise les choix consignés dans le registre et les dépendances de référence. Il ne constitue pas une nouvelle vérification d'exécution.

## Environnement retenu

Le projet référence Python 3.10 ou supérieur, Mesa 3.0.3 et Matplotlib 3.10.8. Les paquets sont figés dans [requirements.txt](../requirements.txt). L'énoncé n'impose aucune version précise de Mesa.

Depuis la racine du projet, installation sur un nouvel ordinateur :

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

L'interface utilise Tkinter et Matplotlib. Voir le [README](../README.md) pour le lancement, les exports et les comparaisons automatiques. Les exemples Mesa récents peuvent viser une autre version : vérifier leur compatibilité avant de les reprendre. Une migration vers une autre version ou vers Solara n'est pas requise par le professeur.

## Mesa et responsabilités

- `Passenger` et `Taxi` sont les deux types d'agents.
- `MultiGrid` non torique contient les taxis et les passagers en attente ou réservés, sur une carte 11 × 9.
- Les services de carte, demande, messagerie, circulation et mesures répartissent les responsabilités. Ils ne sont pas tous des agents.
- Le modèle coordonne les phases et conserve l'horloge en secondes.
- Le rendu observe les états sans modifier les décisions ou les tirages.

Ces éléments correspondent aux choix L03, L04 et L17 du [registre](10_decisions_et_reprise_llm.md). Le professeur recommande MultiGrid, exige CFP et réponses et demande une visualisation. La géométrie, Tkinter et l'organisation des modules sont des choix du projet.

## Temps et communication

La résolution est une seconde. Les messages CFP, OFFER, ACCEPT, CONFIRM et REJECT sont traités par phases à temps simulé constant. Une offre ne réserve pas de place ; le taxi revalide lors de l'acceptation. Après refus, une nouvelle demande peut être émise la seconde suivante.

Les déplacements utilisent un instantané commun des charges par portion dirigée. Les embarquements et descentes ont des durées explicites. Le [modèle documenté](09_modele_implemente.md) centralise les conventions et les définitions des mesures.

## Vérifications avant remise

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe run_experiments.py
```

Contrôler aussi le lancement de l'interface et le rejeu d'un scénario JSON. Ces commandes sont des instructions, pas des résultats de vérification de cette mise à jour.

## Historique et sources

L'[ancien guide](archives/03_guide_mesa.md) conserve les propositions initiales : Mesa 3.5.1, Solara, grille 4 × 4 et messages au tour suivant. Elles ne décrivent pas la version retenue. Les consultations techniques historiques restent datées dans [les sources](07_sources.md). Aucune consultation en ligne n'a été renouvelée pour ce nettoyage.


## Priorité aux outils Mesa, décision U16

Pour chaque évolution, examiner d'abord les outils de la version Mesa retenue : espace, agents et activation, aléatoire, collecte, expériences et visualisation. Employer une solution Mesa si elle satisfait le besoin simplement ; documenter la raison de tout autre choix. Cette revue reste à faire et n'implique pas qu'une fonctionnalité existe dans la version installée.

La présence d'un composant personnalisé dans la version actuelle ne suffit pas à justifier son maintien. Inversement, remplacer automatiquement le contrat temporel ou la messagerie par un outil inadéquat ne répondrait pas à l'objectif. Vérifier compatibilité, sémantique et simplicité avant de décider.

U15 vise aussi une génération automatique simple de la carte. La piste L20 est décrite dans le registre ; aucun générateur de carte n'a été ajouté ici.


## Organisation des comportements, décision U17

L'environnement reste global et cohérent ; éviter de le fragmenter artificiellement. Décomposer surtout les comportements des agents en responsabilités courtes et lisibles. Un bloc ou une méthode dédiée n'implique pas un agent, un service ou une phase temporelle supplémentaire. Examiner les outils Mesa conformément à U16 avant de choisir un mécanisme d'organisation des comportements. Aucun changement d'API ou de contrat temporel n'est décidé par cette consigne.


## Commentaires et structure, décision U18

Chaque évolution doit conserver une structure claire et des commentaires expliquant la logique des parties concernées. Tous les commentaires et docstrings doivent être en anglais, ainsi que les noms des fonctions, méthodes, classes, variables, paramètres, attributs, constantes et modules définis dans le code. Documenter les étapes, hypothèses et raisons des choix, avec des docstrings pour les contrats utiles et des commentaires pour la logique locale. Mettre à jour les commentaires et docstrings affectés dans le même changement que le code, en vérifiant aussi les références situées ailleurs. Une modification n'est pas terminée si ses explications ne correspondent plus au fonctionnement réel.


## Configuration et règles fixes, décision U19

Éviter les coordonnées, seuils et cas particuliers dispersés dans les comportements. Centraliser les paramètres, unités et valeurs par défaut ; valider les entrées et conserver la configuration dans le scénario. Concevoir transport et affichage pour utiliser la géométrie fournie. Les cartes fixes peuvent servir de cas de démonstration ou de vérification ; elles ne doivent pas imposer leur géométrie à toute la logique. Garder les invariants explicites et justifier les règles fixes plutôt que créer un moteur de règles générique sans nécessité.


## Adapter ou réécrire, décision U20

Avant une modification importante, comparer une adaptation locale à un remplacement propre de la partie concernée. Privilégier le remplacement si l'adaptation devient plus coûteuse, plus fragile ou moins lisible. Éviter l'empilement de rustines et les anciennes branches maintenues sans besoin. Synchroniser commentaires et documentation, et distinguer conservation du comportement et changement fonctionnel voulu. Ce principe n'impose pas une réécriture totale à chaque évolution.


## Simulation unique et états individuels, U21 et U22

La priorité de développement est un seul modèle simulé. L'interface actuelle à deux modèles n'est pas l'architecture cible à conserver par obligation ; les modes de comparaison seront traités plus tard.

Représenter les opérations longues par des états et délais propres aux taxis, sans bloquer la boucle commune ni imposer l'attente à toute la flotte. Une activation commune permet des actions individuelles différentes. Ne pas introduire un thread par taxi pour satisfaire cette exigence. Vérifier un cas où un taxi embarque pendant qu'un autre se déplace et qu'un troisième est disponible.
