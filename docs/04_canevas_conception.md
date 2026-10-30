# Synthèse de conception actuelle

## Conception actualisée le 30 octobre 2026

Les décisions U23 à U71 et leur actualisation du 30 octobre dans le [registre](10_decisions_et_reprise_llm.md) priment sur les descriptions historiques ci-dessous. Le dépôt actif implémente les demi-tours aux frontières de cellules, avec congestion distincte par sens. Voir ses [décisions techniques](technical-decisions.md).

| Aspect | Décision confirmée pour la cible |
| --- | --- |
| Voyage | Un seul taxi par passager, sans correspondance ; plusieurs arrêts possibles, U23 |
| Capacité | Paramètre entier de 1 à 4 passagers, 3 par défaut, U24 |
| Réservations | Possibles pendant l'approche du premier client ; places réservées uniquement sur les portions concernées, U25 |
| Détours | Budget cumulatif combinant 25 % de la distance routière directe et un plafond métrique, U26 et U30 |
| Référence D0 | Plus court trajet routier entre accès, fixé une fois par demande et identique pour tous les taxis. Les demi-tours libres retirent la dépendance à une orientation de départ ; budgets cumulatifs conservés, actualisation du 30 octobre de U49 |
| Engagements | Modification des arrêts futurs possible si tous les clients déjà engagés restent dans leur acceptabilité, U27 |
| Suivi | Chaque décision documentée avec sa provenance et son statut ; propositions séparées des confirmations, U28 |
| Échelle | Cellules carrées de 100 m de côté ; 100 m entre voisines routières horizontales ou verticales, U29 |
| Changements physiques | Programme révisable immédiatement ; arrêts et changements de direction aux points autorisés après la portion en cours, U31 |
| Affectation | Offres admissibles triées par début de prise en charge estimé ; à égalité, maximum des parts de budget consommées après insertion le plus faible ; puis identifiant, U41 actualisant U32 et U36 |
| Prévision de prise en charge | Déplacements estimés à vitesse libre de 50 km/h, portion et opération en cours comprises avec les opérations précédentes ; montée du candidat exclue. Congestion réelle maintenue, prévision par congestion observée reportée sauf besoin, U55 |
| Demandes sans offre | CFP initial persistant, réexamen à chaque pas sans relances périodiques ni abandon ; ancienneté conservée ; interruption technique incomplète, U33 et U43 |
| État figé | Arrêt technique incomplet après évaluation complète sans offre admissible, si aucune demande future, tous taxis libres et garés et clients encore en attente. Heure, clients non servis et diagnostic conservés, sans assouplir les règles, U65 |
| Mesures | Résumé global et lignes par client et taxi ; états, horodatages, distances et activités. Attente jusqu'au début de montée, temps à bord entre fin de montée et début de descente, opérations propres séparées, total jusqu'à fin de descente. Dates inconnues absentes ; moyennes des voyages terminés sur les livrés avec effectif et non-livrés distincts, U66 |
| Distances par occupation | Mètres de taxi répartis selon zéro, un, deux, trois ou quatre passagers effectifs suivant la capacité ; un seul comptage par mètre. Partage = somme des catégories à partir de deux ; taux sur la distance totale, vide compris. Détail par taxi et somme de flotte, sans confondre distance à vide et référence personnelle D0, U68 |
| Arrêts | Déposes puis montées, 2 s par personne et par opération, successives ; sans attente volontaire et hors du flux de circulation, U34 |
| Places pendant les opérations | Place mobilisée dès le début de montée et libérée à la fin de descente ; états en montée, à bord et en descente conservés. Réservation future distincte de l'occupation physique ; conventions temporelles et distances précisées en U66 et U68, U53 |
| Approche protégée | Distance déjà parcourue depuis confirmation plus distance restante jusqu'à la montée ne dépassent pas l'approche annoncée ; aucun plafond d'opérations ajoutées, U35 |
| Construction des offres | Insérer montée et descente sans réordonner les anciens arrêts ; choisir le candidat admissible ajoutant le moins de distance au taxi, U37 |
| Concurrence | Plusieurs acceptations du même taxi : ancienneté de demande puis identifiant ; revalidation à chaque confirmation, U38 |
| Carte | Axes horizontaux et verticaux générés à double sens, reliés par un cadre routier extérieur ; virages à 90° autorisés aux coins, sans impasse de bord ni raccordement des bords opposés ; bâtiments adjacents avec accès routier, U39 et U47 |
| Géométrie par défaut | 21 × 21 cellules, cinq axes par direction dont deux aux bords et trois intérieurs aléatoires sauvegardés ; espacement minimal de deux cellules entre axes parallèles. Seize îlots, dimensions et nombres d'axes configurables, U59 |
| Accessibilité | Réseau bidirectionnel connecté et accès routiers valides ; une impasse permet de repartir. Remplace le contrôle des états orientés de U67, actualisation du 30 octobre |
| Bâtiments | 32 par défaut, nombre configurable ; tirage uniforme sans remise parmi les cellules non routières avec accès admissible, sans quota par îlot. Positions et accès sauvegardés et fixes ; configuration invalide si le nombre ne peut être placé, U60 |
| Flotte et demande | 8 taxis et 60 demandes par défaut, paramètres configurables. Total fixé, horaires indépendants uniformes sur les pas de 0,2 s entre 0 et 300 s inclus ; scénario sauvegardé, demandes révélées à leur apparition, livraisons poursuivies après 300 s, U61 |
| Positions initiales | Tirage uniforme sans remise sur les cellules routières hors carrefours, cadre compris ; taxis libres sans passager ni réservation, garés hors flux. Orientations légales tirées ensuite ; scénario sauvegardé sans optimisation par les demandes futures, U63 |
| Aléatoire et rejeu | Quatre suites dérivées de manière stable d'une graine principale : carte et bâtiments, flotte, voyages, horaires. Aucun nouveau tirage pendant l'exécution ; scénario complet sauvegardé comme référence, U64 |
| Origines et destinations | Origine uniforme parmi les bâtiments, destination uniforme parmi ceux dont l'accès diffère ; tirages indépendants entre demandes et des horaires, voyages répétés possibles. Identifiants et accès sauvegardés, sans équilibrage par accès ni type de bâtiment, U62 |
| Accès des bâtiments | Une cellule routière adjacente fixe par bâtiment, choisie avec départage déterministe et sauvegardée ; client à cet accès, taxi sur le réseau. Plusieurs bâtiments peuvent partager un accès, U56 |
| Carrefours et service | Montées et descentes hors des carrefours d'au moins trois branches ; filtrer les accès. Traversée et virages légaux autorisés ; coins à deux branches du cadre distincts, U58 |
| Voyages non nuls | Accès d'origine et destination distincts, à la génération et au chargement ; destinations admissibles préparées sans boucle de rejets. Au moins deux accès distincts utilisables, sinon configuration invalide ; aucun statut sans taxi ajouté, U57 |
| Interface | Interface locale existante adaptée à une seule simulation, avec carte, orientations, commandes et indicateurs ; pas de plateforme web adoptée pour cette version, U69 |
| Plafond technique | Durée simulée maximale configurable, complémentaire de la détection d'état figé ; dépassement sans fin normale = arrêt incomplet, même avec des courses en cours. Valeur numérique à déterminer puis ajuster après essais, U70 |
| Pollution | Mesures de distances et activité sans modèle d'émissions ni conversion en CO2 ; kilomètres non présentés comme quantité de pollution, U71 |
| Taxis libres | Garés sur place, hors du flux, disponibles pour les appels ; pas de repositionnement, U40 |
| Communication | Aucun délai simulé ajouté ; phases communes et une ronde par pas, revalidation après chaque confirmation ; demande refusée réexaminée au pas suivant sans nouveau CFP, U44 et U51 |
| Validité des offres | Offre identifiée par demande, taxi et ronde, utilisable uniquement dans cette ronde ; expiration à sa clôture et renouvellement nécessaire au pas suivant, sans supprimer demande persistante ni réservation confirmée, U52 |
| Vitesse et durée routière | 50 km/h de référence, 7,2 s fixes par portion de 100 m hors congestion ; ralentissement possible, U45 |
| Congestion | v = v_libre / max(1, N/K) par portion dirigée ; K = 2 par défaut configurable. Instantané commun par pas de 0,2 s, nouvelles entrées comprises ; taxis en approche comptés, garés ou en opération exclus. Pas de files physiques, U54 |
| Résolution temporelle | Pas fixe de 0,2 s, compteur entier ; 36 pas par portion libre et 10 par montée ou descente. Progressions indépendantes et réexamen des demandes à chaque pas ; fins sous congestion quantifiées au pas, U50 |
| Demi-tours et orientation | Demi-tours autorisés à chaque frontière de cellule routière, sans durée supplémentaire ; portion ou opération engagée terminée avant changement. Orientation conservée pour affichage et mouvements, actualisation du 30 octobre remplaçant U46 |
| Orientations initiales | Tirage aléatoire parmi les orientations légales après placement de chaque taxi ; position et orientation sauvegardées dans le scénario, sans équilibrage imposé, U48 |

