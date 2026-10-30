# Décisions du projet et base de reprise pour les LLM

## Actualisation utilisateur du 30 octobre 2026 : demi-tours autorisés

L'utilisateur demande de sauvegarder l'état actuel par commit et push, puis
d'implémenter la seconde approche analysée : routage entre cellules et
suppression des alternatives d'orientation du planificateur. Il confirme que
les embouteillages doivent rester distincts pour les deux sens de circulation.
Les demi-tours sont autorisés aux frontières de cellules routières, sans durée
de manoeuvre ajoutée ; une portion ou opération engagée doit être terminée.

Cette décision remplace U46 et la partie orientée de U67. D0 devient simplement
la distance du plus court chemin entre accès, identique à l'ancienne référence
sur les cartes actuelles. Budgets cumulés, approches promises, capacité et
revalidation des offres restent conservés. Les orientations initiales restent
sauvegardées pour l'affichage et la reproductibilité des entrées.

Le commit `d488533` conserve l’état avant modification et `af2f1dc` la
migration du routage. Les deux ont depuis été poussés sur `origin/yanis` ;
le refus 403 initial a été résolu. Les commits `3dc2f38` et `b635c8f`
ajoutent ensuite les explications, la grille visible et les légendes. Les résultats sans demi-tour sont historiques ; les nouveaux
exports sont séparés dans `output/comparison-uturns/` (copie des tableaux dans [results/capacity-comparison](results/capacity-comparison/README.md)).
Les [décisions techniques](technical-decisions.md)
et la [validation](validation.md) du dépôt actif
font référence pour l'implémentation et ses vérifications.

Les sections plus anciennes ci-dessous conservent leur statut historique.


**Version documentaire : 5.2. Dernière mise à jour documentaire : 28 octobre 2026. La présente clarification ne comprend aucune nouvelle relecture ni exécution du code.**

**Actualisation U69 à U71 :** adapter l'interface locale existante à une simulation unique ; conserver un plafond de durée simulée configurable en complément du contrôle d'état figé, avec arrêt incomplet s'il est dépassé ; mesurer distances et activité sans modèle d'émissions ni conversion en CO2. La valeur numérique du plafond sera ajustée après les premiers essais. Les conventions techniques proposées dans le dernier échange ne sont pas de nouvelles décisions utilisateur. La synthèse courante et l'index sont consolidés ; l'historique reste dans ce registre.

**Actualisation U68 :** distance partagée mesurée en mètres de taxi, chaque mètre compté une seule fois. Conserver les distances à zéro, un, deux, trois et quatre passagers selon la capacité configurée, avec des noms distincts de la référence personnelle D0 de U49. Distance partagée = somme des distances à au moins deux passagers ; distances à vide et à un passager conservées, par taxi et pour la flotte.

**Actualisation U67 :** valider toute la carte orientée avant lancement : depuis chaque position et orientation légales du réseau, tous les accès doivent être atteignables, avec possibilité de poursuivre légalement après arrêt. Refuser une carte ne satisfaisant pas cette garantie avec diagnostic. Ce contrôle porte sur la circulation et ne garantit pas l'admissibilité de chaque course au regard du budget de détour.

**Actualisation U66 :** conserver résumé global et détails individuels, une ligne par client et par taxi. Attente jusqu'au début de montée, temps à bord entre fin de montée et début de descente, opérations propres séparées, temps total jusqu'à fin de descente. Dates inconnues absentes ; moyennes de voyages terminés sur les clients livrés avec effectif affiché et non-livrés recensés séparément.

**Actualisation U65 :** arrêt technique incomplet si toutes les demandes sont apparues, tous les taxis sont libres et garés, des clients attendent et une évaluation complète ne produit aucune offre admissible. Conserver clients non servis et diagnostic ; ne pas confondre cet état figé avec une attente temporaire, un abandon ou une réussite. Aucune règle métier assouplie pour forcer la livraison.

**Actualisation U64 :** quatre suites pseudo-aléatoires séparées, dérivées de manière stable d'une graine principale : carte et bâtiments, flotte, voyages, horaires. Ne pas ajouter de tirages pendant les déplacements ou négociations. Le scénario complet sauvegardé reste la référence du rejeu ; une graine seule ne garantit pas le même scénario après changement du générateur.

**Actualisation U63 :** positions initiales des taxis tirées uniformément sans remise parmi les cellules routières hors carrefours, cadre compris. Taxis initialement libres, sans passager ni réservation, garés hors du flux. Tirer ensuite leurs orientations légales selon U48 et sauvegarder le tout, sans utiliser les demandes futures pour favoriser le placement.

**Actualisation U62 :** pour chaque demande, origine uniforme parmi les bâtiments, puis destination uniforme parmi ceux dont l'accès diffère. Tirages indépendants entre demandes et indépendants des horaires ; voyages répétés possibles, y compris au même instant. Sauvegarder bâtiments et accès. Aucun équilibrage par accès ni attractivité selon le type de bâtiment.

**Actualisation U61 :** configuration par défaut de 8 taxis et 60 demandes, apparaissant entre 0 et 300 s. Total fixé par paramètre ; horaires indépendants uniformes sur les pas de 0,2 s, simultanéités possibles. Scénario pré-généré et sauvegardé, demandes révélées aux taxis seulement à leur apparition. La fenêtre d'apparition ne constitue pas l'heure d'arrêt.

**Actualisation U60 :** 32 bâtiments par défaut, nombre configurable, tirés uniformément sans remise parmi les cellules non routières disposant d'un accès admissible. Aucun minimum par îlot ; routes puis emplacements admissibles puis tirage et accès fixes sauvegardés. Si le nombre demandé ne peut être placé, signaler la configuration invalide sans réduction silencieuse.

**Actualisation U59 :** carte par défaut de 21 × 21 cellules, 5 axes horizontaux et 5 verticaux, dont 2 de bord et 3 intérieurs par direction. Positions intérieures tirées au hasard puis sauvegardées ; espacement minimal de 2 cellules entre axes parallèles, bords compris. Dimensions et nombres d'axes configurables. Le réseau est différent du réseau routier complet de l'exemple L23 ; ses statistiques ne sont pas transposables automatiquement.

**Actualisation U58 :** montées et descentes interdites aux carrefours d'au moins trois branches ; accès des bâtiments filtrés en conséquence à la génération et à la validation. Passage et virages légaux restent autorisés. Les coins à deux branches du cadre extérieur sont distincts des carrefours et gardent les virages autorisés de U47.

**Actualisation U57 :** générer uniquement des demandes entre accès routiers distincts, et appliquer la même validation aux scénarios chargés. Préparer directement les destinations admissibles plutôt que multiplier les tirages rejetés. Une carte doit posséder au moins deux accès distincts utilisables ; sinon signaler une configuration invalide. Les bâtiments peuvent toujours partager un accès.

**Actualisation U56 :** un accès routier fixe par bâtiment, choisi parmi les cellules routières adjacentes admissibles avec départage déterministe, puis sauvegardé dans le scénario. Toutes les demandes de ce bâtiment utilisent cet accès ; le client y attend et le taxi reste sur le réseau. Plusieurs bâtiments peuvent partager un accès ; demandes entre accès identiques et arrêts aux intersections encore à préciser.

**Actualisation U55 :** estimation du début de prise en charge à vitesse libre de 50 km/h, sans congestion dans la prévision, avec distance restante sur la portion en cours et temps des opérations précédant le client. Congestion réelle U54 maintenue. L'estimation par congestion observée est une amélioration éventuelle, à examiner seulement si nécessaire, sans mise en oeuvre planifiée.

**Actualisation U54 :** congestion par portion dirigée selon v = v_libre / max(1, N/K), K configurable et égal à 2 par défaut. Calcul commun à chaque pas de 0,2 s, incluant les nouvelles entrées ; un taxi en approche à vide compte, un taxi garé ou en montée/descente ne compte pas. Pas de limite bloquante d'entrée ni de files physiques ; estimation de la congestion future dans les offres encore ouverte.

**Actualisation U53 :** pour contrôler la capacité, une place est mobilisée dès le début de montée et jusqu'à la fin de descente. Conserver les états en montée, à bord et en descente pour distinguer les transitions et les mesures. Réservations futures toujours vérifiées par portion, sans occupation physique immédiate.

**Actualisation U52 :** une offre est utilisable uniquement pendant sa ronde et expire à sa clôture. L'identifier par demande, taxi et numéro de ronde ; une acceptation vise cette offre précise. Revalider chaque acceptation de la ronde après les confirmations précédentes. L'expiration ne supprime ni demande persistante ni réservation confirmée ; renouveler les offres nécessaires aux rondes suivantes sans nouveau CFP.

**Actualisation U51 :** phases communes adoptées : fins physiques dues, apparitions, évaluation et offres, choix des clients, revalidation et confirmations par taxi, démarrage des actions possibles, progression de 0,2 s. Une seule ronde de négociation par pas, sans délai simulé ajouté ; après refus, demande persistante réexaminée au pas suivant. Validité et identification des offres restent à préciser.

**Actualisation U50 :** pas de simulation fixe de 0,2 s, horloge représentée par un compteur entier de pas. Une portion libre de 7,2 s prend 36 pas et une montée ou descente de 2 s prend 10 pas. Chaque taxi progresse indépendamment ; réexamen des demandes à chaque pas selon U43. Sous congestion, les fins d'action restent quantifiées à 0,2 s ; ordre détaillé des événements encore ouvert en Q16.

**Actualisation U49 :** D0 est le plus court trajet routier légal entre les accès d'origine et de destination, avec la meilleure orientation de départ possible, identique pour tous les taxis et fixé une fois pour la demande. Le trajet réellement proposé respecte l'orientation du taxi ; les distances supplémentaires imposées par cette orientation consomment aussi le budget. Aucun recalcul de D0 pour augmenter la limite après une réservation ou insertion.

**Actualisation U48 :** après placement, tirer au hasard une orientation légale pour chaque taxi et sauvegarder position et orientation dans le scénario. Aux intersections et aux coins, l'orientation correspond à une arrivée possible par une route existante ; le départ respecte les mouvements autorisés. Le traitement de l'orientation de prise en charge dans D0 reste ouvert.

**Actualisation U47 :** cadre routier extérieur à double sens adopté pour relier les axes intérieurs et éviter les impasses aux bords de la carte. Les quatre coins autorisent les virages à 90°, sans demi-tour. Le réseau reste fini et non torique. Vérifier l'accessibilité des arrêts avec les orientations légales ; orientations initiales et référence D0 restent ouvertes en Q17.

**Actualisation U46, apport du cahier d'équipe adopté le 28 octobre :** demi-tours interdits partout, y compris aux intersections et après un arrêt. Chaque taxi conserve une orientation logique ; il poursuit son sens entre intersections, puis peut continuer ou tourner à gauche ou à droite aux intersections où la connexion existe. Routage, offres et estimations doivent respecter cette orientation. Vérifier l'accessibilité avec ces mouvements autorisés : une carte géométriquement connectée peut néanmoins bloquer un taxi dans un cul-de-sac.

**Actualisation U44 et U45 :** collecte et négociation sans délai simulé ajouté, dans un ordre explicite. Vitesse de référence comprise comme 50 km/h ; avec 100 m entre cellules routières voisines, durée libre fixe de 7,2 s par portion. La congestion retenue antérieurement peut allonger la durée réelle ; la gestion numérique des fractions de seconde reste à décider.

**Actualisation U43 :** demande persistante confirmée. Un CFP initial reste actif jusqu'à réservation ; les taxis réexaminent les demandes mémorisées à chaque pas de simulation pour commencer. Suppression du délai de relance de 5 s dans la cible, ancienneté initiale conservée, clôture notifiée à la réservation. La durée de collecte des offres reste une décision séparée.

**Actualisation U41 :** le premier critère de sélection est désormais le début de prise en charge estimé le plus tôt, en remplacement de la distance d'approche. À égalité d'estimation, conserver le score de budget de détour de U36, puis l'identifiant stable du taxi. U42 demande de conserver les idées du cahier d'équipe comme pistes documentées, sans les transformer toutes en règles adoptées ; voir L34 à L44.

**Cible de réécriture, U23 à U31 :** un seul taxi par voyage, capacité configurable de 1 à 4 passagers avec 3 par défaut, réservations pendant l'approche et capacité vérifiée sur chaque portion. Distance de 100 m entre cellules routières voisines ; réorganisation immédiate des arrêts futurs, avec changements physiques uniquement aux points autorisés. Le budget cumulatif de détour combine 25 % du trajet routier direct et un plafond en mètres. L'adaptation du plafond à 400 m est un choix de référence de l'assistant en réponse à la demande utilisateur, voir L23 ; la carte d'exemple n'est pas la carte finale choisie. Les conventions de l'ancienne implémentation ci-dessous ne fixent pas cette cible. Aucun code modifié.

**Ce document est le point d'entrée pour reprendre le projet avec un autre LLM.** Il conserve les décisions de l'utilisateur, leur évolution et les choix ajoutés par l'assistant pendant la conception et l'implémentation. Il est destiné à être enrichi au fil du travail.

Le projet compare un service de taxis individuels à un service autorisant le partage sur un trajet compatible. Les deux modes doivent partir du même scénario. L'objectif est d'observer les effets du partage sur l'activité des taxis, les temps des passagers et la congestion, sans présupposer que le partage améliore systématiquement les résultats.

## 1. Usage du document et provenance

### 1.1 Distinguer une demande, une proposition et un comportement codé

| Repère | Signification | Comment le reprendre |
| --- | --- | --- |
| Uxx | Décision ou objectif explicitement exprimé par l'utilisateur | Le préserver ; une proposition du LLM ne suffit pas à le remplacer |
| Lxx | Choix proposé ou ajouté par le LLM pour rendre le projet concret | Le documenter comme tel ; il peut être révisé dans le cadre du travail demandé |
| Cxx | Contrainte ou recommandation du cours | La vérifier dans l'énoncé, indépendamment des préférences du LLM |
| Qxx | Ambiguïté ou point non confirmé individuellement | Ne pas le présenter comme une décision explicite de l'utilisateur |

La demande « vasy code » autorisait l'implémentation de la version discutée. Elle ne permet pas d'attribuer rétroactivement à l'utilisateur chaque valeur numérique, algorithme ou convention ajouté par l'assistant.

Pour les choix Lxx, les motivations ci-dessous sont des justifications de conception issues des explications de l'assistant et de la lecture du code. Elles ne constituent pas une validation scientifique du modèle.

### 1.2 Sources et ordre de lecture

