# Décisions techniques de l'implémentation

Ces conventions ont été choisies dans le cadre de l'autorisation donnée dans
la conversation. Elles ne sont pas attribuées rétroactivement aux décisions U01-U71.
Les anciennes règles et les descriptions du programme historique ne sont pas
réintroduites. Aucun programme historique n'était présent dans ce dossier.

## Bibliothèque et architecture

Mesa 3.3.1 est fixé explicitement, avec Python 3.12 testé et Matplotlib 3.10.8.
Les composants utilisés sont `Model`, `Agent`, `AgentSet.do`, `MultiGrid` non
torique et `DataCollector`. L'API installée a été inspectée et exercée par les tests.

`MultiGrid` répond à la recommandation du professeur et autorise plusieurs
agents dans une cellule. Il demeure disponible dans cette version 3.x.
Une migration vers Mesa 4 demanderait une revue explicite de cette API.
L'interface web de Mesa n'est pas retenue, car la cible exige une interface
locale. Tkinter et l'API objet Matplotlib respectent ce choix.

Les protocoles de messages, la génération de routes et l'insertion contrainte
sont spécifiques au métier. Mesa fournit la structure multi-agents, l'espace,
l'activation et la collecte ; ces politiques sont donc implémentées séparément.
La comparaison, initialement reportée dans le cahier, est désormais autorisée
par l'utilisateur : un script minimal réutilise ce moteur, sans double monde
dans l'interface. Les deux capacités sont exécutées successivement.

Références techniques consultées :