**Ordre temporel cible, U51, U52 et U54 :** à l'instant t, finaliser les déplacements et opérations dus, faire apparaître les demandes, évaluer et transmettre les offres, faire choisir les clients, puis revalider et confirmer les acceptations par taxi selon ancienneté et identifiant. Mettre à jour les engagements après chaque confirmation. Les offres expirent à la clôture de leur ronde ; les demandes non confirmées persistent et les réservations confirmées restent engagées. Démarrer les actions physiques possibles, calculer les charges communes avec les nouvelles entrées, puis progresser pendant 0,2 s ; les actions déjà en cours se poursuivent. Une seule ronde de négociation, sans délai simulé ajouté ; après refus, réexamen au pas suivant sans nouveau CFP. Les conventions de l'ancienne démonstration ci-dessous ne remplacent pas cet ordre. Selon U55, les offres estiment les déplacements à vitesse libre ; la congestion s'applique aux déplacements réels.

**Routage et carte, actualisation du 30 octobre 2026 :** chemins déterministes entre cellules, demi-tours autorisés après la portion engagée. Pour chaque ordre d'arrêts, une seule progression avec comptes individuels remplace les alternatives d'orientation. D0, budgets, protections d'approche et revalidation sont conservés. Les orientations initiales restent sauvegardées pour les triangles ; la congestion reste calculée par portion dirigée.

