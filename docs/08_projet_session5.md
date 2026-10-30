# Session 5 : énoncé commenté du projet

Source : [session-5.pdf](sources/session-5.pdf), Nicolas Sabouret, Université Paris-Saclay, M1 DKAI, couverture « September 2026 ». Extraction et examen visuel des 10 pages : 19 octobre 2026. Le [texte intégral avec images](slides-session-5/texte_integral.md) conserve la formulation anglaise. La dernière page affiche `10/9` : les références ci-dessous utilisent les pages physiques.

## Pages 1 à 3 : contexte

La couverture annonce la session 5 consacrée au projet. Le calendrier situe cette séance MABS au 12 octobre 2026 et la séance Agentic AI au 19 octobre. La page 3 annonce Mesa ou JADE. Le calendrier de séance et la date de remise sont distincts.

## Page 4 : organisation et échéance

**Projet S5** : étudier un problème concret par simulation multi-agents.

- Groupes de **1 ou 2 étudiants**.
- Travail annoncé : **6 h par étudiant**, 3 h en séance et 3 h à la maison.
- Développement : **Python avec Mesa** ou **Java avec JADE**.
- Autres plateformes MAS (Repast, Gama, etc.) : **interdites**.
- Système multi-agents maison sans bibliothèque : **interdit**.
- Remise : **dimanche 25 octobre 2026 à 23 h 59 CET**, selon la date et le fuseau indiqués dans le support.

Le canal de dépôt et le format d'archive ne sont pas précisés.

## Page 5 : livrables et barème

**Projet S5** : rendre le **code source** et un **rapport**. Le support écrit « 5-10 pages max report ». Viser 5 à 10 pages, avec un plafond de 10, est une lecture pratique ; aucune règle sur la couverture ou les annexes n'est donnée.

| Critère | Poids | Attendu explicite |
| --- | --- | --- |
| Choix de conception | 20 % | Explications dans le rapport |
| Implémentation | 20 % | Code et utilisation correcte de la bibliothèque |
| Fonctionnalités et utilisabilité | 20 % | Le professeur exécutera les programmes |
| Analyse | 20 % | Résultats de simulation dans le rapport |
| Présentation générale | 20 % | Organisation du rapport, commentaires du code, etc. |

La note est sur 20, soit 4 points par catégorie par conversion des pourcentages. Aucun sous-barème n'est fourni.

**Proposition** : fournir une installation reproductible, une commande de lancement et une courte expérience réexécutable. Ce sont des moyens de faciliter l'évaluation, pas des formats imposés.

## Page 6 : mission et méthode

**Projet S5** : une municipalité veut réduire la pollution en testant une solution de partage de taxis. Évaluer son impact possible sur le **trafic**, le **temps de trajet des passagers** et l'**acceptabilité**.

Le professeur demande une conception **incrémentale**, l'identification des paramètres **dès le début**, une question exprimée avec des **variables observables**, et un modèle très simple.

La progression donnée comme exemple est :

1. Un seul passager par taxi.
2. Deux passagers sans changement d'itinéraire.
3. Deux passagers avec changement d'itinéraire et « multi-hop ».
4. Plusieurs passagers et plusieurs étapes.

La liste est introduite par « e.g. » ; tous les niveaux ne sont pas explicitement exigés. **Proposition** : terminer et analyser les deux premiers niveaux avant les extensions. Si le « multi-hop » est retenu, préciser si cela signifie des correspondances entre taxis ou seulement des étapes d'itinéraire ; le support n'en fixe pas la sémantique.

La pollution motive le projet, mais aucune formule d'émissions n'est fournie. **Proposition** : mesurer la distance totale parcourue par les taxis comme indicateur indirect et expliciter cette limite.

## Page 7 : décisions de modélisation

Le support invite à définir :

- Les voitures et passagers dans une ville simplifiée, par exemple une cellule de multigrille par quartier.
- Les mouvements des personnes, avec la marche entre quartiers comme possibilité.
- Le partage et l'itinéraire individuel de chaque passager.
- Les délais pour rejoindre un nouveau passager.
- La représentation du temps de trajet.
- L'acceptabilité, explicitement **optionnelle** ici.
- Les embouteillages, explicitement **optionnels**.

L'acceptabilité figure dans la mission générale, puis est rendue optionnelle dans ces questions. Le rapport doit indiquer si elle est étudiée. Une mesure de trafic n'exige pas un modèle d'embouteillage : l'activité des véhicules peut servir dans une première version simple.

## Page 8 : branche Mesa

**Projet S5** :

- Utiliser **`MultiGrid`** pour plusieurs voitures, passagers ou bâtiments dans une cellule.
- Ne pas nécessairement traiter la grille comme une carte détaillée. Un quartier peut occuper une ou plusieurs cellules ; des cellules peuvent représenter des connexions ou autoroutes.
- Les véhicules peuvent sauter des cellules. Un compteur interne peut représenter la durée du saut selon la vitesse, la taille du quartier ou la distance. Un déplacement détaillé nécessiterait du routage.
- Une **communication directe minimale est requise** : appel de taxi par **CFP et réponses**.
- Utiliser une **visualisation dès le début**, avec positions et graphiques.

CFP désigne un appel à propositions. **Proposition** : demande du passager, offres des taxis, choix et confirmation d'une réservation. Le support ne fixe pas le protocole complet, les délais, les refus ou les règles de réservation. Une file de messages personnalisée dans Mesa est compatible avec cette demande ; elle ne remplace pas la bibliothèque de simulation.

## Page 9 : branche JADE

**Projet S5** : ne pas développer d'interface utilisateur. Écrire les variables dans un fichier, puis utiliser un tableur. Les quartiers sont des agents, éventuellement aussi les connexions ou autoroutes. Employer des temporisations pour vitesse, trafic et embarquement ; le support cite `WakerBehaviour`. Vérifier la consommation CPU.

Ces consignes concernent JADE. En Mesa, la visualisation reste demandée.

## Page 10 : lancement

La dernière page invite à commencer et n'ajoute aucune exigence.

## Proposition de rapport court

| Partie | Contenu proposé | Volume indicatif |
| --- | --- | --- |
| Question et périmètre | Mission, comparaison, simplifications | 0,5 à 1 page |
| Conception | Agents, espace, temps, messages et hypothèses | 1,5 à 2 pages |
| Implémentation et utilisation | Bibliothèque, architecture, lancement et interface | 1 page |
| Expériences et résultats | Paramètres, mesures, figures et dispersion | 1,5 à 3 pages |
| Discussion | Compromis trafic/temps, limites et conclusion | 0,5 à 1 page |

Ce plan n'est pas imposé. Les résultats doivent provenir d'exécutions réelles. La [synthèse de conception](04_canevas_conception.md) présente les choix actuels ; le [plan expérimental proposé](11_priorites_et_experiences.md) précise les résultats à produire.
