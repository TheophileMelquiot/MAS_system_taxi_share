# Checklist pour concevoir et relire le projet

Les éléments **Cours** correspondent à des recommandations explicites du support. Les éléments **Proposition** sont des vérifications utiles, à adapter au sujet. Cette liste n'est pas un barème du professeur.

## Exigences et remise de la session 5

Mise à jour : 19 octobre 2026. **Projet S5** correspond à l'énoncé ; les références **Cours** de la suite concernent S4. Mise à jour du 27 octobre 2026 : les cases restent ouvertes car cette relecture documentaire ne constitue pas une vérification d'exécution. L'état décrit est dans le registre et le modèle documenté ; les priorités sont dans [le plan proposé](11_priorites_et_experiences.md).

- [ ] **Projet S5 p. 4** : groupe de 1 ou 2, travail organisé selon les 6 h annoncées par étudiant.
- [ ] **Projet S5 p. 4** : Python + Mesa ou Java + JADE, sans autre plateforme MAS ni MAS maison sans bibliothèque.
- [ ] **Projet S5 p. 4** : remise avant dimanche 25 octobre 2026 à 23 h 59 CET.
- [ ] **Projet S5 p. 5** : code source fourni et rapport conforme à « 5-10 pages max » ; viser 5 à 10 pages, plafond 10.
- [ ] **Projet S5 p. 5, conception 20 %** : choix et hypothèses expliqués dans le rapport.
- [ ] **Projet S5 p. 5, implémentation 20 %** : bon usage de la bibliothèque et code fonctionnel.
- [ ] **Projet S5 p. 5, fonctionnalités/utilisabilité 20 %** : programme prêt à être exécuté par le professeur.
- [ ] **Projet S5 p. 5, analyse 20 %** : résultats de simulation effectifs dans le rapport.
- [ ] **Projet S5 p. 5, présentation 20 %** : rapport organisé et code commenté utilement.
- [ ] **Projet S5 p. 6** : sujet taxis partagés, paramètres identifiés tôt, question et variables observables définies.
- [ ] **Projet S5 p. 6 et 7** : effets sur trafic et temps étudiés ; périmètre de l'acceptabilité et des embouteillages précisé, ces deux points étant optionnels p. 7.
- [ ] **Projet S5 p. 6** : construction incrémentale et simple ; niveaux avancés identifiés comme exemples de progression.
- [ ] **Projet S5 p. 8, Mesa** : recommandation `MultiGrid` prise en compte ; représentation spatiale et durées de trajet justifiées.
- [ ] **Projet S5 p. 8, Mesa** : communication directe minimale CFP et réponses implémentée.
- [ ] **Projet S5 p. 8, Mesa** : visualisation utilisée dès le début, positions et graphiques.
- [ ] **Projet S5 p. 9, si JADE** : pas d'interface, valeurs journalisées pour tableur, quartiers agents, temporisations et CPU contrôlés.

## Contrôles proposés pour les taxis

- [ ] Référence individuelle et partage comparés sur les mêmes demandes et positions initiales.
- [ ] Capacité respectée, réservations incluses ; aucun passager confirmé auprès de deux taxis.
- [ ] Dates de demande, prise en charge et arrivée cohérentes ; états et manifeste sans doublons.
- [ ] Attente, temps à bord et temps total distingués.
- [ ] Distance à vide incluse dans la distance totale ; activité des taxis distinguée des émissions réelles.
- [ ] Demandes non servies à l'arrêt comptabilisées et signalées dans les comparaisons.
- [ ] Cas compatible et incompatible avec un partage sans détour vérifiés.
- [ ] CFP sans offre, refus et concurrence de réservations traités.
- [ ] Installation, commande de lancement, paramètres et reproduction d'une expérience expliqués.
- [ ] Conclusions appuyées sur des résultats réels, avec limites et dispersion.

## Cadrage

- [ ] **Cours, diapo 8** : le système source et le cadre expérimental sont définis.
- [ ] **Proposition** : l'hypothèse, les mesures et la comparaison de référence répondent à une même question.
- [ ] **Cours, diapo 14** : les entités actives, leurs actions et la granularité sont identifiées.
- [ ] **Proposition** : les limites et hypothèses sont explicites.
- [ ] **Proposition** : le cahier des charges reçu est distingué des conseils de cette documentation.

## Les quatre aspects du modèle

- [ ] **Cours, diapo 15** : comportement, environnement, ordonnancement et interactions sont décrits.
- [ ] **Cours, diapo 14** : les ressources et la spatialisation sont inventoriées.
- [ ] **Cours, diapo 14** : les choix discret, dynamique, ouvert et de synchronisation sont traités.
- [ ] **Proposition** : les conflits et conditions d'arrêt ont une règle précise.