**Budget et exemple historique, U30, U49, U59 et L23 :** budget cumulatif = min(25 % de D0, 400 m), avec distance personnelle déjà parcourue et restante ; ne pas le réinitialiser après insertion. Le plafond de 400 m reste la référence adaptée par l'assistant, non calibrée. Le calcul historique de moyenne à 1 400 m concernait un réseau complet de 21 × 21 points routiers, distinct de la carte cible à cinq axes par direction. Ne pas transposer cette moyenne au générateur retenu ni recalibrer implicitement le plafond.

**Actualisations :** les relances historiques de 5 s sont remplacées par U43 ; l'absence d'abandon U33 est maintenue. L27 est confirmé par U34 ; L25 est écarté par U32. L24 est remplacé par la protection spatiale L28 confirmée en U35, sans plafond d'opérations. Le premier critère de L29 est actualisé par U41, le score de budget de U36 est conservé. Des arrêts sur le chemin peuvent prolonger l'attente : aucune attente maximale n'est garantie.

**Rôles et confirmations, U37 à U41, U51 et U52 :** le client émet l'appel et choisit une offre ; le taxi construit, évalue et revalide sa proposition. Les estimations et scores sont transmis par message, sans lecture des états privés des autres agents. Une offre ne réserve pas de place et expire à la clôture de sa ronde. Les confirmations mettent à jour les engagements avant le traitement de l'acceptation suivante. Phases temporelles, carte, demande et congestion sont définies dans le tableau courant.

**Apports du cahier d'équipe, U42 :** les idées L34 à L44 sont conservées avec leur provenance dans le registre. Leurs confirmations ultérieures y sont identifiées : offres, ordre des événements, occupation pendant les opérations, accès, flux aléatoires et mesures. Les scénarios de vérification L43 restent à construire et exécuter. La sauvegarde initiale de ces idées n'est pas une validation automatique de tous les choix du cahier.

**Demandes persistantes, U43, U50 à U52 :** un CFP initial est mémorisé ; les demandes actives sont réexaminées à chaque pas de 0,2 s sans nouvel appel périodique et en conservant leur ancienneté. Les offres sont identifiées par demande, taxi et ronde, puis renouvelées si nécessaire à la ronde suivante. Après refus, réexamen au pas suivant ; réservation confirmée = clôture de la demande ouverte et notification. Une demande impossible ne bloque pas les autres demandes compatibles.

## Préparation technique restante

Les décisions métier principales sont définies. La préparation de la réécriture doit encore vérifier les outils de la version Mesa retenue selon U16, préciser les formats de messages et d'export, les départages internes déterministes, la gestion des opérations déjà commencées, et la séparation entre retard de congestion et quantification numérique. Ces conventions techniques ne sont pas attribuées à l'utilisateur sans confirmation.