1. Les instructions actuelles de l'utilisateur, puis les décisions Uxx encore en vigueur.
2. Le présent registre, pour comprendre la provenance des règles.
3. [Le comportement de la version implémentée](09_modele_implemente.md) et les fichiers de code cités.
4. [L'énoncé commenté](08_projet_session5.md), pour les contraintes du professeur.
5. La [synthèse de conception](04_canevas_conception.md), puis si nécessaire les [anciennes propositions archivées](archives/04_canevas_conception.md). Le [plan d'amélioration](11_priorites_et_experiences.md) contient des recommandations à discuter, sans modifier les décisions actuelles.

Une contradiction entre le code et une décision utilisateur doit être signalée. L'existence d'un comportement dans le programme ne prouve pas que l'utilisateur l'a demandé. Inversement, ce document ne doit pas masquer une différence avec le programme : décrire séparément l'intention et le comportement observé.

### 1.3 Contraintes du cours à ne pas attribuer à l'utilisateur

- **C01 :** les plateformes autorisées sont Python avec Mesa ou Java avec JADE. L'utilisateur a ensuite retenu Mesa, voir U04.
- **C02 :** la branche Mesa recommande `MultiGrid`, exige une communication directe minimale avec CFP et réponses, et demande une visualisation dès le début.
- **C03 :** la démarche doit être simple et incrémentale, avec paramètres et variables observables identifiés.
- **C04 :** code et rapport sont demandés ; conception, implémentation, fonctionnalités/utilisabilité, analyse et présentation comptent chacun pour 20 %.

L'acceptabilité et les embouteillages sont présentés comme optionnels dans l'énoncé. L'utilisateur a choisi d'inclure les embouteillages dans ce projet : leur présence est donc devenue un objectif utilisateur, U06. Les détails administratifs historiques restent dans l'énoncé commenté.

## 2. Décisions explicites de l'utilisateur

Cette section est le socle fonctionnel du projet. Les courtes citations servent à identifier l'origine d'une décision dans la conversation ; leur formulation opérationnelle est donnée juste après.

### U01. Réduire le périmètre de la première étape pour obtenir une base complète

**Origine :** « réduire le spectre mais plus complet ».

Concentrer la première version sur une comparaison compréhensible et cohérente. Les correspondances entre taxis, les détours complexes et l'optimisation générale du transport ne font pas partie du périmètre demandé pour cette version. Cette limitation concerne uniquement la démonstration initiale. U14 confirme que le périmètre final doit être élargi, notamment aux détours.

**Conséquence :** privilégier la cohérence du transport, des durées, des réservations et de la comparaison avant d'ajouter des mécanismes.

### U02. Comparer un mode individuel et un mode partagé, étape reportée par U21

**Origine :** « trajet juste individuelle + un mode avec » les possibilités de regroupement décrites par l'utilisateur.

Le premier mode transporte les passagers individuellement. Le second autorise le partage. Les autres règles et le scénario initial doivent rester communs afin d'interpréter les différences.

**Dans le code :** le paramètre `shared` de `TaxiModel` sélectionne la politique. La capacité physique de deux places est un choix L05, pas une valeur imposée explicitement par l'utilisateur.

### U03. Autoriser le regroupement pour des trajets compatibles

**Origine :** même origine et même destination ; ou une personne sur le trajet, allant vers la même destination ou vers une destination sur ce trajet.

Le service partagé doit couvrir au moins ces deux situations. La version opérationnelle retenue par l'assistant est : l'origine puis la destination du nouveau passager doivent apparaître dans cet ordre sur le trajet restant. Cette formalisation évite de revenir en arrière et conserve le trajet spatial déjà prévu.

**Exemples sur A → B → C → D :** A vers D avec A vers D ; A vers D avec B vers D ; A vers D avec B vers C. C vers B ne correspond pas à cette logique. La même origine avec une destination intermédiaire, par exemple A vers C, est également autorisée par la généralisation L06.

**Dans le code :** `Taxi.can_accept()` et `remaining_service_route()` dans `taxishare/agents.py` (ancien module ; voir [Passenger](../taxishare/passenger.py) et [Taxi](../taxishare/taxi.py) dans le code actuel).

### U04. Utiliser Mesa

**Origine :** « comme on va faire du mesa ».

Le choix de la plateforme est exprimé par l'utilisateur. Le choix précis de `MultiGrid`, la géométrie de la carte, les versions installées et l'interface sont des choix techniques de l'assistant, décrits plus loin.

### U05. Construire une comparaison reproductible et équitable, étape reportée par U21

**Origine :** mêmes seed, nombre de demandes et nombre de taxis pour comparer les modes.

Les placements initiaux, demandes et conditions de circulation doivent être communs. Le calendrier est rejoué à l'identique. Un mode ne doit pas recevoir une demande plus simple à servir simplement parce qu'il a consommé les tirages dans un autre ordre.

La solution technique choisie est de générer puis sauvegarder un scénario complet, L01. La même seed est un moyen de reproduction ; le scénario sauvegardé est l'entrée commune effectivement utilisée.

**Important :** les règles et conditions de départ de la congestion sont identiques. Les ralentissements produits pendant les exécutions peuvent différer, car cette différence fait partie du résultat à étudier.

### U06. Inclure les embouteillages dans la comparaison

**Origine :** inclure les embouteillages « pour voir vraiment le progrès entre les deux versions ».

La simulation doit tenir compte du ralentissement des taxis lorsque la circulation se charge. La distance et les temps sont mesurés pour évaluer l'effet du partage.

L'utilisateur a demandé ce mécanisme, mais n'a pas fixé la formule de vitesse, la valeur du seuil de fluidité ou un modèle réaliste de files. Ces éléments sont L12 et Q04.

### U07. Distinguer les sens de circulation

**Origine :** « l'embouteillage a un sens, dans la case ».

Une concentration de véhicules dans une même case ne doit pas suffire à ralentir tous les mouvements. Les sens opposés et les sorties différentes sont distingués.

**Précision apportée par l'assistant :** deux taxis ayant des destinations finales différentes peuvent se ralentir s'ils empruntent la même portion dans le même sens. La destination finale ne définit pas à elle seule le groupe de congestion.

**Dans le code :** la charge est indexée par une portion dirigée `(départ, arrivée)`, L12. Les conflits de croisement à l'intérieur d'une intersection ne sont pas représentés, L13.

### U08. Répartir les responsabilités pour alléger l'environnement, précision U17

**Origine :** « diviser ses fonctions à d'autres systèmes/agents comme la messagerie ».

Formulation initiale : l'environnement ne devait pas concentrer toute la logique dans un bloc unique, avec une messagerie et des responsabilités communes séparées. U17 précise que cela ne signifie pas fragmenter l'environnement en de nombreuses sous-étapes : conserver un environnement global cohérent et découper surtout les comportements.

L'utilisateur a laissé ouverte la distinction entre systèmes et agents. L'assistant a retenu deux types d'agents décisionnels et plusieurs services ordinaires, L04. Il n'a pas transformé chaque service en agent autonome.

### U09. Exprimer le temps en secondes

**Origine :** « le temps pas en tour mais en seconde ».

Les déplacements, embarquements et autres opérations possèdent des durées explicites en secondes. Une opération en cours n'immobilise pas les autres taxis.

L'utilisateur n'a pas imposé une résolution numérique d'une seconde ni une simulation par événements. La résolution choisie est L10.

### U10. Conserver l'aléatoire pour le scénario, puis employer des durées fixes

**Origine :** « des random pour les spawns des taxis et des gens au début mais le reste sera des temps fixes », avec l'exemple d'un embarquement de 2 secondes.

Les positions initiales des taxis et la localisation des demandes sont aléatoires. Les durées ne sont plus tirées au hasard. L'apparition progressive aléatoire des demandes a ensuite été explicitement réintroduite, U11.

**Valeur retenue :** l'embarquement de 2 secondes reprend l'exemple utilisateur. Les 2 secondes de descente, 60 mètres par portion et 10 m/s sont des conventions de l'assistant.

**Distinction nécessaire :** une durée de base fixe n'empêche pas une durée réelle variable sous l'effet déterministe de la congestion. Aucun nouveau hasard n'est nécessaire pour produire ce ralentissement.

### U11. Prévoir un total de demandes qui apparaissent pendant la simulation

**Origine :** fixer par exemple 30 demandes pour la journée, puis les faire apparaître de manière aléatoire pendant la simulation.

Le total est défini avant l'exécution. Les demandes ne sont pas toutes actives à 0 seconde : chacune possède une heure d'apparition. Les demandes futures doivent donc être prises en compte dans la condition d'arrêt.

Le nombre 30 est un exemple devenu valeur par défaut. Le code permet de le configurer. La distribution uniforme des apparitions et la fenêtre de 300 secondes ont été choisies par l'assistant, L02. Le tirage aléatoire du nombre total reste Q01.

### U12. Arrêter lorsque toutes les demandes prévues sont résolues

**Origine :** « la simulation arrête quand toutes les demandes prévues ont été résolues ».

Une période sans passager actif ne doit pas arrêter la simulation si une demande future est encore prévue.

L'assistant a donné à « résolue » le sens opérationnel de **passager arrivé à destination, descente terminée**, L15. Une réponse à un appel, une réservation ou un embarquement ne suffisent pas. Les deux modes peuvent terminer à des heures différentes.

### U13. Maintenir une base documentaire réutilisable entre LLM

**Origine :** demande actuelle du 27 octobre 2026.

La documentation doit mettre les décisions utilisateur au premier plan et isoler les décisions ajoutées par l'assistant. Chaque LLM doit pouvoir la modifier et l'enrichir en conservant la provenance et l'historique.

La présente mise à jour est documentaire. Elle ne modifie pas les règles du simulateur.

### U14. Distinguer démonstration initiale et objectif final

**Origine :** clarification explicite de l'utilisateur le 27 octobre 2026 : « l'objectif final, c'est de répondre à toutes les attentes du prof avec des détours, etc. ».

**Statut : objectif final confirmé, non implémenté par cette mise à jour.** Le transport individuel et le partage jusqu'à deux passagers sans détour sont des étapes de démonstration. Ils ne constituent pas le périmètre final du projet. L'objectif final inclut les détours et une progression vers les niveaux avancés du sujet, en conservant les exigences de conception, communication, visualisation et analyse.

U14 précise la portée de U01 et dépasse la recommandation de l'assistant de conserver le périmètre initial. Les règles L05 à L07 décrivent toujours la version actuelle ; elles ne doivent pas être présentées comme des limites définitives.

La progression de l'énoncé évoque aussi multi-hop et plusieurs passagers. La signification exacte de multi-hop, les capacités finales et les limites de détour restent à définir. Ne pas inventer ces règles ni présenter toutes les extensions comme des obligations explicites du professeur : la cible élargie est ici une décision utilisateur.

### U15. Viser une carte générée simplement

**Origine :** demande utilisateur du 27 octobre 2026 : « une carte qui se génère et qui n'est pas faite à la main en avance », si cela reste simple.

**Statut : objectif conditionnel confirmé, non implémenté.** Remplacer à terme la géométrie dessinée à l'avance par une génération automatique, si une méthode simple et fiable convient au projet. Le réalisme urbain détaillé n'est pas demandé. La carte fixe actuelle, L03, reste une base de démonstration jusqu'à cette évolution.

Conserver la comparaison équitable U05 : une carte générée doit être commune aux modes comparés et sauvegardée dans le scénario. La reproductibilité de la génération, l'accessibilité des origines et destinations et la connexité du réseau sont des critères de conception à vérifier. Les paramètres et l'algorithme précis ne sont pas fixés par l'utilisateur.

### U16. Privilégier les outils Mesa adaptés avant de réimplémenter

**Origine :** demande utilisateur du 27 octobre 2026 de privilégier les outils Mesa, sauf bonne raison d'utiliser un autre outil ou une solution personnalisée.

**Statut : principe de conception confirmé, à appliquer aux évolutions et à la revue des choix existants.** Avant de créer ou remplacer un composant, examiner les capacités de Mesa dans la version retenue. Employer les outils Mesa lorsqu'ils répondent au besoin de manière simple et correcte. Justifier explicitement un recours externe ou une réimplémentation : fonctionnalité absente, incompatibilité de version, inadéquation aux règles du modèle ou complexité disproportionnée.

Ce principe concerne notamment espace, gestion et activation des agents, aléatoire, collecte, expériences et visualisation. Il ne présume pas qu'un générateur de routes ou un protocole métier donné existe dans Mesa. Vérifier les capacités et la compatibilité avant toute proposition technique. Conserver les exigences de l'énoncé, notamment les messages directs, et les décisions temporelles du modèle.

Les choix existants L01, L04, L09, L16 à L19 restent documentés comme état actuel. Ils doivent être réévalués selon U16 sans déclencher une réécriture automatique ou une migration non justifiée.

### U17. Environnement global et comportements courts

**Origine :** clarification utilisateur du 27 octobre 2026 : conserver « un environnement un peu global » et privilégier le découpage « au niveau des behaviors » pour la lisibilité et la fiabilité.

**Statut : orientation d'architecture confirmée, sans refonte effectuée.** Conserver un environnement global cohérent qui représente le monde et coordonne la simulation. Ne pas multiplier artificiellement ses sous-étapes ou ses composants. Des agents ou services complémentaires peuvent interagir avec cet environnement si une responsabilité réelle le justifie et permet de l'alléger.

Le découpage recherché porte d'abord sur les comportements des agents : responsabilités ciblées, blocs courts et lisibles, états et transitions explicites. Par exemple, évaluer une demande, choisir une offre, confirmer une réservation, avancer et traiter un arrêt sont des responsabilités à examiner séparément. Ces exemples ne prescrivent pas une classe ou un agent pour chaque action.

U17 précise U08. L04 et le contrat temporel décrivent l'état actuel, sans constituer une architecture finale imposée. La clarification ne demande pas de supprimer les phases nécessaires à la cohérence des échanges et déplacements, ni de modifier leurs durées. Un découpage interne du code doit rester distinct d'un changement des règles temporelles du modèle.

La brièveté facilite la compréhension et la vérification, mais ne garantit pas seule la robustesse : conserver des contrats clairs, des transitions cohérentes et les invariants utiles. Appliquer U16 avant d'introduire un mécanisme de comportements personnalisé. Le mot behavior exprime ici une organisation souhaitée, sans imposer une API particulière.

### U18. Structure claire et commentaires de logique maintenus

**Origine :** demande utilisateur du 27 octobre 2026 : structure claire, commentaires expliquant la logique à chaque endroit et commentaires mis à jour à chaque évolution du code.

**Statut : règle de développement confirmée, sans modification du code dans cette mise à jour.** Organiser les fichiers, classes, fonctions et comportements de façon lisible, avec des noms explicites et des responsabilités identifiables, en cohérence avec U17.

Chaque partie du code doit être accompagnée de commentaires adaptés expliquant sa logique : rôle, étapes du traitement, raisons des choix, hypothèses, transitions, contraintes et cas particuliers concernés. Des docstrings peuvent présenter les contrats des modules, classes et fonctions ; les commentaires au niveau des blocs expliquent le déroulement local. Privilégier l'explication du raisonnement plutôt que la simple répétition de la syntaxe.

À chaque mise à jour du code, relire les commentaires et docstrings concernés, y compris ailleurs s'ils décrivent le comportement modifié. Les corriger ou les compléter dans la même mise à jour, supprimer les explications devenues fausses et vérifier qu'ils décrivent le fonctionnement réel. Une modification n'est pas terminée si ses commentaires sont obsolètes. Synchroniser aussi la documentation concernée lorsque les règles ou l'architecture évoluent.

Cette exigence doit guider les prochaines modifications et la revue du code existant. Son inscription ne prouve pas que tous les commentaires du projet ont déjà été relus ou complétés.

**Précision utilisateur du 27 octobre 2026, langue du code :** tous les commentaires et docstrings doivent être rédigés en anglais. Tous les noms définis dans le code doivent être en anglais : fonctions, méthodes, classes, variables, paramètres, attributs, constantes et modules. Appliquer cette règle aux créations et aux mises à jour, et vérifier la cohérence des références lors des renommages. Cette précision complète U18 sans changer la langue des échanges ou de la documentation générale, qui reste celle demandée par l'utilisateur. Aucun commentaire existant n'est traduit ni aucun identifiant renommé par cette mise à jour documentaire.

### U19. Limiter les règles et données codées en dur

**Origine :** demande utilisateur du 27 octobre 2026 d'éviter de coder en dur de nombreuses règles, avec la carte comme exemple.

**Statut : principe de conception confirmé, sans refonte effectuée.** Éviter les cartes, valeurs et cas particuliers dispersés dans les comportements. Les éléments destinés à varier doivent provenir de paramètres explicites, de données de scénario ou d'une génération simple. Centraliser les valeurs par défaut, les nommer, préciser leurs unités et valider les entrées. Les agents doivent fonctionner à partir de ces informations plutôt que dépendre de coordonnées ou de nombres spécifiques à une démonstration.

Pour la carte, U15 demeure un objectif de génération automatique conditionné à une méthode simple. U19 demande aussi que les traitements de transport et d'affichage ne supposent pas une géométrie particulière. Les exemples fixes peuvent rester des scénarios de démonstration ou de vérification clairement identifiés.

Distinguer les paramètres expérimentaux, les politiques susceptibles de varier et les invariants du modèle. Une capacité maximale configurable n'implique pas de rendre optionnel le respect de cette capacité. Les règles fondamentales peuvent rester explicites dans le code ; éviter de transformer chaque instruction en option ou de construire un moteur de règles générique sans besoin concret. Justifier les choix qui restent fixes.

Cette règle complète U15 à U18 : configuration simple et documentée, priorité aux outils Mesa adaptés, environnement cohérent et comportements courts. Une nouvelle configuration doit être sauvegardée avec les scénarios pour préserver la reproductibilité des comparaisons. La présente mise à jour ne constate pas la suppression des éléments déjà codés en dur.

### U20. Préférer une réécriture propre à une adaptation trop coûteuse

**Origine :** demande utilisateur du 27 octobre 2026 de privilégier le remplacement du code lorsque l'effort d'adaptation devient trop important, pour éviter le bricolage lié aux modifications successives.

**Statut : principe de développement confirmé, aucun remplacement effectué ici.** Compte tenu des évolutions importantes prévues, ne pas conserver une implémentation uniquement parce qu'elle existe. Si l'adapter exige trop de contournements, de branches particulières ou de dépendances à une ancienne architecture, privilégier sa suppression et une réécriture propre de la partie concernée.

Comparer simplement le coût et la clarté des deux solutions au regard des objectifs actuels. Le choix doit favoriser une structure cohérente, des comportements lisibles, les outils Mesa adaptés et une maintenance simple. Ne pas multiplier les couches de compatibilité ou maintenir deux chemins concurrents sans nécessité. Une réécriture peut concerner un comportement, un module ou un ensemble plus large si les dépendances le justifient ; elle n'impose pas de recommencer systématiquement tout le projet.

Préserver les décisions métier encore valables, les scénarios utiles et les critères de vérification pertinents, sans imposer la conservation des anciens détails d'implémentation. Lors d'un remplacement, retirer le code devenu inutile et synchroniser commentaires et documentation conformément à U18. Documenter séparément les changements de règles voulus et les remplacements internes qui doivent conserver le comportement.

### U21. Une seule simulation pour le développement actuel

**Origine :** demande utilisateur du 27 octobre 2026 : ne pas alourdir le code avec deux simulations simultanées ; se concentrer sur la simulation, puis examiner plus tard le mode à un passager et les autres comparaisons.

**Statut : priorité de développement confirmée, interface actuelle non modifiée ici.** Développer un seul monde simulé et son fonctionnement. Ne pas imposer deux modèles exécutés simultanément ni une interface comparative comme architecture cible actuelle. Les modes de référence, notamment un seul passager par taxi, et leur mécanisme de comparaison sont reportés à une étape ultérieure.

U21 précise la priorité de U02 et U05 sans abandonner l'objectif final d'analyse du projet. Conserver les données nécessaires à la reproductibilité, sans construire maintenant une infrastructure de comparaison. Les comparaisons pourront utiliser des exécutions séparées ; aucun choix détaillé n'est encore fixé. U14 et les objectifs de détours et niveaux avancés restent valables.

L17 et les documents d'utilisation décrivent encore une interface à deux simulations dans la version existante. Cette description n'est pas une instruction de conserver cette organisation ; son remplacement devra respecter U20 si l'adaptation est trop lourde.

### U22. États et progression indépendants pour chaque taxi

**Origine :** demande utilisateur du 27 octobre 2026 : un taxi qui attend ne doit pas faire attendre les autres ; les taxis doivent pouvoir avoir des états différents.

**Statut : exigence de comportement confirmée, pas de nouvel audit d'exécution.** Chaque taxi possède son état de service, ses engagements, sa progression et les délais propres à son action. Au même instant simulé, un taxi peut embarquer, un autre rouler, un autre attendre une demande et un autre déposer un passager. Aucun état global de flotte ne doit imposer la même action ou une attente collective parce qu'un taxi attend.

Les durées d'embarquement, de descente ou d'attente sont représentées dans la simulation et ne bloquent pas la progression des autres taxis. Une horloge commune et un ordonnancement central restent compatibles avec cette indépendance ; aucun thread ou processus par taxi n'est requis. Les interactions physiques ou de réservation prévues par le modèle, notamment la congestion, peuvent légitimement influencer plusieurs taxis.

Critère de vérification à appliquer lors des évolutions : dans un scénario contrôlé, pendant qu'un taxi consomme un arrêt de plusieurs secondes, un autre continue sa progression et un troisième peut rester disponible. Vérifier les états, positions et échéances à plusieurs instants, et non seulement le résultat final. Les noms et la représentation exacte des états restent à choisir selon U16 à U18.

### U23. Un seul taxi par voyage, sans correspondance

**Origine :** réponse utilisateur du 27 octobre 2026 à la question 1 : « on garde A seulement ».

**Statut : confirmé pour la cible, non implémenté par cette mise à jour.** Un passager effectue son voyage dans un seul taxi. Plusieurs arrêts et plusieurs passagers sont possibles ; les changements de taxi sont exclus de la cible retenue. Ce choix précise U14 : les niveaux avancés ne comprennent pas de correspondances. Ne pas présenter les arrêts multiples comme une réalisation des correspondances dites multi-hop.

### U24. Capacité configurable, trois passagers par défaut et quatre au maximum

**Origine :** réponse utilisateur à la question 2 : « C passe à trois passager par défault avec 4 en max ».

**Statut : confirmé pour la cible, non implémenté.** La capacité en passagers est un paramètre entier positif, limité à quatre, avec trois par défaut. Le conducteur ne fait pas partie de ce nombre. L05 et la valeur historique de deux places ne définissent plus la capacité cible. Le choix d'un mode expérimental individuel reste reporté selon U21.

### U25. Réservations pendant l'approche et occupation par portion

**Origine :** réponse utilisateur à la question 2 : réservations autorisées pendant l'approche du premier passager ; une place est réservée seulement pour la partie du trajet concernée.

**Statut : confirmé pour la cible, non implémenté.** Le taxi peut accepter d'autres demandes pendant l'approche du premier client. Vérifier l'occupation prévue entre chaque prise en charge et dépose de l'itinéraire candidat, avec les passagers présents et les réservations confirmées. Le nombre total d'engagements peut dépasser la capacité si leurs occupations ne se chevauchent pas au-delà de cette limite. Cette règle remplace le comptage conservateur L05 et l'interdiction d'approche L07 pour la cible.

**Exemple :** pour deux places, Alice de A à C, Bob de A à B et Chloé de B à D peuvent être réservés ensemble si Bob descend avant que Chloé embarque. Les règles générales d'ordre et de durée des opérations à un même arrêt restent à confirmer.

### U26. Acceptabilité des détours exprimée en distance

**Origine :** réponse utilisateur à la question 3 : proposer une règle en distance, car le temps futur dépend des embouteillages, en protégeant les petits trajets et en restant adaptée aux grands.

**Statut : principe confirmé, précisé par U30.** La distance supplémentaire liée au partage sert de critère d'acceptation des détours. Les temps restent simulés et mesurés ; cette règle ne garantit ni une heure d'arrivée ni une limite de retard temporel. U30 confirme la règle de L21 et demande une adaptation à l'échelle de la carte, consignée en L23. La limite d'attente avant embarquement et l'effet des arrêts sans distance supplémentaire restent ouverts.

### U27. Révision des itinéraires sous protection des clients engagés

**Origine :** réponse utilisateur à la question 4 : accord pour B, avec ajout d'un client uniquement si l'acceptabilité des clients actuels est conservée, même si leur arrivée est un peu repoussée.

**Statut : principe confirmé, non implémenté.** Un itinéraire confirmé peut être modifié pour ajouter un client si l'itinéraire candidat reste admissible pour tous les clients déjà engagés, y compris ceux réservés mais pas encore embarqués. La limite doit être contrôlée de manière cumulative et non accordée à nouveau pour chaque insertion. Les détails de calcul sont proposés en L21. Ne pas attendre la fin de la course pour réexaminer les arrêts futurs.

L'utilisateur a initialement contesté l'obligation de terminer le déplacement en cours avant de récupérer un nouveau client. Après distinction entre course entière et portion routière, U31 confirme les changements physiques aux points autorisés, voir L22 et Q10. L'accord initial pour B ne constituait pas à lui seul cette confirmation.

### U28. Documenter chaque décision de conception au fil des échanges

**Origine :** instruction utilisateur du 27 octobre 2026 : « à partir de maintenant je te laisse documenté chacune des decision ».

**Statut : autorisation documentaire continue.** Consigner chaque choix confirmé avec son origine, ses conséquences et son statut ; conserver séparément les propositions et les questions ouvertes. Synchroniser les synthèses concernées sans attendre une nouvelle autorisation à chaque échange. Cette autorisation complète U13 ; elle n'autorise pas l'implémentation du simulateur ni la suppression de l'ancien code.

### U29. Échelle spatiale de référence de 100 mètres

**Origine :** réponse utilisateur du 27 octobre 2026 à la nouvelle proposition de détour : fixer la taille des cellules, avec « peut etre faire 100 m pour rendre les clacult plus simple ».

**Statut : référence retenue dans le cadre de l'adaptation demandée, non implémentée.** Une cellule carrée représente 100 m de côté ; un déplacement routier horizontal ou vertical entre cellules voisines représente 100 m. La présence de routes, de bâtiments, le nombre de cellules et l'éventuelle marche restent à définir. La grille n'est pas torique. La valeur historique de 60 m par portion n'est pas la cible. Le calcul de distance doit respecter les routes accessibles ; ne pas confondre distance routière et distance à vol d'oiseau.

### U30. Validation du budget de détour et adaptation à une carte d'exemple

**Origine :** réponse utilisateur à la question 3 : accord pour la règle proposée, avec demande d'adapter la limite à un trajet moyen sur une carte d'exemple et à l'échelle de 100 m.

**Statut : règle confirmée, choix numérique adapté par l'assistant en L23, non implémenté.** Le budget est cumulatif et vaut le minimum de 25 % du plus court trajet routier direct du passager et d'un plafond métrique. Contrôler la distance personnelle déjà parcourue à bord plus celle prévue jusqu'à la destination ; ne pas renouveler le budget à chaque réservation. La valeur de 500 m proposée initialement est réexaminée, pas considérée comme un seuil définitif imposé par l'utilisateur. L23 retient 400 m comme valeur de référence adaptée pour l'exemple ; le taux et le plafond restent configurables. La carte d'exemple ne devient pas automatiquement une décision sur le générateur final.

### U31. Révision immédiate du programme, changements physiques aux points autorisés

**Origine :** réponse utilisateur à la question 4 : « on pars sur A » après explication des deux conventions physiques.

**Statut : confirmé pour la cible, non implémenté.** Le taxi peut réorganiser immédiatement ses arrêts futurs, y compris pour prendre un nouveau passager avant le premier réservé. Un taxi sur une portion termine cette portion jusqu'au prochain point autorisé avant un arrêt ou un changement de direction. Pas d'arrêt ou de demi-tour au milieu d'une portion. La définition des points et sens autorisés appartient à la carte. La progression et la distance déjà parcourues sont conservées. Ce choix confirme L22 et ferme Q10 pour la cible.

### U32. Choisir un taxi proche et tenir compte des budgets de détour

**Origine :** réponse utilisateur à la question 6 : retenir A si les taxis proches respectent les détours autorisés ; si plusieurs peuvent, choisir celui qui a le moins utilisé son budget de détour.

**Statut : confirmé et précisé par U36, non implémenté.** Ne considérer que des offres respectant capacité et acceptabilité de tous les clients engagés ainsi que du candidat. Le choix privilégie la proximité de prise en charge et ajoute un critère de budget de détour utilisé. La proximité doit être la distance d'approche réellement prévue par l'offre, avec les arrêts déjà engagés et la portion en cours ; pas une distance à vol d'oiseau ignorant les engagements. Ne pas attribuer un unique budget personnel au taxi : U30 définit des budgets par passager. U36 confirme le départage uniquement à distance égale et le score relatif maximal après insertion de L29. La proposition L25 de choix par arrivée finale estimée est écartée.

### U33. Continuer à chercher sans abandon volontaire

**Origine :** réponse utilisateur à la question 7 : « A ».

**Statut : confirmé pour la cible, mécanisme précisé par U43, non implémenté.** Sans offre ou après un refus, la demande reste en attente jusqu'à réservation puis livraison. Pas de patience maximale ni d'état abandonné dans la cible actuelle. La relance de 5 s avait été une référence de l'assistant dans L26 ; U43 la remplace par une demande persistante réexaminée sans nouvel appel périodique. Un arrêt technique reste incomplet avec les demandes non livrées identifiées ; il ne devient pas une réussite. L'arrêt normal nécessite toujours toutes les livraisons et aucune demande future.

### U34. Arrêts successifs, déposes avant montées et taxi hors circulation

**Origine :** réponse utilisateur à la question 8 : « je valides sans changement ».

**Statut : confirmé pour la cible, non implémenté.** Les déposes précèdent les prises en charge. Chaque descente prend 2 s, chaque montée 2 s, les opérations sont successives. Deux descentes et une montée prennent donc 6 s. Départ dès la fin des opérations, sans attendre volontairement d'éventuels futurs clients. Le taxi arrêté est hors du flux de circulation ; les autres taxis continuent et ne sont pas ralentis directement par son arrêt. Ce choix confirme L27 et précise Q07. Les nouvelles insertions doivent conserver une occupation valide pendant les opérations, pas seulement entre les arrêts.

### U35. Approche protégée sans plafond d'opérations supplémentaires

**Origine :** réponse utilisateur à la question 5 reformulée : « fait A mais sans les opérations maximum pour simplifier ».

**Statut : confirmé pour la cible, non implémenté.** À la confirmation initiale d'un client, conserver la longueur totale de l'approche annoncée. Toute nouvelle insertion doit respecter, pour chaque client confirmé non embarqué : distance déjà parcourue par son taxi depuis cette confirmation + distance prévue jusqu'à sa montée <= approche annoncée à la confirmation. Ne pas remettre la référence à zéro à chaque insertion. Une insertion sur le chemin peut ajouter des montées et descentes avant le client réservé, sans plafond du nombre d'opérations ; capacité et autres engagements restent obligatoires. Le budget de détour personnel à bord continue de s'appliquer après sa montée.

Cette règle confirme la protection spatiale de L28 A, mais retire explicitement la proposition de deux opérations maximum et sa limite de 4 s. Les opérations gardent leurs durées de 2 s selon U34. Elle ne garantit aucune attente maximale réelle : les arrêts ajoutés sur le chemin et la congestion peuvent prolonger l'attente. L'alternative d'une marge de service de 30 s n'est pas retenue. Le contrôle doit protéger toutes les réservations existantes, pas seulement le premier client.

### U36. Ordre initial de sélection des offres et score de budget, premier critère remplacé par U41

**Origine :** réponse utilisateur : « je valide le 6 », après présentation de l'ordre et du score de L29.

**Statut : confirmé pour la cible, non implémenté.** Filtrer d'abord les offres inadmissibles pour capacité, détour et approche protégée. Minimiser ensuite la distance prévue avant prise en charge. À distance égale seulement, choisir le plus faible maximum des parts de budget de détour utilisées par les passagers déjà engagés et le candidat, après insertion. En dernière égalité, choisir l'identifiant stable du taxi.

La part utilisée compare le détour personnel cumulé, déjà effectué et encore prévu à bord, au budget personnel autorisé. Pour un budget nul, aucun détour positif n'est admissible et la part vaut zéro pour un trajet sans détour. L'ajout hypothétique du candidat fait partie du calcul, y compris pour un taxi auparavant vide. Un taxi à 200 m avec une part maximale de 0 % ne passe pas devant un taxi admissible à 100 m avec 20 %. Cette règle confirme L29 ; elle ne définit pas encore la méthode par laquelle chaque taxi construit son itinéraire candidat.

### U37. Construire les offres par insertion en conservant l'ordre des anciens arrêts

**Origine :** réponse utilisateur à la question 9 : « je valide A ».

**Statut : confirmé pour la cible, non implémenté.** Chaque taxi essaie les positions possibles de la montée et de la descente du candidat, montée avant descente, sans réordonner les arrêts déjà engagés. Éliminer les candidats qui violent une capacité par portion, une approche protégée, un budget personnel de détour ou une contrainte physique. Parmi les itinéraires admissibles, choisir celui qui ajoute le moins de distance totale au taxi ; conserver un départage déterministe pour les itinéraires équivalents. Ce choix confirme L30. Il ne cherche pas l'optimum parmi toutes les permutations des arrêts. Le passager compare ensuite les offres selon U36.

### U38. Acceptations concurrentes traitées par ancienneté de demande

**Origine :** réponse utilisateur à la question 10 : « A », suivie d'une question sur le rôle du client et du taxi dans l'appel.

**Statut : confirmé pour la cible, non implémenté.** Quand plusieurs clients acceptent une offre du même taxi pendant une phase, traiter d'abord la demande la plus ancienne, puis l'identifiant du passager en cas d'égalité. Chaque confirmation met à jour les engagements ; le taxi revalide avant de confirmer le suivant et refuse s'il n'est plus admissible. Une offre seule ne réserve pas de place. Le client refusé reprend sa recherche selon U33. Ce choix confirme L31 ; il ne signifie pas que le taxi attribue seul les demandes sans appel ni choix d'offre par les clients.

**Clarification pédagogique, sans nouvelle décision attribuée à l'utilisateur :** le client initie un appel à propositions CFP avec son origine et sa destination. Un taxi évalue ses propres possibilités et peut proposer un service. Le client compare les offres selon U36 et accepte une seule offre ; le taxi sélectionné revalide et confirme ou refuse. Il y a donc deux arbitrages : le client sélectionne une offre de taxi ; en cas de concurrence, le taxi traite les acceptations selon U38. Le taxi calcule lui-même sa distance d'approche et son score de budget et les communique ; le passager ne lit pas les états privés des autres agents. Les détails de livraison, de clôture des offres et de durée des phases restent à décider ; ne pas transformer cette explication en validation des conventions temporelles historiques de L09.

### U39. Carte générée par axes orthogonaux à double sens

**Origine :** réponse utilisateur à la question 11 : « A ».

**Statut : confirmé pour la cible, non implémenté.** Générer des axes routiers horizontaux et verticaux complets qui se croisent, à double sens et sans diagonales. Leurs positions sont générées ; au moins un axe de chaque orientation garantit la connexion de ce réseau. Placer les bâtiments dans des cellules non routières adjacentes à une route et leur associer un accès. Taille et nombre d'axes sont configurables, échelle de 100 m selon U29. Sauvegarder la géométrie et vérifier les conditions de placement, les accès et la disponibilité d'origines et destinations distinctes. Ce choix confirme L32 et précise L20. Les dimensions par défaut et les nombres de routes et bâtiments restent à choisir ; 21 × 21 est toujours un exemple de calcul, pas une taille finale validée.

### U40. Taxis sans engagement garés sur place

**Origine :** réponse utilisateur à la question 12 : « A ».

**Statut : confirmé pour la cible, non implémenté.** Un taxi sans engagement reste garé à sa position, hors du flux de circulation, et continue de répondre aux demandes. Après sa dernière dépose, il attend sur place son prochain engagement. Aucun repositionnement vers un centre ou une zone de demande n'est introduit. Ce choix confirme L33. Les trajets à vide pour rejoindre un client confirmé restent comptés dans les déplacements et la congestion.

### U41. Choisir selon le début de prise en charge estimé

**Origine :** demande utilisateur du 27 octobre 2026 après comparaison avec le cahier d'équipe : « pour l'instant on va garder son Choisir selon le début de prise en charge estimé ».

**Statut : règle courante confirmée, non implémentée.** Parmi les offres admissibles, choisir la date estimée de début d'embarquement la plus proche. Ce critère remplace la distance d'approche dans U32, U36 et L29 ; leur historique reste conservé. À égalité de date estimée, conserver le plus faible maximum des parts de budget de détour utilisées après insertion, puis l'identifiant stable du taxi. Le reste du classement du cahier d'équipe, notamment arrivée finale, préférence pour taxi vide et tirage au sort, n'est pas adopté par cette demande.

Le taxi calcule et communique une date absolue estimée de début de montée, pas de fin de montée. Inclure portion et opération en cours, déplacements restants et arrêts engagés avant ce client ; les opérations de montée du client lui-même ne précèdent pas son début de prise en charge. Utiliser uniquement les informations disponibles et les hypothèses routières explicites ; ne pas accéder aux demandes futures pour améliorer les prévisions. La méthode exacte de prévision de congestion reste ouverte. L'estimation n'est pas une garantie ; capacité, budgets personnels en distance et approche protégée de U35 restent des conditions impératives. Les renvois historiques au classement U36 se lisent avec cette actualisation U41.

### U42. Conserver les idées utiles du cahier d'équipe pour examen

**Origine :** instruction utilisateur : « sauvegarde les idée dans le point 4 », après la liste des apports du cahier transmis par son équipier.

**Statut : sauvegarde documentaire autorisée et effectuée ; adoption fonctionnelle à décider séparément.** L34 à L44 conservent les dix idées du tableau et l'adaptation des métriques. Certaines explicitent des principes déjà retenus ; les détails nouveaux restent à confirmer. Cette instruction ne valide pas automatiquement les 2 s de collecte, les 2 s par segment, la patience, les durées aléatoires, l'interdiction de tous les demi-tours ou les restrictions de partage du cahier d'équipe. Aucun de ces mécanismes n'est ajouté au code.

### U43. Une demande persistante, sans relances périodiques

**Origine :** réponse utilisateur « oui vasy » à la recommandation de remplacer les relances de 5 s par un CFP initial mémorisé et réexaminé.

**Statut : confirmé pour la cible, non implémenté.** Le client diffuse un seul appel pour sa demande. Les taxis sollicités le conservent parmi les demandes connues actives et le réexaminent à chaque pas de simulation pour la première version. Aucun délai fixe ou aléatoire de relance n'est imposé ; un réexamen ne recrée ni client, ni demande, ni CFP. L'identifiant et l'heure d'apparition restent constants. Un échec ou un refus d'offre laisse la demande active.

Les taxis proposent selon leurs engagements actualisés ; le client choisit selon U41 ; chaque confirmation revalide selon U38. Une réservation confirmée clôt la recherche et est notifiée aux autres taxis concernés pour retirer les demandes et offres devenues obsolètes. Conserver les échanges explicites, sans lecture privée de l'état des clients ni affectation centrale à leur place. L'ancienneté départage les demandes compatibles concurrentes pour un même taxi, sans bloquer les suivantes derrière une demande impossible.

Cette décision confirme L45, remplace le délai historique de L26 et précise U33 sur la recherche sans abandon. Les offres n'acquièrent pas pour autant une validité permanente : leur expiration et leurs versions restent à préciser. La durée de collecte, la résolution temporelle et les mouvements restent des décisions séparées. Une réévaluation sur événements pourra remplacer l'examen à chaque pas si le coût de calcul le justifie. La présente validation porte sur la conception documentée, sans autorisation d'implémenter le simulateur dans cet échange.

### U44. Communication sans délai simulé ajouté

**Origine :** annotation utilisateur « Sauvegarde ça je suis d'accord » sur la recommandation de commencer sans délai simulé ajouté, avec un ordre de traitement explicite.

**Statut : confirmé pour la cible, non implémenté.** Appel ou réexamen, réponses des taxis, comparaison des offres, acceptations, revalidations et confirmations suivent un ordre logique explicite au même instant simulé. Aucune fenêtre d'attente de 2 s ni autre délai artificiel de collecte n'est ajoutée. Cela ne supprime ni les messages requis, ni la revalidation, ni l'ancienneté des demandes concurrentes de U38. Un taxi peut être dans une opération physique en cours tout en traitant les messages autorisés par son état.

Conserver une séquence de traitement bornée par activation, sans boucle de renégociation infinie au même instant. La demande persistante U43 reste active après un échec et est réexaminée lors des activations suivantes. L'ordre fin des événements et les versions et invalidations des offres doivent être précisés, en cohérence avec L34 à L38. La décision ne fixe ni la résolution temporelle du déplacement ni un temps de calcul réel nul ; ne pas introduire de pause réelle pour simuler la négociation.

### U45. Vitesse de référence de 50 km/h et durée libre fixe par portion

**Origine :** demande utilisateur « simulons un 50km en partant du principe qu'on est en ville, mais avec une duréé fix par case ». Interprétation explicitée dans la réponse : une vitesse de 50 km/h, et non une distance de 50 km.

**Statut : référence retenue pour la cible selon cette interprétation, non implémentée.** Avec U29, une portion routière entre voisines horizontales ou verticales représente 100 m. À 50 km/h, soit 125/9 m/s, sa durée libre vaut exactement 7,2 s. Une route de dix portions prend 72 s hors arrêts et congestion. Cette vitesse est une hypothèse simplifiée uniforme, pas une limite légale vérifiée ni une vitesse moyenne urbaine calibrée.

Interpréter la durée fixe comme une durée de base hors congestion, conformément à U10 : U06 sur les ralentissements reste en vigueur. Une durée strictement fixe même en circulation chargée retirerait l'effet temporel des embouteillages et demanderait une révision explicite de U06. Montées et descentes gardent leurs durées distinctes de 2 s selon U34. Le choix de 50 km/h ne valide pas implicitement une résolution d'une seconde ni l'arrondi systématique de chaque portion à 8 s ; ce dernier ferait tomber la vitesse effective à 45 km/h hors congestion. Le traitement des fractions de seconde et les règles de progression restent ouverts en Q15.

### U46. Adopter la règle de l'équipier interdisant les demi-tours

**Date :** 28 octobre 2026.

**Origine :** demande utilisateur d'adopter la règle de demi-tour de son équipier, avec modification de la documentation uniquement. Source de la règle : cahier d'équipe du 26 octobre, sections 4.3, 5 et 7.

**Statut : confirmé pour la cible, documentation uniquement, non implémenté.** Aucun demi-tour, y compris aux intersections. Chaque taxi possède une orientation logique conservée pendant ses déplacements et ses arrêts. Entre intersections, il poursuit son sens, y compris au départ d'un arrêt ou lorsqu'il redevient disponible. À une intersection, il peut continuer tout droit, tourner à gauche ou tourner à droite si la connexion existe ; il ne peut pas repartir immédiatement dans le sens opposé. Les deux sens d'une rue restent utilisables par des taxis d'orientations adaptées, sans nécessiter une simulation détaillée des voies. Cette adoption ne fixe pas un coût temporel supplémentaire pour tourner.

Un client situé derrière un taxi doit être rejoint par un itinéraire légal, par exemple un tour d'îlot, pas par une inversion instantanée de son orientation. Appliquer les contraintes aux approches, aux trajets à bord, aux insertions et aux estimations de début d'embarquement. L'état utilisé pour trouver un chemin doit distinguer position et orientation ; une distance de Manhattan ou un chemin sans orientation ne suffit pas à garantir une offre réalisable. Ne pas remettre l'orientation à zéro au stationnement. Les orientations initiales devront être légales, reproductibles et conservées dans les scénarios ; le mode de leur génération reste à préciser.

**Conséquence pour la carte U39 :** une simple connexité des cellules routières n'est plus une validation suffisante. Vérifier l'accès aux arrêts et la possibilité de poursuivre légalement depuis les positions et orientations utilisées ; éviter de produire des trajets qui terminent dans un cul-de-sac sans sortie autorisée. Ne pas autoriser un demi-tour exceptionnel pour masquer une carte incompatible. Le détail des contraintes du générateur reste à préciser. Le contrôle des budgets U30 reste obligatoire ; cette règle ne crée pas de crédit de détour supplémentaire. Préciser comment l'orientation de prise en charge intervient dans la référence D0, voir Q17, avant de modifier sa définition.

U46 complète U31, qui interdisait déjà les changements au milieu d'une portion. Elle remplace le statut encore ouvert de l'interdiction aux intersections et son classement antérieur parmi les idées de l'équipier non adoptées. Les décisions antérieures et leur provenance restent conservées. Aucun changement du simulateur ni test d'exécution n'est effectué dans cet échange.

### U47. Relier les axes intérieurs par un cadre routier extérieur

**Date :** 28 octobre 2026.

**Origine :** réponse utilisateur « A » à la comparaison entre un cadre routier extérieur et la suppression des branches en impasse. L'utilisateur demande de poursuivre les choix un par un, avec propositions, recommandation et conséquences.

**Statut : confirmé pour la cible, documentation uniquement, non implémenté.** Compléter les axes orthogonaux de U39 par un cadre routier extérieur à double sens, auquel les routes intérieures se raccordent sans terminer en impasse. Aux quatre coins, le virage à 90° suivant la route est explicitement autorisé ; il ne constitue pas un demi-tour. La carte est finie et non torique : ses bords opposés ne sont pas raccordés.

Le générateur construit le réseau avant de placer les bâtiments. Le routage et les estimations prennent en compte position et orientation du taxi, y compris les contournements par le cadre extérieur. Vérifier que les accès des bâtiments sont atteignables depuis les positions et orientations utilisées et que le taxi peut poursuivre légalement après un arrêt. La présence du cadre ne remplace pas ces contrôles.

**Conséquences :** génération simple et carte lisible, avec une géométrie régulière ; rejoindre un client derrière le taxi peut exiger un tour d'îlot ou un passage par le cadre, donc une approche plus longue. Aucun crédit supplémentaire de détour n'est accordé. Dimensions, espacements, nombre d'axes et bâtiments, génération des orientations initiales et traitement de l'orientation dans D0 restent à préciser. La suppression des branches en impasse, alternative B, n'est pas retenue comme méthode principale.

### U48. Tirer les orientations initiales au hasard parmi les orientations légales

**Date :** 28 octobre 2026.

**Origine :** réponse utilisateur « A » à la comparaison entre tirage aléatoire d'une orientation légale après placement et répartition équilibrée des orientations.

**Statut : confirmé pour la cible, documentation uniquement, non implémenté.** Une fois la position initiale du taxi fixée, tirer son orientation au hasard parmi celles compatibles avec la route. Aux intersections et aux coins, elle doit correspondre à une arrivée possible par une route existante ; les départs respectent ensuite les mouvements autorisés. Sauvegarder position et orientation dans le scénario pour les restituer au rejeu et conserver les mêmes conditions initiales lors des futures comparaisons.

L'orientation est conservée pendant les arrêts et ne change qu'avec les déplacements et virages autorisés. Ne pas la réinitialiser lorsqu'un taxi devient libre. Cette précision complète U46 et U47 ; elle ne modifie pas encore la définition de D0 ni les règles de budget de détour.

**Conséquences :** méthode simple et cohérente avec le placement initial aléatoire, sans stratégie supplémentaire d'équilibrage. Une petite flotte peut présenter un déséquilibre des directions et certaines demandes peuvent être initialement moins bien desservies. La répartition équilibrée, alternative B, n'est pas retenue. Le tirage appartient au scénario ; aucun nouvel aléatoire n'est ajouté pendant les déplacements.

### U49. Une distance de référence fixe par voyage, indépendante du taxi

**Date :** 28 octobre 2026.

**Origine :** réponse utilisateur « A » à la comparaison entre une référence propre au voyage du client et une référence adaptée à l'orientation du taxi proposé.

**Statut : confirmé pour la cible, documentation uniquement, non implémenté.** Fixer D0 comme la longueur du plus court trajet routier légal entre les accès d'origine et de destination, avec la meilleure orientation de départ possible. Calculer cette référence une fois pour la demande et la conserver pendant tout le voyage, identique pour tous les taxis. Les chemins respectent les mouvements autorisés ; la liberté de choisir l'orientation initiale pour ce calcul de référence n'autorise pas un taxi réel à se retourner.

Le budget reste cumulatif selon U30, avec la référence métrique L23 : B = min(0,25 × D0, 400 m). Pour chaque client engagé et le candidat, vérifier distance personnelle déjà parcourue à bord + distance personnelle prévue jusqu'à la destination <= D0 + B. La distance réelle tient compte de l'orientation prévue à la prise en charge puis des mouvements autorisés. Un détour imposé par une mauvaise orientation consomme le budget même sans autre passager. L'approche à vide reste exclue de la distance personnelle à bord et conserve sa protection distincte selon U35.

**Exemple :** D0 = 800 m donne B = 200 m et une limite de 1 000 m. Un taxi proposant 1 200 m à bord à cause de son orientation est inadmissible, même vide. Il peut proposer une autre approche légale permettant une meilleure orientation à la prise en charge, si les autres engagements le permettent, ou refuser la demande. La référence ne passe pas à 1 200 m pour rendre cette offre admissible.

**Conséquences :** référence comparable entre taxis et protection de la distance totale du client, sans crédit implicite lié à l'orientation. L'accessibilité physique seule ne suffit pas à garantir l'admissibilité d'un taxi ; certaines demandes peuvent attendre plus longtemps, sans garantie de service issue de cette règle seule. La référence adaptée au taxi, alternative B, n'est pas retenue. Les contrôles détaillés d'accessibilité de Q17 et les cas d'accès d'origine et de destination identiques restent à préciser.

### U50. Avancer par pas fixes de 0,2 seconde

**Date :** 28 octobre 2026.

**Origine :** réponse utilisateur « A » à la comparaison entre pas fixe de 0,2 s et calendrier d'événements.

**Statut : confirmé pour la cible, documentation uniquement, non implémenté.** L'horloge avance par pas de 0,2 s et utilise un compteur entier de pas ; le temps exprimé en secondes se déduit de ce compteur. Chaque taxi conserve son action, son état et sa progression propres. Un taxi en montée ou descente n'empêche pas les autres de circuler ou de traiter leurs messages. Les demandes actives sont réexaminées à chaque pas selon U43, sans nouvel appel périodique.

Hors congestion, une portion de 100 m à la vitesse de référence de U45 dure 36 pas, soit 7,2 s. Une montée ou descente de U34 dure 10 pas, soit 2 s. Exemple : départ à 0 s, arrivée après une portion libre à 7,2 s, puis fin d'une montée commencée immédiatement à 9,2 s. Dix portions libres consécutives représentent 72 s ; ne pas arrondir chaque portion à une seconde entière.

**Conséquences :** déroulement simple et durées libres représentables exactement en nombres entiers de pas ; cinq fois plus d'instants à traiter qu'avec un pas de 1 s. La congestion peut allonger les déplacements ; leurs fins restent quantifiées aux pas de 0,2 s, avec de petits écarts pouvant s'accumuler. Le compteur entier évite les additions décimales répétées pour l'horloge, sans prétendre supprimer toute approximation du calcul des distances ou vitesses. Le calendrier d'événements, alternative B, n'est pas retenu pour cette version. L'ordre des événements au même instant, les détails de congestion et la représentation des dates d'apparition restent à préciser.

### U51. Ordonner les événements par phases communes, une ronde par pas

**Date :** 28 octobre 2026.

**Origine :** réponse utilisateur « A » à la comparaison entre phases communes et négociation complète par client. La proposition inclut une seule ronde de négociation par pas et le réexamen d'une demande refusée au pas suivant.

**Statut : confirmé pour la cible, documentation uniquement, non implémenté.** À chaque instant t, appliquer l'ordre logique suivant :

1. Terminer les déplacements et opérations arrivés à échéance, puis mettre à jour positions, orientations et états des clients.
2. Faire apparaître les nouvelles demandes dues.
3. Évaluer les demandes actives et transmettre les offres des taxis, sans réserver de place à ce stade.
4. Chaque client compare ses offres admissibles selon U41 et accepte une seule offre.
5. Chaque taxi traite ses acceptations par ancienneté de demande puis identifiant selon U38 ; revalider chaque candidat contre les engagements courants, confirmer ou refuser, et mettre à jour les engagements avant de passer au suivant.
6. Démarrer les prochaines actions physiques possibles, avec déposes avant montées et opérations successives selon U34. Une action en cours se poursuit sans être réinitialisée.
7. Faire progresser les actions pendant l'intervalle de 0,2 s avec la congestion applicable, jusqu'au prochain instant. Les fins dues à cet instant sont traitées à la première phase du prochain pas, sans double progression.

Les phases de négociation ne consomment pas de temps simulé. Des taxis peuvent simultanément poursuivre des déplacements et opérations différents ; l'ordre logique ne constitue pas une attente physique commune. Une seule ronde est autorisée par pas : après un refus, la demande reste active et est réexaminée au pas suivant, 0,2 s plus tard, sans nouveau CFP. Ne pas lancer de boucle de renégociation au même instant.

**Exemple :** à 10 s, un taxi termine sa dernière dépose et un client apparaît. La dépose est finalisée avant l'évaluation des demandes ; le taxi peut donc proposer un service à ce même instant. Si plusieurs clients acceptent ce taxi, une confirmation peut modifier la faisabilité des suivantes ; elles sont revalidées et ne sont pas automatiquement toutes confirmées ou toutes refusées.

**Conséquences :** responsabilités et simultanéités explicites, compatibles avec U38, U43, U44 et U50. Une offre calculée avant les confirmations de la ronde peut devenir inadmissible ; le client refusé attend le prochain pas pour choisir à nouveau. La négociation complète par client, alternative B, n'est pas retenue. Identification, expiration et invalidation des offres, détails des instantanés de congestion et conventions fines d'occupation restent à préciser.

### U52. Limiter la validité des offres à leur ronde

**Date :** 28 octobre 2026.

**Origine :** réponse utilisateur « A » à la comparaison entre offre valable uniquement pendant sa ronde et offre conservée jusqu'à invalidation.

**Statut : confirmé pour la cible, documentation uniquement, non implémenté.** Une offre produite lors d'une ronde peut être acceptée et traitée uniquement pendant cette ronde. À la clôture de la ronde, les offres restantes expirent ; ne pas accepter au pas suivant une ancienne offre. Identifier chaque offre par l'identifiant stable de demande, l'identifiant du taxi et le numéro de ronde. Une acceptation désigne cette offre précise ; une référence à une ancienne ronde ne crée aucun engagement.

Pendant la ronde, chaque client choisit une seule offre selon U41. Le taxi traite les acceptations par ancienneté et identifiant selon U38 et U51, revalide capacité, trajet et protections après chaque confirmation, puis confirme ou refuse. Une offre appartenant à la bonne ronde ne garantit pas sa faisabilité après les confirmations précédentes. Ne pas refuser automatiquement toutes les autres acceptations au seul motif qu'une première réservation a modifié l'itinéraire : les revalider individuellement.

À la clôture, l'expiration concerne les offres, pas les demandes ou engagements. Sans confirmation, la demande reste active pour le prochain pas selon U43 et U51, sans nouveau CFP ni remise à zéro de son ancienneté. Une réservation confirmée reste engagée ; sa demande ouverte est clôturée et les taxis concernés sont notifiés selon U43. Les offres nécessaires sont renouvelées aux rondes suivantes, même si leur contenu change peu.

**Conséquences :** règle simple, cohérente avec une ronde par pas de 0,2 s ; pas de durée d'expiration arbitraire ni de fenêtre de collecte supplémentaire. Renouveler les offres peut accroître le volume de messages et des journaux. L'offre conservée jusqu'à invalidation, alternative B, n'est pas retenue. Le numéro de ronde identifie une proposition et ne représente pas une nouvelle demande ou une nouvelle tentative de CFP. Le format technique des messages sera précisé lors de l'implémentation.

### U53. Mobiliser la place du début de montée à la fin de descente

**Date :** 28 octobre 2026.

**Origine :** réponse utilisateur « A » à la comparaison entre place mobilisée pendant toute l'opération et comptage séparé de la place pendant la montée.

**Statut : confirmé pour la cible, documentation uniquement, non implémenté.** Pour le contrôle de capacité physique, une place devient mobilisée dès le début de la montée et est libérée seulement à la fin de la descente. Conserver les états détaillés du client, notamment en montée, à bord et en descente, afin de ne pas confondre contrôle des places et mesures des durées. La confirmation d'une réservation future ne mobilise pas immédiatement une place physique ; l'occupation prévue reste vérifiée sur les portions concernées selon U25.

Les opérations restent successives, de 2 s chacune, avec déposes avant montées selon U34. Exemple pour un taxi plein de trois places : descente commencée à 10 s, place libérée à 12 s, début immédiat d'une montée mobilisant à nouveau cette place, fin de montée à 14 s. Le taxi repart si aucune autre opération n'est prévue. Selon U51, la fin de descente due à 12 s est finalisée avant les négociations de cet instant et avant le démarrage de la montée.

**Conséquences :** un seul critère de mobilisation des places pendant les opérations, sans risque de réutiliser une place avant la fin de descente ni de considérer libre une place pendant la montée. L'alternative B, occupation comptée seulement après la montée avec blocage séparé pendant celle-ci, n'est pas retenue comme contrôle principal. Les états détaillés sont conservés pour définir ensuite les indicateurs ; cette décision ne fixe pas à elle seule la convention du taux d'occupation ou du temps à bord.

### U54. Ralentir selon la charge de chaque portion dirigée

**Date :** 28 octobre 2026.

**Origine :** réponse utilisateur « A » à la comparaison entre ralentissement par charge avec K = 2 par défaut et entrées limitées avec files d'attente.

**Statut : confirmé pour la cible, documentation uniquement, non implémenté.** Pour chaque portion et chaque sens, compter N taxis en circulation. Leur vitesse commune vaut v = v_libre / max(1, N/K), avec v_libre = 50 km/h selon U45. K est un seuil de fluidité configurable, égal à 2 par défaut, et non une capacité bloquant l'entrée. La formule et son seuil sont des hypothèses de simulation non calibrées sur une rue réelle.

Pour chaque intervalle de 0,2 s, déterminer les taxis déjà présents et les nouvelles entrées sur chaque portion après les choix d'actions de U51, puis calculer la charge et la vitesse communes avant de faire progresser les taxis. Au pas suivant, recalculer en tenant compte des sorties et nouvelles entrées. Ne pas recalculer séquentiellement une vitesse différente pour chaque taxi selon l'ordre d'activation. Une portion en sens opposé possède sa propre charge.

Un taxi vide en approche compte pour un véhicule, comme un taxi occupé, indépendamment du nombre de passagers. Un taxi disponible garé ou effectuant une montée ou descente est hors du flux et ne compte pas. Les 7,2 s par portion constituent la durée libre ; la congestion peut modifier la vitesse pendant une traversée et allonger sa durée réelle.

**Exemple avec K = 2 :** un ou deux taxis sur la portion roulent à 50 km/h ; trois à environ 33,3 km/h ; quatre à 25 km/h. Ces vitesses concernent le prochain pas et ne garantissent pas une charge constante pendant toute la traversée.

**Conséquences :** modèle déterministe simple, sans distances de sécurité, files physiques, conflits de carrefour, feux ou trafic extérieur. L'alternative B, entrées limitées avec files, n'est pas retenue. Les effets observés dépendent de la flotte, de la carte, de la demande et de K ; l'absence de ralentissement reste un résultat possible. La méthode de prévision utilisée dans les offres pour estimer le début de prise en charge selon U41 reste à préciser séparément.

### U55. Estimer les prises en charge à vitesse libre pour rester simple

**Date :** 28 octobre 2026.

**Origine :** réponse utilisateur « A pour rester simple on fera B plus tard si vraiment besoin » à la comparaison entre estimation à vitesse libre et estimation fondée sur la congestion actuellement observée. La recommandation de l'assistant pour B n'est pas retenue pour la version courante.

**Statut : confirmé pour la cible, documentation uniquement, non implémenté.** Chaque taxi calcule la date absolue estimée de début de montée en utilisant 50 km/h pour les déplacements prévus, sans ralentissement de congestion dans cette prévision. Inclure la distance restante sur la portion en cours, le temps restant d'une opération en cours, les déplacements et les opérations déjà engagées avant la prise en charge du candidat. Ne pas inclure les 2 s de montée du candidat lui-même, puisque le critère de U41 porte sur le début de cette montée. Les trajets estimés respectent orientation, engagements et mouvements autorisés.

La simulation physique conserve intégralement le ralentissement U54 et les mises à jour de vitesse tous les 0,2 s. Cette simplification porte sur l'offre, pas sur les déplacements réels. Le classement reste celui de U41 : début de prise en charge estimé, puis score de budget de détour et identifiant. Capacité, distance personnelle maximale et approche protégée restent impératives ; l'estimation n'est pas une garantie d'heure réelle.

**Exemple sans opération préalable :** un taxi à 200 m annonce 14,4 s d'approche, même si sa vitesse réelle est réduite par la congestion ; un taxi à 300 m annonce 21,6 s. Le premier peut donc être choisi alors que le second arriverait réellement plus tôt.

**Conséquences :** calcul simple et indépendant des variations de trafic dans la prévision, avec risque de classement sous-optimal et d'estimations trop optimistes en circulation chargée. L'option B, photographie de la congestion actuelle, est reportée et pourra être discutée seulement si un besoin concret le justifie. Elle n'est ni un travail requis pour la version courante ni une modification déjà autorisée du simulateur.

### U56. Associer un accès routier fixe à chaque bâtiment

**Date :** 28 octobre 2026.

**Origine :** réponse utilisateur « A » à la comparaison entre un accès fixe par bâtiment et plusieurs accès possibles choisis selon l'offre du taxi.

**Statut : confirmé pour la cible, documentation uniquement, non implémenté.** Chaque bâtiment non routier possède un seul accès, constitué d'une cellule routière adjacente admissible. Lors de la génération, choisir cet accès avec un départage déterministe si plusieurs voisins sont possibles, puis le sauvegarder dans le scénario. Toutes les demandes dont ce bâtiment est l'origine ou la destination utilisent ce point routier exact.

Le client attend à l'accès et le taxi reste sur le réseau routier ; aucun trajet piéton vers un autre accès n'est ajouté dans cette convention. Le routage, les offres et la référence D0 de U49 utilisent les accès fixes, tout en respectant l'orientation réelle du taxi pour les trajets proposés. Un autre côté du bâtiment ne devient pas implicitement un accès alternatif permettant d'améliorer une offre.

**Conséquences :** rendez-vous stable, distances et réservations plus simples ; l'accès retenu peut être moins pratique pour un taxi qu'une autre rue voisine. Un accès fixe n'est pas nécessairement exclusif : plusieurs bâtiments peuvent partager la même cellule routière d'accès. Les demandes entre bâtiments partageant cet accès, les critères précis d'accès admissible et les arrêts aux intersections restent à préciser. L'alternative B, plusieurs accès proposés selon le taxi, n'est pas retenue.

### U57. Exclure les demandes entre accès routiers identiques

**Date :** 28 octobre 2026.

**Origine :** réponse utilisateur « A » à la comparaison entre exclusion des demandes entre accès identiques et conservation avec résolution sans taxi.

**Statut : confirmé pour la cible, documentation uniquement, non implémenté.** Chaque demande doit avoir une origine et une destination dont les accès routiers fixes sont distincts. Des bâtiments différents partageant le même accès ne constituent pas une paire de voyage admissible. Appliquer cette validation à la génération et aux scénarios chargés ; signaler une entrée invalide plutôt que créer implicitement un voyage de distance nulle ou un nouveau statut sans taxi.

À la génération, sélectionner une origine disposant de destinations admissibles, puis une destination parmi les bâtiments dont l'accès est différent. Préparer les possibilités admissibles plutôt que répéter des tirages rejetés sans borne. Si la carte ne possède pas au moins deux accès distincts utilisables, signaler une configuration invalide. Les lois de tirage et les contrôles d'accessibilité supplémentaires restent à préciser séparément.

**Conséquences :** chaque demande représente un déplacement routier non nul ; aucun traitement spécial de transport de distance nulle ou de résolution sans taxi n'est ajouté. Plusieurs bâtiments peuvent toujours partager un accès selon U56, mais les voyages entre eux sont exclus. La résolution sans taxi, alternative B, n'est pas retenue. Ce choix ne prouve pas à lui seul qu'un taxi sera admissible au regard de l'orientation et du budget de détour.

### U58. Effectuer les montées et descentes hors des carrefours

**Date :** 28 octobre 2026.

**Origine :** réponse utilisateur « A » à la comparaison entre service hors intersections et autorisation des montées et descentes aux carrefours.

**Statut : confirmé pour la cible, documentation uniquement, non implémenté.** Interdire les montées et descentes sur les cellules de carrefour où au moins trois branches routières se rejoignent. Un accès fixe de bâtiment doit se trouver hors de ces cellules ; appliquer ce filtre lors de la génération et de la validation des accès. Un bâtiment sans autre accès admissible ne peut pas être retenu comme bâtiment desservi. Les taxis peuvent toujours traverser les carrefours et y effectuer leurs virages légaux selon U46.

Les simples virages à deux branches aux coins du cadre extérieur ne sont pas classés comme ces carrefours ; les virages à 90° adoptés en U47 restent autorisés. Cette décision porte sur les montées et descentes, sans ajouter de feux, priorités de carrefour ou files physiques. Un taxi arrêté à un accès admissible reste hors du flux selon U34, et conserve son orientation.

**Conséquences :** séparation des points de service et des croisements, avec un filtre simple sur les accès. Sur le générateur à axes complets, les voisines directes des croisements sont déjà routières et ne peuvent accueillir des bâtiments ; la restriction devrait donc peu contraindre ce placement, tout en fournissant une règle explicite pour la validation. L'alternative B, opérations aux carrefours, n'est pas retenue.

### U59. Une carte par défaut de 21 × 21 cellules avec cinq axes par direction

**Date :** 28 octobre 2026.

**Origine :** réponse utilisateur « A » à la comparaison entre carte intermédiaire de 21 × 21 avec cinq axes par direction et petite carte de 11 × 11 avec quatre axes. La proposition inclut des axes intérieurs aléatoires sauvegardés et un espacement minimal de deux cellules entre axes parallèles.

**Statut : confirmé pour la cible, documentation uniquement, non implémenté.** Retenir par défaut 21 × 21 cellules, avec cinq axes horizontaux et cinq verticaux à double sens. Dans chaque direction, deux axes constituent les bords du cadre et trois sont intérieurs. Les axes extérieurs passent par les premières et dernières lignes ou colonnes ; les positions intérieures sont tirées au hasard et sauvegardées. Espacer les axes parallèles d'au moins deux cellules, soit 200 m entre centres, y compris par rapport aux axes du cadre. Conserver dimensions et nombres d'axes comme paramètres configurables et valider leur compatibilité avec cet espacement.

Le réseau forme seize îlots, dont les dimensions peuvent varier avec les positions tirées. Avec l'échelle de U29, les centres des axes extérieurs opposés sont distants de 2 000 m. Un côté du cadre comporte vingt portions et prend 144 s à vitesse libre de référence, hors arrêts et congestion. Cette distance entre centres ne désigne pas la largeur bord à bord des vingt et une cellules.

**Conséquences :** davantage de variété spatiale et de contournements qu'avec la petite carte ; déplacements plus longs et dispersion potentiellement accrue à flotte identique, sans garantie de partage ou congestion. Les nombres de bâtiments, taxis et demandes restent à définir. La carte de 11 × 11 à quatre axes, alternative B, n'est pas la valeur par défaut, mais le paramétrage doit permettre d'autres configurations valides.

Le choix de 21 × 21 ne transforme pas le réseau routier complet utilisé pour le calcul illustratif L23 en carte cible : notre réseau n'utilise que cinq lignes et cinq colonnes routières. Ne pas réutiliser sa moyenne de 1 400 m comme mesure de cette nouvelle carte. Le plafond de détour de référence de 400 m reste celui de L23, sans recalibrage implicite.

### U60. Placer trente-deux bâtiments par tirage uniforme sans remise

**Date :** 28 octobre 2026.

**Origine :** réponse utilisateur « A » à la comparaison entre 32 bâtiments tirés parmi tous les emplacements admissibles et 32 bâtiments avec au moins un bâtiment dans chaque îlot.

**Statut : confirmé pour la cible, documentation uniquement, non implémenté.** Retenir 32 bâtiments par défaut, avec nombre configurable. Après construction du réseau, lister les cellules non routières possédant au moins un accès routier adjacent admissible hors carrefour selon U56 et U58. Tirer uniformément les cellules retenues sans remise : au maximum un bâtiment par cellule, sans imposer de quota ou de minimum par îlot.

Associer ensuite à chaque bâtiment son accès fixe selon le départage déterministe U56, puis sauvegarder positions et accès dans le scénario. Les bâtiments restent fixes pendant la simulation. Plusieurs bâtiments peuvent partager un accès, mais les demandes doivent avoir des accès d'origine et de destination distincts selon U57. Si le nombre demandé dépasse les emplacements admissibles, signaler une configuration invalide plutôt que réduire ce nombre ou multiplier les tirages rejetés.

**Conséquences :** placement simple, sans stratégie d'équilibrage. Les îlots proposant davantage d'emplacements admissibles sont davantage représentés en moyenne ; certains îlots peuvent rester sans bâtiment. Avec 32 bâtiments pour les 16 îlots de U59, la moyenne globale vaut deux bâtiments par îlot, sans répartition locale garantie. L'alternative B, garantie d'un bâtiment par îlot avant complément, n'est pas retenue. Les nombres de taxis et demandes ainsi que leurs lois de tirage restent à préciser.

### U61. Huit taxis et soixante demandes uniformes sur trois cents secondes

**Date :** 28 octobre 2026.

**Origine :** réponse utilisateur « B » à la comparaison entre 8 taxis avec 30 demandes et 8 taxis avec 60 demandes, sur une fenêtre commune de 0 à 300 s. Les deux propositions fixent le total par paramètre et tirent les horaires indépendamment et uniformément sur les pas de 0,2 s.

**Statut : confirmé pour la cible, documentation uniquement, non implémenté.** Retenir par défaut 8 taxis et 60 demandes, avec une fenêtre d'apparition de 0 à 300 s. Conserver ces valeurs comme paramètres configurables. Le nombre total de clients est fixé par la configuration, sans tirage supplémentaire de ce total. Chaque demande représente un passager selon les règles de capacité existantes.

Tirer indépendamment les horaires parmi les instants représentables par le pas U50, uniformément de 0 à 300 s inclus, soit les numéros de pas 0 à 1 500. Plusieurs demandes peuvent apparaître au même instant. Générer et sauvegarder ces horaires avant l'exécution ; les taxis ne reçoivent connaissance d'une demande qu'à son apparition, sans accès aux demandes futures. Le rythme moyen de 60 demandes sur 300 s correspond à une demande toutes les 5 s en moyenne, sans espacement régulier imposé.

À la fin de la fenêtre, poursuivre les livraisons selon U12 et U33 ; 300 s n'est ni une fin normale automatique ni une durée de journée réelle calibrée. Une interruption technique reste incomplète. Les lois spatiales des origines et destinations et des positions initiales des taxis restent à préciser.

**Conséquences :** charge de demande plus élevée que l'alternative A à flotte identique ; davantage de messages et de calculs, avec attentes, partage et congestion potentiellement accrus mais sans garantie avant exécution. La configuration A de 30 demandes n'est pas le défaut retenu, tout en restant possible par paramétrage. Aucun essai comparatif n'est exécuté ou imposé par cette décision.

### U62. Tirer les origines et destinations par bâtiment

**Date :** 28 octobre 2026.

**Origine :** réponse utilisateur « A » à la comparaison entre tirage parmi les bâtiments et tirage uniforme parmi les accès routiers distincts.

**Statut : confirmé pour la cible, documentation uniquement, non implémenté.** Pour chaque demande, choisir uniformément le bâtiment d'origine parmi les bâtiments desservis, puis choisir uniformément la destination parmi les bâtiments dont l'accès fixe est différent. Préparer ces destinations admissibles selon U57, sans boucle de rejets. Sauvegarder les identifiants des bâtiments et leurs accès dans le scénario.

Les tirages sont indépendants entre demandes et indépendants des horaires de U61. Plusieurs clients peuvent demander le même voyage, y compris au même instant ; ne pas éliminer ces répétitions. Chaque bâtiment possède la même probabilité d'être une origine. Cette règle ne signifie pas que toutes les paires admissibles ont la même probabilité : le nombre de destinations admissibles peut varier selon le nombre de bâtiments partageant l'accès d'origine.

**Conséquences :** méthode simple qui fait des bâtiments les lieux de référence, avec attractivité individuelle identique sans catégorie logement, commerce ou bureau. Un accès desservant plusieurs bâtiments contribue davantage aux origines en moyenne. Exemple : avec trois bâtiments à un accès et un bâtiment à l'autre, les probabilités d'origine par accès sont respectivement 75 % et 25 %. L'alternative B, accès équiprobables puis choix du bâtiment associé, n'est pas retenue. Les positions initiales des taxis restent à définir.

### U63. Répartir initialement les taxis sur le réseau routier hors carrefours

**Date :** 28 octobre 2026.

**Origine :** réponse utilisateur « A » à la comparaison entre placement routier hors carrefours et placement uniquement aux accès des bâtiments. Les deux propositions utilisent un tirage sans remise pour les positions initiales.

**Statut : confirmé pour la cible, documentation uniquement, non implémenté.** Les taxis commencent libres, sans passager ni réservation, garés hors du flux. Tirer uniformément leurs positions initiales parmi les cellules routières hors carrefours d'au moins trois branches, cadre extérieur compris. Utiliser un tirage sans remise : huit positions distinctes pour les huit taxis par défaut. Cette restriction concerne uniquement le placement initial, sans ajouter une capacité physique par cellule pendant la simulation.

Après les positions, tirer pour chaque taxi une orientation légale selon U48, puis sauvegarder positions et orientations dans le scénario. Le placement ne consulte pas les futures demandes pour améliorer la disponibilité initiale. Vérifier que la configuration contient suffisamment de cellules admissibles et des orientations légales ; signaler une configuration invalide sinon.

**Conséquences :** placement simple sans stratégie de rapprochement des bâtiments ; des taxis peuvent commencer loin des clients, notamment sur le cadre extérieur, et effectuer de longues approches. L'alternative B, placement uniquement aux accès des bâtiments, n'est pas retenue. Les taxis restent garés jusqu'à un engagement selon U40, puis suivent les trajets légaux et la congestion réelle.

### U64. Séparer les tirages de carte, flotte, voyages et horaires

**Date :** 28 octobre 2026.

**Origine :** réponse utilisateur « A » à la comparaison entre quatre suites de tirages séparées et un générateur unique pour tous les composants.

**Statut : confirmé pour la cible, documentation uniquement, non implémenté.** À partir d'une graine principale, dériver de manière stable quatre suites pseudo-aléatoires distinctes : carte et bâtiments ; positions et orientations de flotte ; origines et destinations des voyages ; horaires d'apparition. Les composants utilisent uniquement la suite qui leur est attribuée, sans couplage implicite par l'ordre global des tirages. Sauvegarder les données complètes du scénario et les informations de graine nécessaires à la traçabilité.

**Exemple :** conserver la même graine et les paramètres de carte et demande en passant de huit à douze taxis ne doit pas décaler les tirages de carte, voyages ou horaires. Cela ne garantit pas que les positions des huit premiers taxis soient identiques entre deux tailles de flotte : cette propriété dépend du procédé d'échantillonnage et n'est pas ajoutée ici.

Les déplacements, opérations et négociations n'introduisent aucun nouvel aléatoire. La séparation des suites n'autorise pas d'autres types de tirages que ceux déjà retenus. Le choix d'API et de dérivation doit être vérifié avec les outils disponibles selon U16 lors de l'implémentation.

**Conséquences :** isolation des composants facilitant vérifications et futures expériences, au prix de quatre générateurs à gérer. Le JSON complet reste la référence pour rejouer les entrées : la graine seule ne suffit pas à retrouver une ancienne génération après changement d'algorithme. L'alternative B, générateur unique, n'est pas retenue. La conservation de la version du code et de l'environnement lors des comparaisons entre versions reste à préciser en Q09.

### U65. Détecter l'état figé et terminer avec un diagnostic incomplet

**Date :** 28 octobre 2026.

**Origine :** réponse utilisateur « A » à la comparaison entre détection de l'état figé et poursuite des réexamens jusqu'au plafond technique.

**Statut : confirmé pour la cible, documentation uniquement, non implémenté.** Après une évaluation complète des demandes actives, arrêter techniquement avec statut incomplet lorsque toutes les conditions suivantes sont réunies : aucune demande future, tous les taxis libres et garés sans action ni engagement en cours, au moins un client encore en attente, et aucune offre admissible. Il n'existe alors plus d'événement interne prévu susceptible de changer la situation selon les règles retenues.

Conserver l'heure d'arrêt, les clients non servis et les motifs disponibles d'absence d'offre ou de refus. Le contrôle relève de l'observation globale du modèle et ne donne pas aux agents accès aux demandes futures. Une absence momentanée d'offre ne suffit pas : ne pas arrêter sur ce critère tant qu'une course ou opération est en cours, qu'une demande future doit apparaître ou qu'une offre admissible existe.

**Exemple :** à 340 s, 59 clients sur 60 sont livrés et les huit taxis sont libres, mais aucun ne peut proposer de course admissible au dernier client. Terminer incomplet avec ce client identifié, plutôt que répéter indéfiniment la même évaluation. Ce diagnostic caractérise le blocage de la politique depuis l'état courant et ne prouve pas une impossibilité pour toute autre politique.

**Conséquences :** calculs inutiles évités et diagnostic explicite, avec un contrôle supplémentaire de l'état global. Les demandes restantes ne deviennent ni abandonnées ni livrées. Ne pas ajouter repositionnement automatique, demi-tour exceptionnel ou dépassement de budget pour transformer cette interruption en réussite. L'alternative B, attendre seulement le plafond technique, n'est pas retenue comme réponse à cet état figé. Cette décision n'enlève pas un éventuel plafond général de sécurité et n'en fixe pas la valeur.

### U66. Conserver un résumé global et les mesures individuelles

**Date :** 28 octobre 2026.

**Origine :** réponse utilisateur « A » à la comparaison entre résumé global avec détails individuels et résumé global seul. La proposition explicite les champs et conventions temporelles ci-dessous.

**Statut : confirmé pour la cible, documentation uniquement, non implémenté.** Conserver un résumé de l'exécution et une ligne par client et par taxi, soit 60 lignes clients et huit lignes taxis pour la configuration par défaut. Pour chaque client, conserver état final, taxi attribué, dates de demande et confirmation, débuts et fins de montée et descente, distance de référence D0, distance réellement parcourue à bord et détour. Pour chaque taxi, conserver distances totale, à vide et partagée, nombre de clients livrés, temps de circulation, d'opérations et à l'état libre.

Le résumé comprend notamment nombres de clients livrés et non livrés, attente moyenne, temps total moyen et distances cumulées. Les détails individuels servent à expliquer les moyennes et à vérifier les budgets de détour ; ils ne remplacent pas le statut complet ou incomplet de l'exécution.

**Conventions temporelles :** attente = début de montée moins date de demande ; temps à bord = début de descente moins fin de montée ; durées de montée et descente propres au client conservées séparément ; temps total = fin de descente moins date de demande. Les opérations pour d'autres clients survenant entre ces bornes restent incluses dans son temps à bord. Exemple : demande à 10 s, montée de 30 à 32 s, descente de 70 à 72 s donnent attente 20 s, temps à bord 38 s, opérations propres 4 s, total 62 s.

En exécution incomplète, laisser absentes les dates encore inconnues, sans les remplacer par zéro ni une fausse heure de livraison. Les moyennes de voyages terminés portent uniquement sur les clients livrés, avec l'effectif indiqué et les autres clients recensés séparément. Une population vide ne produit pas de moyenne définie ; une distance effectivement mesurée nulle reste une valeur valide.

**Conséquences :** données individuelles peu volumineuses pour la configuration retenue et utiles à l'analyse et au diagnostic. L'alternative B, résumé seul, n'est pas retenue. Cette décision n'impose pas un journal complet à chaque pas. Les conventions précises des indicateurs de partage, de l'occupation et de la séparation entre retard de congestion et quantification numérique devront rester explicites lors de leur formalisation, sans modifier les règles métier déjà adoptées.

### U67. Vérifier l'accessibilité de toute la carte avec les orientations

**Date :** 28 octobre 2026.

**Origine :** réponse utilisateur « A » à la comparaison entre validation de toute la carte orientée et vérification limitée aux positions initiales et paires origine-destination du scénario.

**Statut : confirmé pour la cible, documentation uniquement, non implémenté.** Avant lancement, depuis chaque position et orientation légales du réseau, vérifier que tous les accès de bâtiments sont atteignables en respectant les mouvements autorisés et qu'un taxi peut poursuivre légalement après un arrêt. La destination est le point d'accès ; ne pas exiger arbitrairement toutes les orientations d'arrivée possibles à cet accès. L'état de routage distingue position et orientation conformément à U46, avec virages du cadre selon U47.

La validation est indépendante des seules demandes et positions de flotte tirées : elle doit également couvrir des états atteints après d'autres courses ou insertions. Une simple connexité géométrique ou l'existence d'un trajet initial ne suffit pas. Appliquer les contraintes d'accès déjà retenues, notamment hors carrefour selon U58. Si la carte ne satisfait pas cette garantie, la refuser avec un diagnostic avant exécution, sans autoriser un demi-tour exceptionnel pour la réparer implicitement.

**Conséquences :** contrôle de préparation plus large mais adapté à notre petit réseau et utile pour rejouer la carte avec d'autres demandes. Cette validation garantit la circulation et la poursuite légale, pas la faisabilité de chaque course avec tous les engagements et budgets de distance. Un trajet légal peut dépasser la limite de U49 ; la détection de blocage U65 reste donc nécessaire. L'alternative B, validation limitée au scénario préparé, n'est pas retenue.

### U68. Mesurer les distances des taxis par nombre effectif de passagers

**Date :** 28 octobre 2026.

**Origine :** demande utilisateur « Je veux A mais aussi savoir combien de ces mètre sont à deux passagers, combien à 3, etc » après comparaison entre mètres de taxi et mètres-passagers comme mesure principale du partage.

**Statut : confirmé pour la cible, documentation uniquement, non implémenté.** Retenir les mètres réellement parcourus par les taxis comme unité principale de distance partagée. Pour chaque déplacement, attribuer sa distance à la catégorie correspondant au nombre effectif de passagers simultanément à bord : zéro, un, deux, trois ou quatre selon la capacité configurée. Chaque mètre est compté une seule fois dans une seule catégorie, sans multiplication par le nombre de passagers. Conserver cette décomposition par taxi et dans le résumé de flotte.

Nommer explicitement les mesures, par exemple distance_empty_m, distance_with_1_passenger_m, distance_with_2_passengers_m, distance_with_3_passengers_m et distance_with_4_passengers_m, selon la capacité. Éviter le nom isolé D0 pour la distance à vide : U49 utilise déjà D0 pour la référence personnelle d'un voyage. Les états de montée et descente de U53 n'ajoutent aucune distance lorsque le taxi est arrêté ; des réservations futures ne comptent pas comme des personnes transportées.

Distance totale = somme des catégories de zéro à la capacité. Distance partagée = somme des catégories à partir de deux passagers. Si la distance totale est non nulle, taux de distance partagée = distance partagée / distance totale, déplacements à vide compris. Une catégorie sans distance effectivement parcourue vaut zéro ; un pourcentage dont le dénominateur est nul reste absent. Pour la flotte, sommer les distances avant de calculer les pourcentages, plutôt que faire une moyenne non pondérée des pourcentages des taxis.

**Exemple fictif, capacité trois :** 300 m à vide, 400 m avec une personne, 200 m avec deux et 100 m avec trois donnent 1 000 m au total, dont 300 m partagés, soit 30 %. Le détail distingue 200 m à deux et 100 m à trois. La catégorie quatre est utilisée lorsque la capacité configurée le permet.

**Conséquences :** la mesure principale reste reliée à l'activité des véhicules tout en distinguant l'intensité d'occupation. Le comptage en mètres-passagers, alternative B, n'est pas retenu comme mesure principale. Le taux ne démontre pas à lui seul une économie de distance ; une comparaison requiert toujours des scénarios et références appropriés.

### U69. Adapter l'interface locale existante à une seule simulation

**Date :** 28 octobre 2026.

**Origine :** « Je valide tes trois recommandations », après la recommandation A pour l'interface locale plutôt qu'une interface web.

**Statut : confirmé pour la cible, documentation uniquement, non implémenté.** Adapter l'interface locale existante au monde unique de U21, avec carte, orientations, commandes et indicateurs. L'interface existante est décrite dans le guide comme utilisant Tkinter et Matplotlib ; aucune nouvelle plateforme web n'est adoptée pour cette version. Ce choix fixe la cible d'utilisation, sans imposer de conserver un composant interne dont la réécriture serait plus simple selon U20.

**Conséquences :** limiter les dépendances et le travail d'interface supplémentaire, tout en adaptant le rendu à la carte générée et aux états de la nouvelle simulation. Les détails de disposition et les outils Mesa compatibles doivent être examinés lors de la préparation technique selon U16. Cette validation ne constitue pas une demande de commencer à coder.

### U70. Conserver un plafond technique configurable de durée simulée

**Date :** 28 octobre 2026.

**Origine :** même validation des trois recommandations, dont A pour le plafond technique en complément de la détection d'état figé.

**Statut : confirmé pour la cible, documentation uniquement, non implémenté.** Conserver un plafond configurable de durée simulée, distinct de la fenêtre d'apparition des demandes et du critère d'état figé U65. Si l'exécution atteint cette limite sans satisfaire la fin normale, arrêter avec statut incomplet, y compris si des courses étaient encore en cours. Conserver l'heure, la cause de l'arrêt, les états et les données partielles des clients et taxis selon U66.

**Conséquences :** couvrir également une exécution qui ne se termine pas alors que certains taxis restent actifs, sans déclarer ses passagers livrés ou abandonnés. Une limite trop courte peut interrompre une exécution valide ; aucune valeur numérique définitive n'est choisie dans cet échange. La valeur par défaut sera déterminée puis ajustée à partir des premiers essais. La détection d'état figé reste active indépendamment du plafond.

### U71. Mesurer l'activité et les distances sans modèle d'émissions

**Date :** 28 octobre 2026.

**Origine :** même validation des trois recommandations, dont A pour les distances et l'activité sans calcul d'émissions.

**Statut : confirmé pour la version cible courante, documentation uniquement, non implémenté.** Conserver les mesures de distance, occupation, temps et congestion déjà retenues, sans ajouter de modèle d'émissions ni de conversion en CO2. Les kilomètres parcourus mesurent une activité de transport et ne sont pas présentés comme une quantité de pollution. La décomposition par nombre effectif de passagers de U68 reste conservée.

**Conséquences :** modèle plus simple, sans coefficients d'émissions ni données de flotte supplémentaires. Les conclusions pourront porter sur distances et temps ; elles ne pourront pas annoncer de réduction chiffrée d'émissions à partir de ces seules mesures. Un modèle d'émissions serait une extension distincte à définir et justifier ultérieurement.

## 3. Évolution des décisions

Les étapes ci-dessous suivent l'ordre de la conversation. Aucune date précise n'est reconstruite pour les messages qui n'en portent pas.

| Sujet | Ancienne idée | État courant | Provenance |
| --- | --- | --- | --- |
| Périmètre | Démonstration centrée sur individuel et partage compatible | Base initiale conservée ; objectif final élargi, notamment aux détours | U01 à U03 précisés par U14 |
| Durées | Plages aléatoires, par exemple embarquer entre 1 et 3 s | Durées fixes ; embarquer prend 2 s | Remplacement explicite par l'utilisateur, U10 |
| Demandes à 0 s | Tous les passagers apparaissent au début, proposition de l'assistant | Apparitions échelonnées et aléatoires d'un ensemble fini | Correction explicite par l'utilisateur, U11 |
| Arrêt | Formulations « répondu » ou « résolu » | Dernière descente terminée et plus aucune demande future | Objectif U12, interprétation L15 |
| Congestion | Charge d'une portion sans précision suffisante sur le sens | Charge par portion dirigée | Précision utilisateur U07, mécanisme L12 |
| Durée routière | Durée figée à l'entrée proposée dans une première explication | Vitesse recalculée chaque seconde pendant la traversée | Révision de l'assistant, L12 |
| Messagerie | Livraison au tour suivant proposée dans le canevas historique | Échanges par phases au même instant simulé | Choix d'implémentation de l'assistant, L09 |
| Ville | Carte routière fixe 11 × 9, L03 | Démonstration actuelle conservée ; objectif de génération automatique simple | U15, non implémenté |

Ne pas réintroduire les durées aléatoires ou toutes les demandes à 0 seconde en lisant une ancienne explication. Ces deux points ont été remplacés par des demandes plus récentes de l'utilisateur.

## 4. Choix proposés ou ajoutés par le LLM

**Statut des sections 4.1 à 4.4 : implémentés, mais pas tous confirmés individuellement par l'utilisateur.** Ils constituent les conventions de la version actuelle. Les sections suivantes précisent individuellement le statut des propositions et décisions pour la réécriture. Leur présence dans cette section n'autorise pas à modifier spontanément le programme : rester dans le périmètre du travail demandé.

### 4.1 Reproductibilité, carte et architecture

| ID | Choix et localisation | Justification et conséquence |
| --- | --- | --- |
| L01 | Scénario complet sauvegardé en JSON, empreinte SHA-256 et deux flux aléatoires locaux séparés pour flotte et demandes, dans [scenario.py](../taxishare/scenario.py) | Rend les entrées identiques entre modes ; changer le nombre de taxis ne décale pas les tirages de demandes. L'empreinte identifie les données du scénario, pas la version du code. |
| L02 | Origines/destinations tirées parmi les bâtiments ; heures entières uniformes dans une fenêtre inclusive ; total de demandes configuré | Donne un générateur simple et rejouable. Ne représente ni heure de pointe ni demande issue de données réelles. Les futurs passagers ne sont créés qu'à l'apparition de leur demande. |
| L03 | `MultiGrid` non torique ; carte 11 × 9, trois axes verticaux, deux horizontaux et onze bâtiments ; chemins par recherche en largeur, ordre est/nord/ouest/sud | Suit la recommandation du cours et donne un réseau connecté avec des chemins déterministes. La géométrie et les constantes sont des exemples de modèle. Voir [city.py](../taxishare/city.py). |
| L04 | Agents `Passenger` et `Taxi` ; services `City`, `DemandScheduler`, `MessageBus`, `Traffic`, `Metrics` ; coordination et horloge dans `TaxiModel` | Répond à U08 en répartissant les responsabilités. L'horloge reste un attribut du modèle, pas un service autonome. Les bâtiments sont passifs, les passagers à bord restent agents Mesa mais quittent la grille. |

### 4.2 Transport et choix des offres

| ID | Choix et localisation | Justification et conséquence |
| --- | --- | --- |
| L05 | Deux places physiques ; limite d'un engagement en individuel et deux en partagé ; réservations incluses | Simplifie le contrôle des capacités. La limite de deux personnes est un choix de première version. La réservation d'une place future reste conservative et peut limiter les regroupements. |
| L06 | Premier engagement fixe le trajet ; origine puis destination sur le trajet restant ; même origine avec destination intermédiaire autorisée | Formalise U03 sans détour. Un point déjà quitté est exclu, même si le taxi n'a pas encore terminé sa portion. Le trajet reste fixe même en cas de congestion. |
| L07 | Aucun second engagement pendant l'approche du premier passager ; taxi libre immobile ; ni marche ni attente volontaire pour constituer un groupe | Réduit les cas de coordination. Peut manquer des occasions de partage et influencer l'attente. Une fois arrivé à l'origine du premier passager, le taxi peut proposer le partage. |
| L08 | Choix de l'offre par heure estimée de fin d'embarquement, puis numéro du taxi ; acceptations par ancienneté de demande puis identifiant | Donne des règles reproductibles. L'estimation utilise les vitesses disponibles lors de l'offre, celles du dernier intervalle connu, et n'anticipe pas les futures arrivées. La politique est gloutonne, sans affectation optimale globale. |
| L09 | `CFP`, `OFFER`, `ACCEPT`, `CONFIRM`, `REJECT` et notifications de transport ; échanges de durée simulée nulle dans des phases ordonnées | Une offre ne réserve pas une place ; le taxi revalide lors de l'acceptation. Les offres valent pour cette phase seulement. Après refus ou absence d'offre, une nouvelle demande peut être émise la seconde suivante. Voir [messaging.py](../taxishare/messaging.py) et `taxishare/agents.py` (ancien module ; voir [Passenger](../taxishare/passenger.py) et [Taxi](../taxishare/taxi.py) dans le code actuel). |

### 4.3 Temps, circulation et arrêt

| ID | Choix et localisation | Justification et conséquence |
| --- | --- | --- |
| L10 | Résolution d'une seconde ; actions sur plusieurs secondes ; embarquements et descentes successifs ; déposes avant prises en charge | Répond à U09 avec une exécution lisible. Deux embarquements prennent quatre secondes. Les autres taxis continuent pendant un arrêt. Voir `prepare_action()` et `advance_stop()`. |
| L11 | Bâtiment associé à un accès routier ; passager déjà présent à cet accès ; taxi arrêté supposé garé hors circulation | Évite de simuler la marche et les arrêts bloquants. « Même origine/destination » s'évalue sur les accès routiers. Le taxi n'entre jamais dans le bâtiment. |
| L12 | Charge N/K par portion dirigée ; vitesse = vitesse libre / max(1, N/K), recalculée chaque seconde ; seuil non bloquant | Réalise U06 et U07 par un ralentissement déterministe. Les nouvelles entrées sont incluses dans l'instantané commun ; les sorties influencent l'intervalle suivant. Un taxi compte pour un véhicule, quelle que soit son occupation. Voir [traffic.py](../taxishare/traffic.py). |
| L13 | Aucun trafic extérieur, feu, conflit d'intersection ou file physique ; sens opposés indépendants | La première version mesure uniquement le ralentissement dû aux taxis sur leurs portions dirigées. Deux mouvements différents ne se bloquent pas au carrefour. Ce choix limite le réalisme du terme « embouteillage ». |
| L14 | Progression continue en mètres sur une portion, arrivée sur la grille à la fin ; un reliquat de trajet consomme une seconde entière | Permet des vitesses non entières avec une horloge simple. Une seconde partiellement utilisée n'est pas reportée sur la portion suivante. L'affichage interpole la position ; la position `MultiGrid` reste au départ jusqu'à l'arrivée. |
| L15 | Résolution d'une demande à la fin de la descente ; pas d'annulation ni abandon ; plafond technique provoquant une erreur | Donne un critère de fin vérifiable à U12. Une exécution interrompue au plafond ne constitue pas une réussite. Une liste vide termine à 0 seconde. Voir [model.py](../taxishare/model.py). |

### 4.4 Outils, mesures et vérification

| ID | Choix et localisation | Justification et conséquence |
| --- | --- | --- |
| L16 | Python 3.10 et Mesa 3.0.3 retenus lors de l'implémentation ; Matplotlib 3.10.8 ; environnement `.venv` réutilisant les paquets installés | Évite une installation supplémentaire dans l'environnement disponible à ce moment. Les dépendances de référence sont inscrites dans [requirements.txt](../requirements.txt). Ce choix n'était pas une version imposée par l'utilisateur ou le cours. |
| L17 | Interface locale Tkinter/Matplotlib avec deux cartes ; exécution automatique séparée | Fournit une visualisation sans ajouter Solara à l'environnement initial. Voir [app.py](../app.py), [visualization.py](../taxishare/visualization.py) et [run_experiments.py](../run_experiments.py). |
| L18 | CSV/JSON/PNG, distances à vide incluses, mesures par passager et sommes flottantes stables via `fsum` | Facilite l'analyse et évite des écarts d'agrégation dus à l'ordre des taxis. Le retard de congestion distingue ralentissement et arrondi temporel. Voir [metrics.py](../taxishare/metrics.py) et la section 5. |
| L19 | Invariants pendant les simulations et tests `unittest` déterministes | Contrôle capacité, affectation unique, positions et chronologie. Les tests ne démontrent pas le réalisme du modèle. Les résultats d'une seule seed ne justifient pas une conclusion générale. |

### 4.5 Proposition de génération à examiner

**L20, statut proposé, non implémenté :** générer un réseau simple en sélectionnant des lignes et colonnes routières qui se croisent, puis placer les bâtiments sur des cellules adjacentes avec un accès routier. Cette piste vise un réseau connecté par construction ; vérifier que la taille et les tirages permettent de placer les bâtiments et des origines/destinations distinctes.

Employer une graine de carte distincte des tirages de flotte et de demandes pour pouvoir faire varier un facteur sans décaler les autres. Sauvegarder la géométrie réalisée et ses paramètres dans le scénario. Examiner d'abord les outils Mesa disponibles conformément à U16 ; ne pas attribuer à Mesa un générateur urbain sans vérification. Cette piste est une proposition de l'assistant, pas l'algorithme choisi par l'utilisateur.

### 4.6 Propositions de conception pour la réécriture, non implémentées

**L21, proposé puis confirmé dans son principe de calcul par U30 le 27 octobre 2026 : budget cumulatif de distance.** Pour chaque passager, fixer D0 comme la longueur d'un plus court trajet routier autorisé entre son origine et sa destination, indépendamment de la congestion. La proposition initiale était B = min(0,25 × D0, 500 m). Le plafond de référence est ensuite adapté à 400 m en L23, avec taux et plafond configurables, identiques pour tous dans un premier modèle. Les valeurs sont des hypothèses de départ non calibrées. Le plafond ne constitue pas un minimum accordé aux petits trajets.

Avant confirmation d'une nouvelle réservation, vérifier pour chaque client engagé et pour le candidat : distance personnelle déjà parcourue à bord + distance personnelle prévue jusqu'à sa destination <= D0 + B. Pour un client non embarqué, seule la distance prévue à bord intervient ; l'approche du taxi n'appartient pas à son trajet à bord. Inclure toutes les insertions antérieures, sans réinitialiser D0 ou B. Le taxi conserve donc un budget pour chaque passager, pas un budget global du véhicule. Exemples historiques avec le plafond initial de 500 m : D0 de 200 m donne B de 50 m ; 1 000 m donne 250 m ; 4 000 m donne 500 m. Avec le plafond adapté de L23, ce dernier budget devient 400 m.

Cette règle protège la distance, pas le temps. Un arrêt sur le trajet peut ajouter de l'attente sans détour. Une limite temporelle d'attente et, si nécessaire, une limite d'arrêts intermédiaires doivent être discutées séparément. Les trajets de distance nulle et les conditions d'accessibilité restent à préciser.

**L22, proposé puis confirmé par U31 le 27 octobre 2026 : décisions immédiates, effets physiques aux points autorisés.** Recalculer et confirmer les futurs arrêts dès réception d'une demande, sans attendre la fin de la course. Conserver toutefois la progression déjà effectuée et terminer la portion jusqu'au prochain point d'arrêt ou de bifurcation autorisé avant une prise en charge ou un changement de direction. Ne pas assimiler cette portion à la course entière. L'alternative d'arrêts ou demi-tours au milieu d'une portion a été écartée par l'utilisateur pour la cible.

### 4.7 Échelle de distance et nouvelles questions du 27 octobre 2026

**L23, choix de référence de l'assistant en réponse à U30, non implémenté : plafond de détour adapté à 400 m.** Exemple de calcul simplifié : réseau carré orthogonal complet de 21 × 21 points routiers espacés de 100 m, sans bord raccordé et sans diagonale. Toutes les 194 040 paires ordonnées de points distincts sont équiprobables. Une énumération JavaScript en mémoire donne une distance moyenne de 1 400 m, une médiane de 1 300 m et un 90e percentile de 2 300 m. Ce calcul ne constitue ni un scénario de simulation ni une décision sur la carte finale ; bâtiments et profils de demande ne sont pas représentés.

Retenir B = min(0,25 × D0, 400 m) comme référence : budget de 100 m pour 400 m directs, 200 m pour 800 m, 350 m pour le trajet moyen de 1 400 m, puis plafond de 400 m à partir de 1 600 m. Ne pas arrondir les budgets vers le haut. Sur ce réseau, les longueurs entre deux points fixes ont la même parité en nombre de portions : un trajet plus long ajoute au moins deux portions, soit 200 m. Par conséquent, les voyages de moins de 800 m n'autorisent aucun détour spatial positif, mais peuvent partager leur chemin avec des arrêts supplémentaires. Le budget de 350 m d'un trajet direct de 1 400 m autorise en pratique 200 m de supplément sur cet exemple. Cette conséquence est explicitée à l'utilisateur ; réexaminer la sensibilité après choix du réseau et des demandes, sans recalibrage automatique à chaque exécution.

**L24, proposition à reformuler à la demande de l'utilisateur, remplacée pour discussion par L28 : protéger aussi les clients réservés avant leur montée.** La proposition initiale limitait à 300 m l'augmentation cumulative de la distance d'approche annoncée à la confirmation, avec conservation de la distance déjà parcourue. L'utilisateur n'est pas convaincu et demande une autre proposition ; ne pas appliquer ce seuil comme une décision confirmée.

**L25, proposition écartée par U32 : choix des offres selon l'arrivée estimée.** L'assistant proposait de minimiser l'heure estimée d'arrivée finale en tenant compte des distances, arrêts et vitesses publiques disponibles. L'utilisateur retient la proximité de prise en charge avec un critère de budget de détour. Ne pas conserver l'arrivée finale estimée comme critère de sélection sans nouvelle décision.

**L26, absence d'abandon confirmée par U33, relance historique remplacée par U43 : absence d'offre et fin normale.** L'assistant avait proposé un CFP répété toutes les 5 s après un échec. U43 remplace cette partie par une demande persistante mémorisée, sans nouvel appel périodique ni délai de relance. L'arrêt normal exige toujours toutes les livraisons ; un plafond technique termine avec le statut incomplet, les demandes restantes et une cause à examiner, sans être présenté comme une réussite ni comme un abandon volontaire. L'alternative d'une patience maximale explicite a été écartée pour la cible actuelle. Une attente illimitée ne prouve pas que toutes les demandes finiront par être servies.

**L27, confirmé sans changement par U34 : fonctionnement d'un arrêt.** Descente de 2 s par personne, embarquement de 2 s par personne, opérations successives, déposes avant montées afin de libérer les places. Pour 2 descentes et 1 montée, arrêt de 6 s. Pas d'attente volontaire de regroupement ; taxi arrêté hors du flux de circulation, les autres taxis continuent. Les alternatives d'opérations simultanées et d'arrêt bloquant une voie ne sont pas retenues. L'origine initiale des conventions reste distincte de leur confirmation actuelle.

### 4.8 Protection avant embarquement et précision de l'affectation

**L28, protection spatiale confirmée et simplifiée par U35 : protéger la route d'approche.** Après confirmation, une nouvelle insertion ne peut augmenter la distance totale d'approche du taxi vers le client réservé, en comptant la distance parcourue depuis la confirmation et la distance restante. Les nouveaux clients peuvent être servis avant lui s'ils restent sur un itinéraire d'approche de longueur admissible. La proposition initiale limitait en plus les opérations ajoutées à deux par client en attente, soit 4 s ; cette limite a été explicitement retirée par l'utilisateur pour simplifier. Les opérations ajoutées ne sont donc pas plafonnées. Les retards de congestion et de service restent hors garantie temporelle. Exemple : une montée ou une descente sur le chemin est admissible ; un détour spatial de 200 m ne l'est pas avant ce client, mais peut l'être après sa montée selon son budget personnel.

Alternative B historique, non retenue par U35 : autoriser 30 s cumulées de service théorique supplémentaire à vitesse libre, incluant distances et opérations. Ne pas appliquer cette marge ni réintroduire la limite historique de deux opérations sans nouvelle décision.

**L29, confirmé initialement par U36, premier critère remplacé par U41 : budget relatif projeté le plus contraint.** Le classement historique minimisait la distance d'approche prévue, puis le score de saturation, puis l'identifiant. Le classement courant minimise la date estimée de début d'embarquement, puis conserve ce même score et l'identifiant. Pour chaque passager déjà engagé et le candidat, calculer la part du budget utilisée par son détour total déjà effectué et prévu à bord ; le score du taxi est le maximum de ces parts. Exemple : 100 m de détour sur 200 m autorisés donnent 50 %. Une part relative évite de comparer directement des mètres avec des budgets différents ; prendre le maximum évite qu'une moyenne masque un passager à sa limite. Pour un budget nul, exiger zéro détour et attribuer une saturation nulle à ce passager ; un détour positif reste inadmissible. Ne pas utiliser seulement la distance déjà physiquement parcourue, car des réservations peuvent avoir déjà engagé le budget futur. Le nouvel itinéraire permet de calculer le score même pour un taxi auparavant vide. Cette méthode ne garantit pas une utilisation accrue du partage : une préférence pour les budgets peu utilisés peut favoriser des taxis peu chargés.

### 4.9 Choix confirmés : itinéraires, concurrence, carte et taxis libres

Les propositions L30 à L33 ci-dessous sont confirmées respectivement par U37 à U40, mais non implémentées. Leurs alternatives ne sont pas retenues pour la cible actuelle.

| ID | Question et proposition recommandée | Alternative et conséquences |
| --- | --- | --- |
| L30 | Pour construire une offre, essayer les positions possibles de la nouvelle montée et de la nouvelle descente, en conservant l'ordre des arrêts déjà engagés. Parmi les candidats admissibles, retenir le plus faible ajout de distance totale du taxi ; départage déterministe. Les limites de tous les clients, l'approche protégée et la capacité par portion restent impératives. | Réordonner aussi tous les arrêts existants peut trouver de meilleures solutions, mais demande une recherche plus coûteuse et plus difficile à expliquer. La règle d'affectation U36 compare les offres ; elle ne remplace pas ce choix interne du taxi. |
| L31 | Si plusieurs clients acceptent le même taxi pendant une phase, traiter leurs acceptations par ancienneté de demande, puis identifiant. Chaque confirmation revalide et met à jour les engagements ; un candidat devenu inadmissible reçoit un refus et réessaie selon U33. Une offre seule ne réserve pas de place. | Privilégier le plus petit ajout de distance peut améliorer l'efficacité immédiate, mais retarder les anciennes demandes. Protocole de phase, expiration et délais restent à détailler ensuite. |
| L32 | Générer une carte de routes orthogonales en choisissant des lignes et colonnes complètes qui se croisent, avec au moins un axe de chaque orientation. Routes à double sens, sans diagonales ; bâtiments placés dans les cellules non routières adjacentes à une route et associés à un accès. Échelle de 100 m selon U29, géométrie et demandes accessibles à valider et sauvegarder. | Réseau irrégulier connecté : davantage de variété mais génération et vérifications plus complexes. Le format 21 × 21 reste une référence de calcul, pas une taille finale déjà confirmée. |
| L33 | Un taxi sans engagement reste garé à sa position, hors du flux, et continue de répondre aux messages. | Repositionnement vers un centre ou une zone de demande ajoute une politique, des kilomètres à vide et du trafic ; il faut ensuite distinguer ses effets de ceux du partage. |

### 4.10 Idées conservées du cahier d'équipe, demande U42

**Source :** cahier des règles version 1 du 26 octobre 2026 transmis par l'utilisateur le 27 octobre, fichier joint `C:/Users/yanis/.codex/attachments/3900d899-6ec0-4bd1-ae14-01891c19696f/Pasted text.txt`, notamment sections 4, 9, 10, 13, 15, 16, 18 et 19. Les propositions suivantes sont conservées pour examen, sans implémentation. Les principes déjà confirmés sont signalés séparément.

| ID | Idée sauvegardée | Application et statut pour notre cible |
| --- | --- | --- |
| L34 | Identifiant de tentative dans les messages | Adapté et confirmé en U52 : identifier l'offre par demande, taxi et ronde, sans recréer le CFP persistant de U43. L'acceptation vise cette offre précise ; ignorer une ancienne ronde. |
| L35 | Expiration explicite des offres | Confirmé en U52 : offre valable uniquement pendant sa ronde, expiration à sa clôture. Ni fenêtre de collecte ni durée de 2 s du cahier ajoutées. |
| L36 | Confirmation indivisible | Vérifier l'admissibilité et enregistrer les engagements sans intercaler une autre confirmation. Principe explicité par U38 et U51 : mettre à jour les engagements avant de traiter l'acceptation suivante ; réalisation technique à préciser. |
| L37 | Échéances d'appel et de clôture propres à chaque client | Calendriers indépendants sous une horloge commune, sans attendre tous les agents ni introduire un thread par taxi. Compatible avec U22 ; résolution et délais exacts encore ouverts. |
| L38 | Ordre explicite des événements simultanés | Ordre adopté pour notre cible en U51, avec une seule ronde par pas. Cette décision porte sur la séquence explicitée dans U51 et ne valide pas automatiquement l'ordre complet du cahier d'équipe. |
| L39 | Occupation durant les opérations | Confirmé en U53 : place mobilisée du début de montée à la fin de descente, avec états intermédiaires distincts. Réservations futures contrôlées par portion selon U25 ; conventions des indicateurs à préciser séparément. |
| L40 | Accès précis des bâtiments | U56 confirme un accès fixe par bâtiment, choisi à la génération et sauvegardé ; U57 exclut les demandes entre accès identiques. U58 interdit les accès de service aux carrefours d'au moins trois branches, sans interdire leur traversée ni les virages légaux. |
| L41 | Flux aléatoires séparés | Confirmé et précisé en U64 : quatre suites, carte et bâtiments, flotte, voyages, horaires, dérivées de manière stable d'une graine principale. Aucun nouvel aléatoire en exécution ; scénario complet sauvegardé comme référence. |
| L42 | Indicateurs sans observation non applicables | U66 confirme dates inconnues absentes et moyennes des voyages terminés sur les clients livrés, avec effectif et non-livrés distincts. Population vide sans moyenne définie ; zéro effectivement mesuré valide. Autres populations d'indicateurs à expliciter. |
| L43 | Scénarios courts de vérification | Vérifier concurrence, messages périmés, capacité, demandes absentes ou futures, indépendance des taxis et animation sans effet. Adapter les cas de partage à notre capacité par portion et à nos détours. |
| L44 | Mesures détaillées par client et taxi | U66 confirme les lignes individuelles, dates, distances et temps d'activité. U68 définit le partage en mètres de taxi et la décomposition des distances selon zéro à quatre passagers effectifs, adaptée à la capacité. Distinguer explicitement retard de congestion et quantification numérique lors de leur formalisation. |

**Décisions temporelles actualisées :** collecte sans délai simulé ajouté selon U44 et suppression des relances selon U43. Aucun tirage de 5 à 7 s ni fenêtre de collecte de 2 s n'est introduit. Une durée de collecte est un choix de modèle, pas une durée imposée par Mesa ; la documentation officielle de présentation et d'activation a été consultée le 27 octobre 2026 : https://mesa.readthedocs.io/stable/overview.html. Cette consultation ne valide pas l'emploi de ses API actuelles avec l'ancienne dépendance Mesa 3.0.3. L'ordre détaillé des événements reste à préciser.

**Échelle routière actualisée par U45 :** 100 m par portion, vitesse libre de référence de 50 km/h, durée libre fixe de 7,2 s. L'exemple antérieur de 10 m/s n'est pas la vitesse retenue. Les 2 s par portion du cahier d'équipe ne sont pas importées : à notre échelle elles donneraient 180 km/h. La congestion peut allonger la durée réelle ; résolution et fractions de seconde restent à préciser en Q15.

### 4.11 Demande persistante confirmée après question sur les relances

**L45, proposé puis confirmé par U43 le 27 octobre 2026, non implémenté : conserver un seul appel actif jusqu'à réservation.** L'utilisateur a demandé si les relances de 5 s étaient nécessaires puisque l'ancienneté départage les demandes, puis a validé la demande persistante. Distinguer le choix de priorité de U38 et la persistance d'une demande : une priorité ne garantit pas à elle seule qu'un taxi mémorise l'appel après un refus. Dans le mécanisme historique, relancer signifiait refaire un appel pour la même demande, en conservant son identifiant et son heure d'apparition ; ne jamais créer un nouveau client ni réinitialiser son ancienneté.

**Règle confirmée :** diffuser un CFP initial, conserver la demande en attente dans les connaissances acquises par message des taxis sollicités, puis réexaminer les demandes actives lors des activations pertinentes, sans imposer 5 s avant un nouvel examen. Pour la première version, examen à chaque pas de simulation ; il ne signifie ni nouveau CFP ni nouveau client à chaque pas. Réduire les calculs avec des filtres simples et ne renvoyer une offre que si elle est nouvelle, modifiée ou doit être renouvelée selon son protocole. La résolution cible reste à confirmer ; une seconde est un exemple cohérent avec la version historique.

Un taxi peut devenir compatible par déplacement, libération ou réorganisation de places, fin d'opération, changement d'engagement ou information de circulation ; limiter les réexamens au seul retour à l'état libre manquerait des possibilités de partage. Le client continue de choisir selon U41 ; le taxi revalide à chaque confirmation. La réservation clôt la demande ouverte et est notifiée aux taxis concernés pour supprimer appels et offres obsolètes. Le détail des identifiants de version, expirations et notifications reste à préciser selon L34 et L35. Pas de consultation cachée des états privés des clients ni d'attribution centrale à leur place.

L'ancienneté protège les demandes concurrentes admissibles pour un même taxi ; elle n'impose pas une file globale où une demande momentanément impossible bloquerait toutes les suivantes. L'examen fréquent peut augmenter le coût de calcul ; une réévaluation sur événements est une optimisation ultérieure possible. U43 remplace le délai de relance de référence de L26, sans modifier U33 sur l'absence d'abandon. L'approbation provient du message utilisateur suivant la question, pas de la question elle-même.

## 5. Paramètres et comportement de l'implémentation actuelle

### 5.1 Valeurs de référence, modifiables

Ces valeurs sont relevées dans les fichiers au 27 octobre 2026. Leurs noms permettent de les retrouver sans dépendre de numéros de ligne susceptibles de changer.

| Paramètre | Valeur actuelle | Provenance | Où le modifier |
| --- | --- | --- | --- |
| Seed | 42 | Défaut choisi par le LLM | Générateur, interface ou option `--seed` |
| Nombre de taxis | 8 | Défaut choisi par le LLM | Interface ou `--taxis` |
| Nombre de demandes | 30 | Exemple utilisateur retenu comme défaut | Interface ou `--requests` |
| Fenêtre d'apparition | 0 à 300 s, bornes incluses | Choix du LLM | Interface ou `--window` |
| Embarquement | 2 s par personne | Exemple utilisateur retenu, U10 | `Parameters.boarding_s` |
| Descente | 2 s par personne | Choix du LLM | `Parameters.alighting_s` |
| Longueur d'une portion | 60 m | Choix du LLM | `Parameters.segment_length_m` |
| Vitesse libre | 10 m/s | Choix du LLM | `Parameters.free_speed_m_s` |
| Seuil de fluidité K | 2 véhicules par portion dirigée | Choix du LLM | Interface, `--threshold` ou `Parameters.fluid_threshold` |
| Plafond technique | 20 000 s | Choix du LLM | `Parameters.max_seconds` ; option CLI à la génération |
| Capacité physique | 2 places | Choix du LLM | `Taxi.physical_capacity` ; étendre la capacité exige aussi de revoir tests et mesures |

Les constantes physiques sont sauvegardées dans le scénario. Elles ne sont pas toutes exposées dans l'interface ou la ligne de commande. La résolution temporelle reste une seconde dans le code.

### 5.2 Contrat temporel

Pour chaque intervalle de t à t+1 : apparition des demandes dues, échanges de réservation, choix des actions, mesure commune des charges, déplacement ou seconde d'arrêt, notifications de fin d'action, contrôle des invariants et collecte.

Une demande prévue à t est traitable à t. Le gestionnaire crée également les demandes à t+1 en fin d'intervalle pour l'affichage ; elles ne sont traitées qu'à l'intervalle suivant. Une sortie de portion n'autorise pas une seconde traversée dans le même intervalle.

Un changement de cet ordre peut modifier les résultats même sans changement des politiques individuelles. Toute révision doit donc être documentée comme une décision de modèle.

### 5.3 Définitions des mesures

| Mesure | Définition actuelle |
| --- | --- |
| Attente | Début d'embarquement moins heure d'apparition |
| Temps à bord | Début de descente moins fin d'embarquement |
| Temps total | Fin de descente moins heure d'apparition |
| Distance totale | Tous les mètres parcourus, à vide ou occupés |
| Distance partagée | Mètres parcourus avec exactement deux passagers à bord |
| Retard de congestion | Somme de d/v effective moins d/v libre pour chaque déplacement d |
| Temps de circulation cumulé | Somme des secondes passées par les taxis sur les portions |
| Heure de fin | Heure simulée de la dernière descente terminée, depuis 0 seconde |

Avec les constantes actuelles, le temps total d'un passager livré comprend l'attente, deux secondes d'embarquement, le temps à bord et deux secondes de descente. Les arrêts effectués pour d'autres passagers pendant son voyage appartiennent à son temps à bord.

Sur un export partiel, les moyennes n'utilisent que les valeurs déjà disponibles pour chaque indicateur. Leurs populations peuvent donc différer : l'attente peut être connue avant la livraison, alors que le temps total nécessite l'arrivée. Toujours lire `complete`, le nombre de livrés et les états des demandes avant de comparer.

### 5.4 État des vérifications documentées

Le fichier [test_simulation.py](../tests/test_simulation.py) contient 17 tests : durées exactes d'une course, partage identique, prise en charge et dépose intermédiaires, demandes incompatibles ou dépassées, demandes futures, réservations concurrentes, circulation dirigée, exemple de deux cohortes, rejouabilité, indépendance de certains tirages, ordre des taxis, rendu sans effet sur le modèle, validation d'entrées et arrêt technique.

L'exécution précédente rapportée dans la conversation indiquait 17 tests réussis. Pour cette mise à jour documentaire du 27 octobre, les sources et les tests ont été relus ; la suite n'a pas été réexécutée. Un autre LLM doit dater ses propres vérifications au lieu de reprendre ce succès comme une vérification nouvelle.

Pour relancer les vérifications depuis la racine du projet :

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## 6. Points à confirmer et limites

Ces points ne bloquent pas l'usage de la version actuelle. Ils identifient ce qu'un prochain LLM ne doit pas présenter comme définitivement décidé par l'utilisateur.

| ID | Point ouvert | Comportement actuel et impact |
| --- | --- | --- |
| Q01, résolu pour la cible | Nombre total fixé ou tiré dans une plage ? | U61 fixe le total par paramètre, 60 demandes par défaut avec 8 taxis, sans tirage du total. |
| Q02, résolu pour la configuration de départ | Durée d'une « journée » et forme des apparitions ? | U61 fixe une fenêtre abstraite de 0 à 300 s, horaires indépendants uniformes sur les pas de 0,2 s, simultanéités possibles. Pas de profil d'affluence ni de journée réelle calibrée ; livraisons poursuivies après la fenêtre. |
| Q03, résolu pour la cible | Quelle capacité finale ? | U24 : configurable, 3 passagers par défaut, maximum 4. L'ancienne implémentation reste à 2. |
| Q04, modèle et estimation fixés pour la cible | Quel réalisme attendre des embouteillages ? | U54 confirme v = v_libre / max(1, N/K) par portion dirigée, K = 2 par défaut configurable, calcul commun tous les 0,2 s. U55 estime les prises en charge à vitesse libre ; prévision par congestion actuelle reportée sauf besoin. Ni files bloquantes, ni feux, ni trafic extérieur ; modèle non calibré. |
| Q05, résolu pour la cible | Partager pendant l'approche du premier passager ? | Autorisé par U25 ; L07 reste seulement la convention historique. |
| Q06, résolu pour la cible | Optimiser l'affectation et prévoir des places réutilisées plus loin ? | U25 confirme la capacité par portion ; U36 fixe le choix des offres ; U37 construit chaque offre par insertion sans réordonner les arrêts existants. |
| Q07, résolu pour la cible | Les montées et descentes sont-elles successives ou simultanées ? | U34 confirme les opérations successives de 2 s chacune, déposes avant montées, taxi arrêté hors du flux. |
| Q08, périmètre courant défini | Représenter la pollution ou l'acceptabilité ? | U26, U30, U35 et U49 définissent l'acceptabilité en distance et l'approche protégée, sans attente maximale garantie ni préférences individuelles hétérogènes. U71 retient distances et activité sans modèle d'émissions ou conversion en CO2 pour cette version. |
| Q09, tirages définis, versions à préciser | Quel niveau de reproductibilité conserver ? | U64 sépare quatre suites de tirages et conserve le scénario complet comme référence de rejeu. Une graine seule ne suffit pas après changement du générateur. Archiver version du code, règles et environnement lors des comparaisons entre versions ; modalités encore à préciser. |
| Q10, résolu pour la cible | Quels changements physiques pendant une portion en cours ? | U31 confirme les changements aux points autorisés, sans arrêt ou demi-tour intermédiaire. |
| Q11, règle et scénario spatial par défaut définis | Quelle formule précise de budget de distance ? | U30 confirme le budget cumulatif, L23 retient 400 m comme référence. U59 fixe la carte, U60 les bâtiments et U62 le tirage des voyages par bâtiment ; réseau distinct de l'exemple complet L23. Les statistiques de cet exemple ne sont pas celles du scénario cible ; aucun recalibrage automatique du plafond. |
| Q12, résolu pour la cible | Comment protéger l'attente et les arrêts sans détour ? | U35 confirme une approche sans allongement, sans plafond d'opérations ajoutées. Aucune garantie d'attente maximale ; durées des arrêts et congestion restent effectives. |
| Q13, résolu pour la cible | Quel critère de choix d'une offre ? | U41 remplace la distance par le début de prise en charge estimé ; à égalité, conserver le score relatif maximal de U36, puis l'identifiant. |
| Q14, résolu pour la cible | Relances, patience et demandes non servies ? | U33 exclut l'abandon, U43 conserve un CFP persistant réexaminé à chaque pas. U65 arrête techniquement l'état figé sans demande future, tous taxis libres et sans offre admissible, avec clients non servis et statut incomplet. |
| Q15, résolu pour la cible | Comment représenter les fractions de seconde ? | U50 fixe un pas de 0,2 s et un compteur entier : 36 pas par portion libre, 10 par opération. U61 tire les apparitions sur les pas 0 à 1 500 pour la fenêtre par défaut ; fins sous congestion quantifiées au pas. |
| Q16, résolu pour la cible | Quelle durée de collecte, quel ordre et quelle validité des offres ? | U44 impose zéro délai simulé ajouté ; U51 fixe les phases communes et une ronde par pas de 0,2 s ; U52 limite l'offre à sa ronde, identifiée par demande, taxi et ronde. Après refus ou expiration sans confirmation, demande persistante réexaminée au pas suivant sans nouveau CFP. |
| Q17, garantie de circulation définie pour la cible | Comment intégrer l'orientation dans la référence de trajet et la génération ? | U46 à U49 fixent mouvements, cadre, orientations initiales et D0. U67 impose l'accès à tous les arrêts depuis chaque position et orientation légales, avec poursuite légale après arrêt ; carte invalide refusée avant exécution. Les budgets restent contrôlés pour chaque offre, sans garantie que tout client sera servi ; U65 conserve le diagnostic d'état figé. |

Les questions Qxx ne sont pas une liste de fonctionnalités à ajouter automatiquement. Les faire évoluer selon la prochaine demande et maintenir un périmètre maîtrisé.

## 7. Guide de reprise et d'enrichissement

### 7.1 Règles de maintien de cette base

**U18 :** à chaque évolution du code, maintenir simultanément les commentaires et docstrings concernés, ainsi que la documentation affectée. La clarté de la structure et l'explication de la logique font partie du travail demandé.

1. Relire les fichiers réellement présents avant de décrire le fonctionnement : l'utilisateur peut les modifier entre deux échanges.
2. Préserver les identifiants Uxx et Lxx. Lorsqu'une décision est remplacée, conserver son ancienne formulation et identifier celle qui la remplace.
3. Attribuer une nouvelle décision à l'utilisateur seulement si une demande explicite la soutient. Un accord pour coder n'est pas une citation de chacun des choix techniques.
4. Ajouter les choix du nouveau LLM avec le prochain identifiant libre, à partir de L46 après cette version, avec leur justification, leur conséquence et leur statut : proposé, implémenté, confirmé par l'utilisateur ou remplacé. Le prochain identifiant utilisateur libre est U72.
5. Distinguer une modification de paramètre, une modification de règle et une correction de bug. Si un bug contredit une règle attendue, documenter la différence et la correction sans réécrire l'intention utilisateur.
6. Quand le code évolue, synchroniser ce registre, `09_modele_implemente.md`, les valeurs de référence et les vérifications concernées. Les anciens résultats ne sont pas automatiquement ceux de la nouvelle version.
7. Pour comparer les modes, conserver le même scénario et les mêmes règles communes. Pour comparer des versions, conserver aussi la version du code et l'environnement d'exécution.
8. Ajouter une entrée au journal avec la date réelle, l'auteur ou outil connu, les décisions touchées, les fichiers modifiés et les vérifications effectuées. Ne pas inventer de nom ou de version de modèle.

### 7.2 Consignes de collaboration déjà données par l'utilisateur

- Répondre dans la langue de la question.
- Privilégier la méthode fiable la plus simple, rapide et économe ; utiliser scripts ou API pour les opérations répétitives.
- Si un accès manque, signaler rapidement le blocage au lieu d'enchaîner des contournements.
- Ne pas utiliser le caractère de tiret cadratin dans les contenus créés ou modifiés.
- Pour un notebook existant, le relire régulièrement et fournir les cellules complètes dans le chat ; ne pas modifier directement le fichier sans demande explicite.
- Respecter une demande de rester à la logique avant le code. Dans l'historique de ce projet, l'utilisateur a ensuite autorisé l'implémentation par « vasy code ».

Ces consignes sont rappelées pour le transfert. Les instructions actuelles de l'utilisateur et les règles applicables dans la nouvelle session restent prioritaires.

### 7.3 Texte à donner au prochain LLM

> Reprends ce projet de simulation Mesa en commençant par `docs/10_decisions_et_reprise_llm.md`, puis lis `docs/09_modele_implemente.md`, le README et les fichiers concernés par ma demande. Les Uxx sont mes décisions explicites, les Lxx sont les conventions ajoutées par les assistants et les Qxx sont des points ouverts. Préserve cette distinction. Vérifie le code actuel au lieu de supposer que l'historique décrit encore exactement son état. Pour chaque évolution demandée, enrichis cette base avec la provenance du choix, son statut, sa justification, les fichiers affectés et les vérifications réellement effectuées. Conserve l'historique des décisions remplacées. Ne change pas les règles du simulateur si je demande uniquement de la documentation. Réponds dans la langue de ma question et n'utilise pas de tiret cadratin.

### 7.4 Fiche à copier pour une nouvelle décision

```text
Identifiant : prochain Uxx ou Lxx libre, selon la provenance réelle
Titre :
Date :
Origine : demande utilisateur citée, contrainte du cours ou proposition de l'assistant
Statut : proposé / implémenté / confirmé par l'utilisateur / remplacé
Décision :
Justification :
Conséquences et limites :
Décision précédente remplacée, le cas échéant :
Fichiers concernés :
Vérifications effectuées et résultat :
Points restant ouverts :
```

## 8. Journal des évolutions

| Date ou période | Auteur/provenance | Évolution | Vérification et périmètre |
| --- | --- | --- | --- |
| Historique avant cette base | Utilisateur | Réduction du périmètre ; deux modes ; comparabilité ; secondes ; durées fixes ; demandes échelonnées ; congestion par sens ; séparation des responsabilités | Synthétisé en U01 à U12 à partir de la conversation |
| Première implémentation décrite dans la conversation | Assistant LLM | Création des agents, services, interface, scénarios, mesures et tests | Choix regroupés en L01 à L19 ; succès des tests rapporté dans cet historique |
| 27 octobre 2026 | Utilisateur puis assistant LLM | Demande U13 et création de la présente base ; distinction des origines, suivi des décisions remplacées et guide de reprise | Relecture des sources et de la documentation ; mise à jour documentaire uniquement ; pas de nouvelle exécution des tests |

| 27 octobre 2026, nettoyage documentaire | Utilisateur puis assistant | Harmonisation du guide, de la conception, des index et des renvois ; archivage des propositions remplacées ; recommandations et protocole dans le document 11 | Contrôle documentaire et des liens locaux ; aucun changement du simulateur, aucun nouveau résultat de test ou d'expérience ; recommandations non promues en décisions Uxx |

| 27 octobre 2026, clarification du périmètre final | Utilisateur puis assistant | Ajout U14 : individuel et partage sans détour sont des démonstrations intermédiaires ; cible finale élargie, notamment aux détours ; recommandation restrictive du document 11 remplacée | Documentation uniquement ; aucun changement du code ni nouvelle vérification d'exécution |

| 27 octobre 2026, objectifs carte et outils | Utilisateur puis assistant | Ajout U15 (carte générée si simple), U16 (priorité aux outils Mesa adaptés) et proposition L20 ; synchronisation de la conception, du guide et du plan | Documentation uniquement ; aucune modification du simulateur, aucune vérification nouvelle d'API Mesa ou d'exécution |

| 27 octobre 2026, clarification de l'architecture | Utilisateur puis assistant | Ajout U17 précisant U08 : environnement global cohérent, délégation si justifiée et découpage prioritaire des comportements | Documentation uniquement ; aucune refonte, aucune modification des phases ou durées et aucun test exécuté |

| 27 octobre 2026, clarté et commentaires | Utilisateur puis assistant | Ajout U18 : structure claire, commentaires expliquant la logique de chaque partie, mise à jour des commentaires et docstrings à chaque modification concernée | Documentation uniquement ; aucun code modifié ni audit des commentaires existants |

| 27 octobre 2026, limitation du codage en dur | Utilisateur puis assistant | Ajout U19 : paramètres et données variables centralisés, logique indépendante de la carte de démonstration, règles fixes justifiées | Documentation uniquement ; aucune refonte du code ni vérification d'exécution |

| 27 octobre 2026, réécriture plutôt que rustines | Utilisateur puis assistant | Ajout U20 : remplacer proprement le code lorsque son adaptation devient trop coûteuse ou dégrade la cohérence, au lieu d'accumuler les contournements | Documentation uniquement ; aucun code supprimé ou réécrit |

| 27 octobre 2026, langue du code | Utilisateur puis assistant | Précision de U18 : commentaires, docstrings et identifiants du code en anglais ; synchronisation des consignes et de la checklist | Documentation uniquement ; aucun code traduit ou renommé |

| 27 octobre 2026, simulation unique et indépendance des taxis | Utilisateur puis assistant | Ajout U21 : développement d'une seule simulation, modes et comparaisons reportés ; U22 : états et délais propres à chaque taxi, sans attente collective implicite | Documentation uniquement ; interface comparative existante inchangée, aucun scénario ou test exécuté |

| 27 octobre 2026, premier échange de conception pour la réécriture | Utilisateur puis assistant | U23 à U28 : absence de correspondances, capacité 3 par défaut et 4 maximum, réservations pendant l'approche et par portion, acceptabilité en distance, engagements modifiables sous protection des clients, suivi documentaire autorisé. L21 et L22 restent proposés. Q03 et Q05 résolus pour la cible ; Q06 et Q08 précisés ; Q10 à Q12 ajoutés. | Mise à jour du registre, de l'index documentaire et du canevas ; contrôle documentaire uniquement. Aucun code ni test modifié ou exécuté. |

| 27 octobre 2026, échelle spatiale et suite des questions | Utilisateur puis assistant | U29 à U31 : échelle 100 m, règle cumulative de détour validée avec adaptation demandée, changements physiques aux points autorisés confirmés. L23 adapte le plafond à 400 m sur un exemple ; L24 à L27 restent proposés. | Calcul exhaustif en mémoire de 194 040 paires sur un réseau d'exemple : moyenne 1 400 m, médiane 1 300 m, P90 2 300 m. Mise à jour du registre, du canevas et de l'index. Aucun code du projet modifié, aucune simulation ou suite de tests exécutée. |

| 27 octobre 2026, affectation et arrêts | Utilisateur puis assistant | U32 : proximité et budget de détour, détails de départage ouverts ; U33 : pas d'abandon ; U34 : arrêts validés. L24 à reformuler, L25 écarté, statuts de L26 et L27 actualisés. L28 et L29 proposés. | Mise à jour du registre, du canevas et de l'index ; contrôle documentaire uniquement. Aucun code, test ou simulation exécuté ou modifié. |

| 27 octobre 2026, approche protégée et sélection confirmées | Utilisateur puis assistant | U35 confirme l'approche sans allongement et retire le plafond d'opérations ; U36 confirme l'ordre et le score de sélection. Statuts de L28, L29, Q12 et Q13 actualisés. L30 à L33 proposés pour la suite. | Mise à jour du registre, du canevas et de l'index ; contrôle documentaire uniquement. Aucun code modifié ni test ou simulation exécuté. |

| 27 octobre 2026, itinéraires, concurrence et carte confirmés | Utilisateur puis assistant | U37 à U40 confirment L30 à L33 : insertion des arrêts, ancienneté des demandes concurrentes, axes orthogonaux générés, taxis libres garés. Clarification des rôles client et taxi dans CFP, offre, acceptation et confirmation ; détails temporels encore ouverts. | Mise à jour du registre, du canevas et de l'index ; contrôle documentaire uniquement. Aucun code modifié, aucune simulation ou suite de tests exécutée. |

| 27 octobre 2026, apports du cahier d'équipe | Utilisateur puis assistant | U41 remplace le premier critère de sélection par le début de prise en charge estimé, autres départages conservés. U42 demande la sauvegarde des idées utiles ; L34 à L44 les conservent sans adoption automatique. Délais de relance, collecte et durée routière distingués. | Mise à jour du registre, du canevas et de l'index ; vérification arithmétique des unités ; consultation de la présentation officielle Mesa, sans choix d'API ni migration. Aucun code modifié, aucune simulation ou suite de tests exécutée. |

| 27 octobre 2026, remise en question des relances | Utilisateur puis assistant | Question sur l'utilité des 5 s ; clarification de la différence entre priorité, persistance et répétition d'un CFP. L45 propose une demande active mémorisée et réexaminée sans nouvel appel périodique. Proposition non confirmée, aucune décision utilisateur ajoutée. | Mise à jour du registre et des synthèses ; contrôle documentaire uniquement. Aucun code modifié ni simulation ou test exécuté. |

| 27 octobre 2026, demande persistante validée | Utilisateur puis assistant | U43 confirme L45 : CFP initial persistant, examen à chaque pas, ancienneté conservée et clôture notifiée à la réservation. Relances de 5 s de L26 remplacées ; durée de collecte toujours ouverte. | Mise à jour du registre, du canevas et de l'index ; contrôle documentaire uniquement. Aucun code modifié, aucune simulation ou suite de tests exécutée. |

| 27 octobre 2026, collecte immédiate et vitesse de référence | Utilisateur puis assistant | U44 confirme les échanges sans délai simulé ajouté ; U45 interprète la vitesse demandée comme 50 km/h et fixe la durée libre à 7,2 s pour 100 m. Q15 et Q16 explicitent fractions de seconde et ordre des événements. | Mise à jour du registre, du canevas et de l'index ; vérification des unités et de l'effet d'un arrondi à 8 s. Aucun code modifié, aucune simulation ou suite de tests exécutée. |

| 28 octobre 2026, règle de demi-tour de l'équipier adoptée | Utilisateur puis assistant | U46 : aucun demi-tour, même aux intersections ; orientation conservée après arrêt ; chemins, insertions et estimations respectent les mouvements autorisés. Q17 signale les précisions nécessaires sur carte, orientations initiales et référence D0. | Mise à jour du registre, du canevas et de l'index ; contrôle documentaire uniquement. Aucun code modifié, aucune simulation ou suite de tests exécutée. |

| 28 octobre 2026, cadre routier extérieur adopté | Utilisateur puis assistant | Réponse A : U47 relie les axes intérieurs par un cadre à double sens, avec virages à 90° aux coins ; carte finie non torique. Q17 partiellement résolu ; orientations initiales et référence D0 restent ouvertes. | Mise à jour du registre, du canevas et de l'index ; contrôle documentaire uniquement. Aucun code modifié, aucune simulation ou suite de tests exécutée. |

| 28 octobre 2026, orientations initiales aléatoires adoptées | Utilisateur puis assistant | Réponse A : U48 tire une orientation légale après placement de chaque taxi, sauvegardée avec sa position ; aucune répartition équilibrée imposée. Q17 reste ouvert pour D0 et les contrôles détaillés d'accessibilité. | Mise à jour du registre, du canevas et de l'index ; contrôle documentaire uniquement. Aucun code modifié, aucune simulation ou suite de tests exécutée. |

| 28 octobre 2026, distance de référence indépendante du taxi adoptée | Utilisateur puis assistant | Réponse A : U49 fixe D0 une fois par demande, plus court trajet légal avec la meilleure orientation de départ possible. Les distances supplémentaires imposées par l'orientation réelle consomment le budget, même sans partage. Q17 reste ouvert pour les contrôles détaillés des scénarios. | Mise à jour du registre, du canevas et de l'index ; contrôle documentaire uniquement. Aucun code modifié, aucune simulation ou suite de tests exécutée. |

| 28 octobre 2026, pas fixe de 0,2 s adopté | Utilisateur puis assistant | Réponse A : U50 fixe le pas à 0,2 s et l'horloge en pas entiers ; durées libres de 36 pas par portion et 10 par opération. Q15 précisé, ordre détaillé encore ouvert en Q16. | Mise à jour du registre, du canevas et de l'index ; contrôle documentaire uniquement. Aucun code modifié, aucune simulation ou suite de tests exécutée. |

| 28 octobre 2026, phases communes adoptées | Utilisateur puis assistant | Réponse A : U51 fixe l'ordre des fins physiques, apparitions, offres, choix, confirmations, nouveaux départs et progression. Une ronde par pas ; demande refusée réexaminée au pas suivant. Q16 actualisé, validité des offres encore ouverte. | Mise à jour du registre, du canevas et de l'index ; contrôle documentaire uniquement. Aucun code modifié, aucune simulation ou suite de tests exécutée. |

| 28 octobre 2026, offres limitées à leur ronde | Utilisateur puis assistant | Réponse A : U52 fixe l'identification par demande, taxi et ronde, l'expiration en fin de ronde et le renouvellement sans nouveau CFP. Demandes persistantes et engagements confirmés conservés ; Q16 résolu pour la cible. | Mise à jour du registre, du canevas et de l'index ; contrôle documentaire uniquement. Aucun code modifié, aucune simulation ou suite de tests exécutée. |

| 28 octobre 2026, places mobilisées pendant les opérations | Utilisateur puis assistant | Réponse A : U53 mobilise une place du début de montée à la fin de descente. L39 confirmé ; états intermédiaires conservés, réservations futures par portion et mesures distinguées du contrôle physique. | Mise à jour du registre, du canevas et de l'index ; contrôle documentaire uniquement. Aucun code modifié, aucune simulation ou suite de tests exécutée. |

| 28 octobre 2026, congestion par charge adoptée | Utilisateur puis assistant | Réponse A : U54 confirme la formule par portion dirigée, K = 2 par défaut configurable et un calcul commun à chaque pas incluant les nouvelles entrées. Pas de files physiques ; Q04 précisé, prévision des temps dans les offres encore ouverte. | Mise à jour du registre, du canevas et de l'index ; contrôle documentaire uniquement. Aucun code modifié, aucune simulation ou suite de tests exécutée. |

| 28 octobre 2026, prévision à vitesse libre adoptée | Utilisateur puis assistant | Réponse A pour rester simple : U55 estime le début de prise en charge à 50 km/h avec les opérations précédentes, tout en maintenant la congestion réelle U54. L'estimation par congestion observée est reportée sauf besoin concret. | Mise à jour du registre, du canevas et de l'index ; contrôle documentaire uniquement. Aucun code modifié, aucune simulation ou suite de tests exécutée. |

| 28 octobre 2026, accès routier fixe adopté | Utilisateur puis assistant | Réponse A : U56 associe un accès routier fixe à chaque bâtiment, choisi avec départage déterministe et sauvegardé. Plusieurs bâtiments peuvent partager un accès ; demandes correspondantes et arrêts aux intersections encore ouverts. | Mise à jour du registre, du canevas et de l'index ; contrôle documentaire uniquement. Aucun code modifié, aucune simulation ou suite de tests exécutée. |

| 28 octobre 2026, demandes entre accès identiques exclues | Utilisateur puis assistant | Réponse A : U57 exige des accès d'origine et destination distincts pour génération et chargement. Préparer les destinations admissibles ; invalider une carte sans deux accès distincts utilisables. Aucun statut de résolution sans taxi ajouté. | Mise à jour du registre, du canevas et de l'index ; contrôle documentaire uniquement. Aucun code modifié, aucune simulation ou suite de tests exécutée. |

| 28 octobre 2026, opérations hors carrefours adoptées | Utilisateur puis assistant | Réponse A : U58 interdit les montées et descentes sur les carrefours d'au moins trois branches et filtre les accès. Traversée, virages légaux et coins à deux branches du cadre conservés ; L40 précisé. | Mise à jour du registre, du canevas et de l'index ; contrôle documentaire uniquement. Aucun code modifié, aucune simulation ou suite de tests exécutée. |

| 28 octobre 2026, carte par défaut définie | Utilisateur puis assistant | Réponse A : U59 fixe 21 × 21, cinq axes par direction dont trois intérieurs aléatoires, espacement minimal de deux cellules, paramètres configurables et géométrie sauvegardée. L'exemple complet L23 reste distinct du réseau cible. | Mise à jour du registre, du canevas et de l'index ; contrôle documentaire uniquement. Aucun code modifié, aucune simulation ou suite de tests exécutée. |

| 28 octobre 2026, bâtiments uniformément répartis par tirage | Utilisateur puis assistant | Réponse A : U60 retient 32 bâtiments configurables, tirés uniformément sans remise parmi les emplacements admissibles, sans minimum par îlot. Positions et accès fixes sauvegardés ; erreur si le nombre demandé ne peut être placé. | Mise à jour du registre, du canevas et de l'index ; contrôle documentaire uniquement. Aucun code modifié, aucune simulation ou suite de tests exécutée. |

| 28 octobre 2026, demande accrue retenue par défaut | Utilisateur puis assistant | Réponse B : U61 fixe 8 taxis et 60 demandes sur 0 à 300 s, total paramétré et horaires uniformes indépendants sur les pas de 0,2 s. Q01 et Q02 précisés ; origines et destinations et placement initial de flotte encore ouverts. | Mise à jour du registre, du canevas et de l'index ; contrôle documentaire uniquement. Aucun code modifié, aucune simulation ou suite de tests exécutée. |

| 28 octobre 2026, voyages tirés par bâtiment | Utilisateur puis assistant | Réponse A : U62 fixe origine uniforme parmi les bâtiments et destination uniforme parmi ceux d'un autre accès ; demandes indépendantes entre elles et des horaires, répétitions possibles. Aucune attractivité particulière ni uniformisation par accès. | Mise à jour du registre, du canevas et de l'index ; contrôle documentaire uniquement. Aucun code modifié, aucune simulation ou suite de tests exécutée. |

| 28 octobre 2026, positions initiales routières retenues | Utilisateur puis assistant | Réponse A : U63 place les taxis uniformément sans remise sur le réseau hors carrefours, cadre compris, libres et garés. Orientations légales ensuite tirées et sauvegardées ; aucun usage des demandes futures pour optimiser le placement. | Mise à jour du registre, du canevas et de l'index ; contrôle documentaire uniquement. Aucun code modifié, aucune simulation ou suite de tests exécutée. |

| 28 octobre 2026, quatre suites de tirages séparées | Utilisateur puis assistant | Réponse A : U64 dérive de manière stable quatre suites depuis une graine principale, pour carte et bâtiments, flotte, voyages et horaires. L41 confirmé ; scénario complet de référence, aucune stochasticité supplémentaire en exécution. | Mise à jour du registre, du canevas et de l'index ; contrôle documentaire uniquement. Aucun code modifié, aucune simulation ou suite de tests exécutée. |

| 28 octobre 2026, arrêt sur état figé adopté | Utilisateur puis assistant | Réponse A : U65 termine incomplet sans demande future, tous taxis libres et garés, clients en attente et aucune offre admissible après évaluation complète. Diagnostic et clients restants conservés, aucune règle métier assouplie. | Mise à jour du registre, du canevas et de l'index ; contrôle documentaire uniquement. Aucun code modifié, aucune simulation ou suite de tests exécutée. |

| 28 octobre 2026, résumé et mesures individuelles adoptés | Utilisateur puis assistant | Réponse A : U66 conserve lignes par client et taxi et résumé global, précise attente, temps à bord, opérations propres et total. Dates inconnues absentes, moyennes des voyages terminés sur les livrés avec effectif et non-livrés distincts. | Mise à jour du registre, du canevas et de l'index ; contrôle documentaire uniquement. Aucun code modifié, aucune simulation ou suite de tests exécutée. |

| 28 octobre 2026, validation de toute la carte orientée | Utilisateur puis assistant | Réponse A : U67 vérifie l'accès à tous les arrêts et la poursuite légale depuis chaque position et orientation légales du réseau. Q17 précisé ; contrôle indépendant des demandes, sans garantie d'admissibilité de chaque course selon son budget. | Mise à jour du registre, du canevas et de l'index ; contrôle documentaire uniquement. Aucun code modifié, aucune simulation ou suite de tests exécutée. |

| 28 octobre 2026, distances détaillées par occupation | Utilisateur puis assistant | A avec précision utilisateur : U68 mesure les mètres de taxi, décomposés selon zéro à quatre passagers effectifs suivant la capacité. Partage = somme des catégories à partir de deux, avec détails par taxi et pour la flotte ; aucun double comptage des mètres. | Mise à jour du registre, du canevas et de l'index ; contrôle documentaire uniquement. Aucun code modifié, aucune simulation ou suite de tests exécutée. |

| 28 octobre 2026, trois recommandations finales validées | Utilisateur puis assistant | U69 : interface locale pour un monde unique ; U70 : plafond technique configurable avec arrêt incomplet, valeur à ajuster après essais ; U71 : distances et activité sans calcul d'émissions. Synthèse courante et index consolidés, Q08 et Q15 actualisés ; conventions techniques supplémentaires non attribuées à l'utilisateur. | Documentation uniquement ; historique conservé dans le registre. Aucun code modifié, aucune simulation ou suite de tests exécutée. |
