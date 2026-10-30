# Ancienne version : conception et conventions

> Actualisation du 30 octobre 2026 : ce document conserve une description historique. Le code actif se trouve à la racine de ce dépôt. Les demi-tours aux frontières de cellules sont désormais autorisés, avec congestion séparée par sens et actions engagées préservées. Les comparaisons capacité 1 / 3 sont implémentées. Lire les [décisions techniques actuelles](technical-decisions.md) et la [validation](validation.md).


> Priorité actuelle, U21 et U22 : développer une seule simulation avec des états et délais indépendants pour chaque taxi. Un taxi qui attend ne bloque pas les autres. Les modes à un passager et les comparaisons sont reportés ; les descriptions de deux simulations ci-dessous concernent l'existant ou des travaux ultérieurs, sans imposer une exécution simultanée. Aucun code n'a été modifié lors de cette clarification.


> Objectif final clarifié le 27 octobre 2026 (U14) : la version individuelle et le partage à deux sans détour sont des démonstrations intermédiaires. La cible finale est élargie, notamment aux détours et à une progression vers les niveaux avancés du sujet. Les règles ci-dessous décrivant la version actuelle ne fixent pas le périmètre final. Voir le [registre des décisions](10_decisions_et_reprise_llm.md).


Cette version met en oeuvre les objectifs utilisateur et les conventions ajoutées par l'assistant dans la conversation. Toutes les constantes et règles détaillées n'ont pas été fixées explicitement par l'utilisateur. Le [registre des décisions et guide de reprise](10_decisions_et_reprise_llm.md), rédigé le 27 octobre 2026, distingue leur provenance. Les constantes sont des hypothèses de simulation, sans calibration sur une ville réelle. Les exigences du professeur restent documentées dans `08_projet_session5.md`.

## Scenario commun

Le scenario JSON contient la carte complete, les batiments et leurs acces, les positions initiales des taxis, toutes les demandes et les parametres physiques. Son empreinte SHA-256 figure dans les resultats des deux modes.

Les positions initiales des taxis sont tirees parmi les cellules routieres. Chaque demande possede un identifiant, une origine, une destination et une heure d'apparition entiere, tiree uniformement entre 0 et la fin de la fenetre incluse. Origine et destination sont tirees uniformement parmi les batiments distincts. Des tirages independants controlent flotte et demandes. Aucun tirage aleatoire ne survient ensuite dans les decisions, les durees ou le rendu.

Les demandes futures sont connues du gestionnaire de scenario, mais ne sont communiquees aux taxis qu'a leur apparition. Leurs agents passagers sont crees a cet instant. Il n'y a ni annulation ni abandon dans cette version.

## Carte et batiments

La carte fixe mesure 11 par 9 cellules. Les cellules routieres forment trois axes verticaux et deux axes horizontaux. Onze batiments sont associes a des acces routiers adjacents. Le taxi ne traverse jamais un batiment. Le passager attend directement a son acces, sans marche simulee.

`MultiGrid` contient les taxis et les passagers en attente ou reserves. Les batiments sont des donnees statiques utilisees pour le dessin et les demandes. Un passager embarque est retire de la grille, reste enregistre comme agent Mesa et sa localisation depend de son taxi.

Les routes forment implicitement un graphe. Une recherche en largeur trouve les plus courts chemins en nombre de portions. L'ordre des voisins est fixe : est, nord, ouest, sud. Les chemins sont mis en cache. Aucun chemin n'est recalcule pour contourner la congestion.

## Roles et services

| Composant | Responsabilite |
| --- | --- |
| `Passenger` | Envoyer un CFP, choisir une offre, accepter et recevoir les notifications de transport |
| `Taxi` | Evaluer les demandes, confirmer ses reservations, executer ses deplacements et arrets |
| `DemandScheduler` | Creer les agents passagers a leur heure d'apparition |
| `MessageBus` | Livrer les messages et enregistrer leur historique |
| `City` | Conserver la carte, les acces et les chemins autorises |
| `Traffic` | Calculer les charges et vitesses par portion dirigee |
| `Metrics` | Observer les etats, calculer les indicateurs et exporter |
| `TaxiModel` | Coordonner les phases et conserver l'horloge en secondes |

Les taxis utilisent les contenus des messages et les informations routieres publiques. Ils ne consultent pas les etats internes des autres taxis ou des passagers pour prendre leurs decisions. L'observateur et les controles de coherence peuvent inspecter les etats globaux.

## Reservation et partage

Les deux modes emploient des taxis de deux places physiques. Le mode individuel limite les engagements a un passager. Le mode partage autorise deux engagements, reservations incluses. Cette regle conservative ne promet pas une place reservee a une autre personne avant sa liberation.

Un passager en attente envoie un `CFP` a tous les taxis, avec origine, destination et heure de demande. Les taxis admissibles repondent par `OFFER`, avec une estimation de l'heure de fin d'embarquement. Le passager choisit l'estimation la plus faible, puis le numero de taxi en cas d'egalite. Il envoie un `ACCEPT`. Le taxi revalide la place et le trajet, puis repond `CONFIRM` ou `REJECT`.

Les acceptations concurrentes sont traitees par heure de demande puis identifiant. Les offres ne bloquent pas de place et expirent a la fin de la phase. Un refus laisse le passager en attente ; il peut refaire une demande la seconde suivante. Il s'agit d'une politique gloutonne, sans optimisation globale d'affectation. Plusieurs passagers peuvent donc solliciter le meme taxi alors qu'un autre est libre.