- [Vue d'ensemble Mesa](https://mesa.readthedocs.io/stable/overview.html)
- [API Mesa](https://mesa.readthedocs.io/stable/mesa.html)
- [DataCollector](https://mesa.readthedocs.io/stable/apis/datacollection.html)

La documentation en ligne évolue ; les dépendances fixées et le code installé
sont les références exécutables de ce projet.

## Temps et états

`tick` est un entier et `time_seconds = tick * 0.2`.
Le compteur `steps` propre à Mesa compte les appels à `step()` et n'est pas
utilisé comme horloge physique. Une dernière activation peut finaliser la
descente à la frontière courante sans faire avancer un nouvel intervalle.

L'ordre explicite est : finalisations, apparitions, offres, choix, confirmations,
clôtures, démarrages physiques, instantané de circulation, progression de 0,2 s.
Les notifications sont consommées dans la phase à laquelle elles se rapportent.
Aucune pause réelle ne représente une durée simulée. Il n'y a pas de thread
par agent ni de délai de négociation ajouté.

La carte Mesa positionne un taxi sur l'origine de la portion jusqu'à sa fin.
L'action `Move` conserve le point d'arrivée et la progression continue ; le
rendu interpole sa position. La finalisation déplace l'agent dans `MultiGrid`.
L'orientation affichée à l'arrêt reste celle de l'arrivée précédente. Pendant
le mouvement, le triangle suit la direction de `Move`. Le planificateur utilise
la cellule d'arrivée future, sans interrompre la portion déjà engagée.

Un passager futur n'est pas sur la grille. Il apparaît à son accès, quitte la
grille au début de montée et réapparaît à destination à la fin de descente.
Il reste agent Mesa pendant tout ce cycle. Un voyage correspond toujours à un taxi.

## Routage, accès et départages

Les coordonnées sont des couples entiers `(x, y)`, avec `(0, 0)` en bas à gauche.
Une orientation est un vecteur cardinal d'arrivée `(dx, dy)`, conservé pour
l'affichage et les mouvements physiques. Le routage utilise uniquement les
cellules. Les demi-tours sont autorisés à toute frontière de cellule routière,
y compris après un arrêt et aux intersections, sans temps de manoeuvre ajouté.
Une portion ou une opération déjà engagée reste verrouillée jusqu'à sa fin.

`City.path_to` retourne un seul plus court chemin déterministe, sans inclure la
cellule de départ. Il retourne un tuple vide pour un arrêt sur place, `None`
pour une destination routière inaccessible et une erreur pour une cellule
hors réseau. La recherche en largeur conserve un arbre par cellule de départ,
réutilisé pour toutes les destinations, puis met les chemins en cache.

D0 est la distance du plus court chemin entre les accès, fixée une fois par
voyage. Sur le réseau actuel, elle est identique à l'ancienne référence utilisant
la meilleure orientation de départ. Le budget reste min(25 % de D0, 400 m),
avec les paramètres configurables existants.

L'ordre stable des voisins est nord, est, sud, ouest. Les chemins de même
longueur sont ainsi reproductibles. Entre programmes admissibles, le taxi
minimise d'abord sa distance restante totale (équivalente à minimiser l'ajout,
le programme précédent étant commun à toutes les insertions), puis utilise
l'ordre lexicographique des identifiants d'arrêts et des chemins.
Les accès fixes de bâtiments sont choisis par minimum lexicographique `(x, y)`.

`City.validate_accessibility` vérifie la connexité du réseau bidirectionnel,
l'existence d'un voisin pour chaque cellule et l'appartenance des accès au
réseau. Une impasse permet désormais de repartir dans le sens opposé. Le cadre
et les axes complets restent la géométrie du générateur ; ils ne sont pas retirés.

Pour chaque insertion, `_route` parcourt une seule séquence de plus courts
chemins. Avec des demi-tours libres, la direction d'arrivée n'influence plus
l'étape suivante. Les distances, temps estimés et contraintes sont des coûts
positifs ou des plafonds : allonger une étape ne peut améliorer une ressource.
`Label`, `_visit` et `_prune` sont supprimés. Les comptes individuels, les
approches promises, la capacité et les bornes de revalidation restent vérifiés.
La recherche des positions d'insertion et l'ordre relatif des anciens arrêts
restent inchangés. Cette simplification repose sur l'estimation à vitesse libre,
sans coût de virage, fenêtre horaire minimale ni évitement de congestion.

## Engagements et revalidation

Les objets échangés sont immuables : `Trip`, `Stop`, `Leg`, `Plan`, `Offer`.
Les identifiants applicatifs de taxi et passager sont sauvegardés dans le
scénario ; ils sont indépendants de l'identifiant interne de Mesa.
Une offre est identifiée par `(passenger_id, taxi_id, round_id)`.

Chaque taxi possède son dictionnaire de demandes connues, ses offres et ses
engagements. Chaque client possède sa propre boîte de réception et choisit ses
offres. Les observateurs peuvent lire les agents pour les métriques et les
assertions ; ces lectures ne participent pas aux décisions des agents.

La revalidation peut rechercher une insertion compatible avec des engagements
confirmés plus tôt dans la même ronde, mais ne peut dégrader aucun des éléments
annoncés : distance d'approche, début de montée estimé, distance à bord du candidat
et score de budget. Sinon, elle refuse, sans seconde ronde au même instant.
Ce choix conservateur applique la clarification « ne pas modifier silencieusement
l'offre acceptée ». Il n'entraîne pas le refus automatique de toutes les autres
acceptations : plusieurs peuvent rester compatibles.

L'estimation annoncée n'est pas une garantie temporelle permanente. Après la
confirmation, les protections du cahier sont spatiales. Des opérations futures
ou la congestion peuvent donc augmenter l'attente réelle.

Une montée commencée possède déjà sa place ; une descente commencée la conserve
jusqu'à sa fin. Le planificateur projette la fin de l'opération verrouillée avant
de réorganiser la suite. Le temps restant est inclus dans l'estimation. Les
arrêts retirés de la liste au début d'une opération restent représentés par
l'action en cours. Les nouveaux engagements ne la redémarrent pas.

## Aléatoire et scénario

La graine par défaut choisie pour cette version est 2026. Les quatre graines
de flux sont dérivées par SHA-256 de `taxishare-v1:<graine>:<nom>` avec les noms
`map`, `fleet`, `trips`, `times`, puis utilisées par quatre `random.Random`.
Le hasard n'intervient pas dans les décisions, le mouvement ou le rendu.

Les combinaisons d'axes admissibles sont tirées uniformément par une transformation
qui retire les espacements imposés, puis les réintroduit. Les bâtiments sont
tirés sans remise. Les destinations sont préparées par origine pour exclure
les accès identiques sans boucle de rejet. Les horaires sont des entiers inclusifs.

Le JSON exporté est versionné (`schema_version = 1`) et conserve toutes les
entrées pour la traçabilité. À la demande de l'utilisateur, le chargement de
scénarios depuis un fichier est retiré de l'interface, de la ligne de commande
et de `Scenario`. Le rejeu reconstruit le modèle depuis le scénario courant
en mémoire. Une génération identique nécessite les mêmes paramètres, la même
graine et la même version du générateur ; une graine seule ne suffit pas après
une modification du code. `--config` conserve la lecture des paramètres de
génération uniquement, sans importer une carte ni des voyages sauvegardés.

## Calcul numérique, congestion et plafond

Les distances utilisent des flottants double précision. La tolérance de
comparaison vaut `1e-7 m`, très inférieure à toute portion du réseau, et ne
constitue pas une marge de détour. Les clés de classement sont stabilisées à
sept décimales. Aucun budget n'est arrondi à la portion supérieure.

Pour chaque taxi circulant pendant un intervalle :

1. Distance avancée = minimum du reste de portion et de `v * 0.2`.
2. Temps physique utilisé = distance avancée / vitesse congestionnée.
3. Retard de congestion = temps physique utilisé - distance / vitesse libre.
4. Quantification = 0,2 s - temps physique utilisé.

Le résidu final ne permet pas de commencer la portion suivante avant la prochaine
frontière. L'identité vérifiée est : temps de circulation = distance / vitesse
libre + retard de congestion + quantification. Les opérations sont mesurées
séparément. Les retards agrégés sont des véhicule.secondes, pas des moyennes clients.

Le plafond initial choisi est 7 200 s simulées, configurable. Il ne prolonge
pas les voyages artificiellement et ne garantit pas leur réussite. Le scénario
par défaut finit bien avant ; une configuration différente peut être incomplète.

## Observation, exports et portée

`DataCollector` observe chaque frontière effectivement traitée, après les phases
logiques et avant l'intervalle suivant ; une observation finale conserve l'état
terminal. Pendant une pause après un intervalle, la dernière ligne historique
peut donc précéder l'horloge courante de 0,2 s. Les résumés d'export lisent l'état
physique courant. Les fins d'action dues sont finalisées au prochain appel.

Les historiques détaillés de messages sont optionnels ; les compteurs sont
toujours conservés. Les charges instantanées ne sont pas exportées intégralement
à chaque pas : les indicateurs de congestion et de quantification le sont.
Le diagnostic d'absence d'offre est une catégorie globale de contraintes,
pas une preuve d'impossibilité pour toutes les politiques.

La provenance contient les empreintes de chaque fichier Python, des documents
source disponibles et les versions des principales bibliothèques. L'empreinte
du scénario utilise une sérialisation JSON canonique distincte.

L'insertion demeure une politique locale, sans optimum global garanti. Son coût
augmente avec le nombre d'engagements et d'insertions possibles. Aucun plafond
silencieux du nombre d'engagements ou des solutions n'est ajouté pour accélérer.
L'occupation moyenne et le taux de clients ayant partagé ne sont pas ajoutés :
la mesure retenue est la distance de taxi parcourue avec au moins deux personnes.

## Interface simplifiée et comparaisons minimales, 30 octobre 2026

Le formulaire est limité aux taxis, demandes, fenêtre d'apparition, capacité et
graine. Les autres valeurs de `Config` sont préservées lors de la génération ;
elles restent accessibles dans le code et en ligne de commande. Carte, graphiques,
rejeu en mémoire et export sont conservés. Le chargement de scénarios reste retiré.

`run_experiments.py` génère une seule fois par graine, puis construit deux
scénarios dont seule la capacité diffère : un et trois passagers. Les empreintes
complètes des scénarios diffèrent donc aussi, puisque la configuration est incluse.
Les axes, bâtiments, positions et orientations initiales, voyages et horaires
sont identiques dans chaque paire. Cinq graines fixées à l'avance sont utilisées
par défaut, de 2026 à 2030, sans sélection sur les résultats.

Les effectifs et statuts permettent de vérifier le service rendu. Seules distance
totale, attente moyenne, temps total moyen et fraction de distance partagée sont
agrégés. Les différences sont calculées par graine avant moyenne et écart-type
d'échantillon. Les paires incomplètes sont exclues ; chaque mesure conserve son
effectif utilisable et les valeurs inconnues restent absentes. Aucune nouvelle
mesure de satisfaction, de congestion ou d'émissions n'est ajoutée.

## Demi-tours et simplification du routage, 30 octobre 2026

L'utilisateur autorise la seconde approche après analyse du code : remplacer
le routage orienté et les alternatives du planificateur par un routage entre
cellules. Cette décision remplace l'interdiction U46 et la partie orientée du
contrôle U67 ; elle simplifie U49 sans changer D0 sur les cartes actuelles.

La congestion reste calculée par portion dirigée dans `traffic_snapshot` :
A vers B et B vers A ont des charges et vitesses indépendantes. Autoriser un
demi-tour n'efface aucune distance déjà parcourue et ne change pas le sens
d'une action `Move` en cours. Les offres continuent à estimer les temps à
vitesse libre ; la congestion s'applique à l'exécution physique.

Les orientations initiales et leur tirage sont conservés pour les triangles,
le format du scénario et les mêmes entrées aléatoires. Aucun changement du
générateur ni du schéma JSON n'est nécessaire. L'empreinte du scénario seule
ne distingue donc pas les deux règles ; les empreintes du code dans
`provenance.json` identifient le moteur utilisé.

Le commit local `d488533` conserve l'état avant cette migration. Le routage et
le planificateur sont plus simples ; aucun facteur d'accélération n'est affirmé.
Les résultats sans demi-tour restent historiques. Les nouvelles comparaisons
utilisent `output/comparison-uturns/` pour préserver `output/comparison/`.