## Comportement des agents

- [ ] **Cours, diapo 22** : les agents ne consultent pas indûment l'état interne de leurs pairs.
- [ ] **Cours, diapo 24** : la perception, la décision et l'action sont visibles dans l'organisation du code.
- [ ] **Cours, diapo 23** : les perceptions cachées et leur coût sont examinés.
- [ ] **Cours, diapo 23** : le nombre d'actions par activation respecte la règle retenue.
- [ ] **Proposition** : l'instrumentation globale ne modifie pas l'information disponible pour décider.
- [ ] **Cours, diapo 25** : les calculs longs ne bloquent pas inutilement les activations.
- [ ] **Proposition** : si un traitement externe existe, son délai et le moment d'application de son résultat sont définis.

## Communication et temps

- [ ] **Proposition** : le choix entre effets immédiats et décisions sur état commun est explicite.
- [ ] **Proposition** : un exemple avec deux agents explique les conséquences de l'ordre d'activation.
- [ ] **Proposition appliquée à S5** : les messages requis ont des règles de transport, lecture, expiration et consommation définies.
- [ ] **Proposition** : les mises à jour de ressources interviennent à un moment identifié.

## Technique et visualisation

- [ ] **Cours, diapo 29** : l'installation locale utilise un environnement virtuel.
- [ ] **Proposition** : la version de Mesa correspond au notebook ou à l'énoncé.
- [ ] **Proposition** : les coquilles et fragments de pseudo-code du PDF ne sont pas copiés comme code exécutable.
- [ ] **Cours, diapo 30** : portrayal, paramètres et renderer sont définis pour la visualisation.
- [ ] **Cours, diapo 30** : la visualisation présentée utilise une installation locale.
- [ ] **Proposition** : afficher les résultats ne change pas les règles ou les tirages de la simulation.
- [ ] **Cours, diapo 37** : les figures utilisent l'API objet Matplotlib.
- [ ] **Complément officiel** : si des threads touchent Matplotlib, l'accès graphique est sérialisé.

## Résultats et documentation

- [ ] **Cours, diapo 8** : correction de l'implémentation et validité du modèle sont discutées séparément.
- [ ] **Proposition** : les invariants utiles sont contrôlés sur des cas courts et des cas limites.
- [ ] **Proposition** : les mesures ont une définition, une unité et un moment de collecte.
- [ ] **Proposition** : plusieurs graines et la dispersion des résultats sont examinées.
- [ ] **Proposition** : les paramètres, versions et conditions d'arrêt sont conservés.
- [ ] **Cours, diapos 5 et 6** : les expériences servent à analyser puis réviser le modèle.
- [ ] **Proposition** : le README explique l'installation, l'exécution et les conclusions dans leur domaine de validité.


## Objectifs utilisateur ajoutés le 27 octobre 2026

- [ ] **U15, conditionné à une solution simple** : génération automatique de la carte étudiée, réseau connecté et bâtiments accessibles ; géométrie reproductible, sauvegardée et commune aux modes comparés.
- [ ] **U16** : outils Mesa adaptés examinés avant chaque solution personnalisée ou externe ; version compatible et raison de l'écart documentées.


- [ ] **U17, précision de U08** : environnement global cohérent, délégations justifiées, comportements courts et ciblés ; découpage interne distingué des phases temporelles et changements de règles.


- [ ] **U18** : structure claire et logique expliquée dans chaque partie par des commentaires adaptés ; commentaires et docstrings affectés relus et synchronisés à chaque mise à jour du code, sans explication obsolète. Tous les commentaires et docstrings doivent être en anglais, ainsi que les noms des fonctions, méthodes, classes, variables, paramètres, attributs, constantes et modules définis dans le code.


- [ ] **U19** : paramètres et données variables centralisés, valeurs par défaut nommées et documentées, entrées validées ; transport et rendu indépendants des coordonnées de démonstration ; règles fixes justifiées et configuration sauvegardée.


- [ ] **U20** : pour une évolution importante, adaptation et réécriture comparées ; remplacement propre privilégié si l'adaptation est trop coûteuse ou accumule les contournements ; code obsolète retiré, décisions et vérifications pertinentes préservées.


- [ ] **U21** : développement centré sur une seule simulation ; modes de référence et comparaisons reportés, sans imposer deux modèles simultanés.
- [ ] **U22** : état et délais propres à chaque taxi ; scénario contrôlé vérifiant qu'un taxi en arrêt ne bloque ni le déplacement ni la disponibilité des autres.