La traçabilité devra conserver le scénario complet avec la version du code et l'environnement utilisés. La valeur numérique du plafond U70 sera déterminée puis ajustée après les premiers essais. Aucun de ces essais ni aucune réécriture ne sont réalisés par cette consolidation documentaire.

## Description historique de la démonstration et principes conservés

> Objectif final clarifié le 27 octobre 2026 (U14) : la version individuelle et le partage à deux sans détour sont des démonstrations intermédiaires. La cible finale est élargie, notamment aux détours et à une progression vers les niveaux avancés du sujet. Les règles ci-dessous décrivant la version actuelle ne fixent pas le périmètre final. Voir le [registre des décisions](10_decisions_et_reprise_llm.md).


Mise à jour documentaire : 27 octobre 2026. Cette fiche remplace le canevas initial. Elle synthétise les décisions consignées, sans nouvel audit du code. Le [registre](10_decisions_et_reprise_llm.md) fait référence pour leur provenance ; le [modèle documenté](09_modele_implemente.md) décrit les conventions détaillées.

## Question et périmètre

À demande et flotte initiales identiques, quel effet le partage sans détour a-t-il sur la distance totale des taxis, l'attente et le temps total des passagers, ainsi que sur le ralentissement lié à la circulation ?

L'objectif est une comparaison sur un modèle simplifié, sans présupposer un gain. Les décisions utilisateur U01 à U12 retiennent Mesa, deux modes comparables, des trajets compatibles, une congestion par sens, des durées explicites et des demandes progressives. Elles ne fixent pas toutes les valeurs numériques.

| Aspect | Convention actuelle | Provenance |
| --- | --- | --- |
| Référence et variante | Un engagement en individuel, deux en partagé, réservations incluses | Objectif U02 ; capacité L05 |
| Partage | Origine puis destination sur le trajet restant, sans détour ; aucun second engagement pendant l'approche | U03 ; formalisation L06 et restriction L07 |
| Espace | MultiGrid 11 × 9 non torique, réseau routier et onze bâtiments | Recommandation du cours ; géométrie L03 |
| Chemins | Plus courts chemins en nombre de portions, départage déterministe ; pas de reroutage face à la congestion | L03 et L06 |
| Temps | Résolution 1 s ; embarquement et descente 2 s par personne, successifs | U09 et U10 ; conventions L10 |
| Demande | Ensemble fini pré-généré, apparitions progressives ; défaut 30 demandes sur 0 à 300 s | U11 ; distribution et fenêtre L02 |
| Circulation | Charge et vitesse par portion dirigée ; pas de files physiques ni trafic extérieur | U06 et U07 ; L12 et L13 |
| Fin | Toutes les demandes apparues et tous les passagers descendus ; plafond technique signalé comme échec | U12 ; interprétation L15 |
| Absents de la version actuelle, sans exclusion définitive | Marche, détours, correspondances, émissions calculées et acceptabilité individuelle | U01 et simplifications L07, L11, L13 |

## Agents, information et environnement

| Entité | Perception et décision | Actions et effets |
| --- | --- | --- |
| Passager | Offres reçues ; choix selon la fin d'embarquement estimée, puis identifiant du taxi | CFP, acceptation ; reçoit confirmations et notifications |
| Taxi | Messages, engagements propres et informations routières publiques ; contrôle de capacité et de compatibilité | Offre, confirmation ou refus ; déplacement, embarquement et dépose |
| Services | Carte, calendrier, transport des messages, circulation et observation | Création des demandes dues, calcul commun des charges, livraison et collecte |

L'observateur peut lire les états globaux pour mesurer et vérifier. Cette information ne doit pas devenir une perception globale implicite des agents. Les passagers à bord quittent la grille et leur localisation dépend du taxi.

## Temps et interactions

Pour chaque intervalle de t à t+1 : apparition des demandes dues, échanges de réservation à temps constant, choix des actions, calcul commun des charges, déplacement ou seconde d'arrêt, effets de fin d'action et collecte. Les demandes de t+1 visibles à l'affichage sont traitées à l'intervalle suivant.

Une offre seule n'engage pas de place. La confirmation revalide capacité et trajet. Les conflits suivent un ordre déterministe. Le rapport doit expliciter les phases de communication et les actions physiques, ainsi que leurs durées.

## Mesures et limites

Les mesures actuelles comprennent distance totale à vide et occupée, distance partagée, attente, temps à bord, temps total, retard de congestion, temps de circulation et heure de fin. Leurs formules figurent dans [le modèle documenté](09_modele_implemente.md).