Le premier engagement fixe une approche et un trajet de transport. Pendant l'approche, le taxi n'accepte pas de second passager. Quand il atteint l'origine, le partage devient possible : l'origine du second passager doit figurer avant sa destination sur le trajet restant. Le point de depart d'une portion deja entamee est exclu. Le trajet ne subit aucun detour. Les nouvelles prises en charge peuvent ajouter des arrets et des retards.

Exemples sur A vers B vers C vers D : A vers D, A vers C et B vers C peuvent etre regroupes avec A vers D. C vers B ou une destination hors du trajet ne peuvent pas l'etre. Une fois A depasse, une nouvelle demande depuis A est incompatible avec la course en cours.

Les departs ne sont pas retardes volontairement pour attendre d'eventuelles nouvelles demandes. A un arret, les deposes sont effectuees avant les embarquements, puis par anciennete de demande et identifiant.

## Horloge et durees

La resolution est une seconde. Un embarquement prend deux secondes par personne, et une descente deux secondes par personne. Les operations sont successives : deux embarquements prennent quatre secondes. Aucune autre action physique n'a lieu pendant un arret.

Chaque portion mesure 60 metres et sa vitesse libre vaut 10 metres par seconde, soit six secondes sans congestion. Ces unites sont des valeurs de modele, sans revendication de realisme calibre.

Pour l'intervalle de temps allant de t a t+1 :

1. Faire apparaitre les demandes prevues a t.
2. Echanger CFP, offres, acceptations et confirmations a temps simule constant.
3. Chaque taxi choisit un arret ou entre sur sa prochaine portion.
4. Calculer toutes les charges, nouvelles entrees comprises.
5. Faire avancer tous les taxis selon ce meme instantane, ou consommer une seconde d'arret.
6. Appliquer les arrivees, embarquements et deposes a t+1.
7. Faire apparaitre les demandes de t+1 pour l'affichage, verifier les invariants et collecter.

La demande apparue a t+1 est traitee dans la phase de communication de l'intervalle suivant. Les messages prennent un temps simule nul. Les arrondis de mouvement se font a la seconde : un reliquat de portion prend une seconde entiere et le taxi ne repart pas sur la suivante dans le meme intervalle.

## Congestion dirigee

Chaque portion est identifiee par le couple ordonne (cellule de depart, cellule d'arrivee). A vers B et B vers A ont des charges independantes. Deux sorties differentes depuis A sont egalement independantes. Les conflits d'intersection ne sont pas representes.

N compte les taxis effectivement engages sur une portion. Un taxi transporte un ou deux passagers mais compte toujours pour un seul vehicule. Un taxi vide en approche compte. Un taxi disponible ou en arret est suppose gare en bord de route et ne compte pas. Aucun vehicule exterieur n'est simule.

K est un seuil de fluidite, deux par defaut, et non une capacite physique bloquant l'entree. La charge vaut N/K. La vitesse commune de l'intervalle est :

**v = vitesse libre / max(1, N/K)**

Avec K=2 : un ou deux taxis roulent a 10 m/s ; trois a environ 6,67 m/s ; quatre a 5 m/s. Le sens oppose est traite a part. Les vitesses sont recalculees chaque seconde selon les entrees et sorties. Les sorties en fin d'intervalle influencent la vitesse de l'intervalle suivant.

Chaque taxi garde une progression continue en metres. Il ne peut embarquer au milieu d'une portion. A l'affichage, sa position est interpolee entre les cellules ; sa position dans `MultiGrid` reste celle du depart jusqu'a l'arrivee.

Il s'agit d'un modele de ralentissement par densite. Il ne represente ni distances de securite, ni files physiques, ni blocage de carrefour, ni feux. Une destination finale differente n'evite pas la congestion si deux taxis empruntent la meme portion dans le meme sens.

## Arret et mesures

L'arret normal exige que toutes les demandes prevues soient apparues et que tous les passagers soient deposes. Une periode temporairement sans demande active ne termine pas la simulation. Une liste vide se termine a 0 seconde. Un plafond technique interrompt avec une erreur explicite, jamais comme une execution reussie.

| Indicateur | Convention |
| --- | --- |
| Attente | Debut d'embarquement moins apparition de la demande |
| Temps a bord | Debut de descente moins fin d'embarquement |
| Temps total | Fin de descente moins apparition de la demande |
| Distance totale | Somme des metres reellement parcourus, a vide ou occupes |
| Distance partagee | Metres parcourus avec deux passagers simultanement a bord |
| Retard de congestion | Somme, pour chaque deplacement d, de d/v effective moins d/v libre |
| Temps de circulation | Somme des secondes durant lesquelles les taxis parcourent une portion |
| Fin de service | Heure de la derniere depose, depuis 0 seconde |

Le retard de congestion est exprime en vehicule.secondes et distingue le ralentissement de l'arrondi a la seconde en fin de portion. Le temps total comprend attente, embarquement, temps a bord et descente. Les etats et valeurs manquantes sont conserves dans les exports partiels. Pour une execution complete, toutes les demandes sont presentes dans les moyennes.

Les conclusions concernent ce modele. La distance est un indicateur d'activite, pas une mesure directe de pollution. Le partage ne garantit pas une amelioration pour chaque scenario.
