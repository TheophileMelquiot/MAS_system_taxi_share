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
L'infrastructure d'expériences comparatives reste reportée conformément au cahier.

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
L'orientation logique reste celle de l'arrivée précédente tant que la portion
en cours n'est pas terminée. Le planificateur utilise son orientation d'arrivée
future, sans interrompre cette portion.

Un passager futur n'est pas sur la grille. Il apparaît à son accès, quitte la
grille au début de montée et réapparaît à destination à la fin de descente.
Il reste agent Mesa pendant tout ce cycle. Un voyage correspond toujours à un taxi.

## Routage, accès et départages

Les coordonnées sont des couples entiers `(x, y)`, avec `(0, 0)` en bas à gauche.
Une orientation est un vecteur cardinal d'arrivée `(dx, dy)`.
Un état routier est `(cellule, orientation)` ; la direction opposée est interdite.
Aux coins, le virage à 90 degrés est une transition normale.

La recherche en largeur trouve les plus courts chemins en nombre de portions.
Pour chaque arrêt, elle conserve un chemin par orientation d'arrivée atteignable.
Les orientations sont combinées au fil du programme, sans réinitialisation aux
arrêts. Un chemin d'approche plus long peut rendre le trajet à bord admissible.
Les chemins plus longs ayant les mêmes états de départ et d'arrivée ne sont
pas explorés : ils n'améliorent ni la distance, ni les contraintes cumulatives.

L'ordre stable des voisins est nord, est, sud, ouest. Les chemins de même
longueur sont ainsi reproductibles. Entre programmes admissibles, le taxi
minimise d'abord sa distance restante totale (équivalente à minimiser l'ajout,
le programme précédent étant commun à toutes les insertions), puis utilise
l'ordre lexicographique des identifiants d'arrêts et des chemins.
Les accès fixes de bâtiments sont choisis par minimum lexicographique `(x, y)`.

La validation inverse du graphe vérifie que chaque état légal peut atteindre
chaque accès et dispose d'une continuation. Il n'est pas exigé d'atteindre
toutes les orientations possibles d'un accès.

Le planificateur conserve plusieurs états de recherche si leurs distances
individuelles diffèrent. Éliminer un état uniquement parce que sa distance
totale est plus longue pourrait perdre une solution protégeant un passager.
Seuls les états ayant les mêmes ressources sont fusionnés.

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

Le JSON est versionné (`schema_version = 1`). Les anciens formats sont refusés
avec un diagnostic, faute d'ancien scénario fourni à migrer. Le scénario complet,
et non la graine seule, est la référence de rejeu.

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
augmente avec le nombre d'engagements et d'orientations possibles. Aucun plafond
silencieux du nombre d'engagements ou des solutions n'est ajouté pour accélérer.
L'occupation moyenne et le taux de clients ayant partagé ne sont pas ajoutés :
la mesure retenue est la distance de taxi parcourue avec au moins deux personnes.