Une comparaison finale doit vérifier que les deux exécutions sont complètes et portent sur les mêmes entrées. La distance mesure une activité des taxis, pas directement la pollution. Les tests mécaniques ne valident pas le réalisme de la congestion.

## Expériences et historique

Le [plan d'amélioration](11_priorites_et_experiences.md) propose les expériences et les éléments à présenter dans le rapport. Ces propositions ne sont ni des résultats acquis ni de nouvelles règles du simulateur.

L'[ancien canevas](archives/04_canevas_conception.md) conserve les idées remplacées : grille 4 × 4, temps abstrait, 40 demandes et exclusion de la congestion. Il sert uniquement d'historique.


## Objectifs complémentaires confirmés : U15 et U16

- Viser une carte générée automatiquement si une méthode simple et fiable suffit. La carte fixe décrite ci-dessus correspond uniquement à l'état actuel. Conserver une même géométrie sauvegardée pour comparer les modes, et vérifier la connexité du réseau et l'accès des bâtiments.
- Privilégier les outils Mesa adaptés et compatibles avec la version retenue. Avant une implémentation personnalisée ou l'ajout d'une dépendance, examiner la solution Mesa et justifier l'écart si elle ne convient pas.

Le registre distingue les objectifs utilisateur U15 et U16 de la piste technique L20, qui reste une proposition de génération à examiner.


## Architecture cible, précision U17

Conserver un environnement global cohérent, responsable du monde et de la coordination. Ajouter des agents ou services complémentaires seulement pour des responsabilités justifiées. Le découpage principal concerne les comportements des agents, en blocs courts et ciblés, plutôt qu'une multiplication des sous-étapes de l'environnement.

Les phases temporelles décrites plus haut restent les conventions de la version actuelle. Un découpage pour améliorer la lisibilité ne doit pas modifier implicitement l'ordre des interactions, les durées ou le budget d'action. La robustesse repose sur des contrats et transitions clairs en plus de comportements lisibles. Voir U17, qui précise U08 dans le registre.


## Lisibilité et commentaires, U18

La structure doit être claire : fichiers et comportements aux responsabilités identifiables, noms explicites et déroulement lisible. Chaque partie du code doit expliquer sa logique par des commentaires adaptés : étapes, raisons des choix, hypothèses, transitions et cas particuliers. Les docstrings présentent les contrats utiles. Tous les commentaires et docstrings doivent être en anglais, ainsi que les noms des fonctions, méthodes, classes, variables, paramètres, attributs, constantes et modules définis dans le code. À chaque modification, relire et mettre à jour dans le même changement les commentaires et docstrings affectés, y compris ceux situés ailleurs. Cette règle complète U17 ; elle ne constitue pas un audit déjà réalisé du code existant.


## Paramétrage et limitation du codage en dur, U19

Centraliser les paramètres et leurs valeurs par défaut ; utiliser les données du scénario ou une génération simple pour les éléments variables. Les comportements et le rendu doivent exploiter la carte fournie sans dépendre des coordonnées particulières de la démonstration. Distinguer paramètres, politiques et invariants : les contraintes de cohérence restent obligatoires, même quand leurs valeurs sont configurables. Conserver et justifier les règles fixes nécessaires, sans multiplier artificiellement les options.


## Stratégie d'évolution, U20

Si l'adaptation d'une partie du code devient trop coûteuse ou impose une accumulation de contournements, préférer la remplacer par une implémentation propre. Choisir le périmètre utile de réécriture, conserver les décisions métier et les vérifications pertinentes, puis retirer les anciennes branches devenues inutiles. L'objectif est une architecture cohérente avec la cible finale, sans imposer de préserver chaque détail de la démonstration initiale.


## Priorité actuelle : simulation unique et taxis indépendants, U21 et U22

Se concentrer sur un seul monde simulé. Le mode limité à un passager et les autres modes de comparaison seront examinés plus tard. Les objectifs finaux de détours et niveaux avancés sont conservés. Les descriptions précédentes des deux modes concernent l'existant et les comparaisons futures.

Chaque taxi conserve son état, ses engagements et ses délais propres. Des taxis peuvent simultanément rouler, embarquer, déposer ou attendre une demande. L'attente d'un taxi ne bloque pas les autres. L'horloge globale coordonne des progressions individuelles ; elle n'impose pas une action ou une attente commune. Les effets collectifs explicitement modélisés, comme la congestion, restent possibles.
