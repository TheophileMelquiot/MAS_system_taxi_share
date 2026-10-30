# Sources et provenance

Consultation : **11 octobre 2026**. Les compléments techniques utilisent des sources primaires. Les interprétations de conception sont indiquées comme propositions dans les documents.

Complément documentaire : **19 octobre 2026**. La session 5 a été extraite et ses 10 pages examinées visuellement. Les consultations techniques initiales restent datées du 11 octobre ; elles n'ont pas toutes été renouvelées.

## Énoncé local ajouté : session 5

- [Session 5, projet](sources/session-5.pdf), Nicolas Sabouret, Université Paris-Saclay, M1 DKAI, couverture « September 2026 ».
- 10 pages physiques ; total annoncé de 9 dans les pieds de page, dernière page `10/9`.
- SHA-256 : `d4ef1b963457822c8f83ecbd300a37953516046f3febdbefb09ce22dba5868a8`.
- [Texte et métadonnées](slides-session-5/texte.json), [texte avec images](slides-session-5/texte_integral.md), [index](slides-session-5/README.md), [énoncé commenté](08_projet_session5.md).
- Pages 4 et 5 : organisation, échéance, livrables et barème. Pages 6 et 7 : mission et périmètre. Pages 8 et 9 : recommandations Mesa et JADE.
- Le lecteur PDF signale une définition dupliquée de `/Group` ; l'extraction et le rendu des 10 pages ont néanmoins abouti et ont été vérifiés.

Complément officiel vérifié le 19 octobre : [API des espaces Mesa](https://mesa.readthedocs.io/stable/apis/space.html), pour `mesa.space.MultiGrid`, l'occupation multiple et les méthodes de placement et déplacement. Les choix de ville, de protocole et d'expériences dans le canevas sont des propositions, pas des données extraites.

## Support local

- [Session 4, simulation](sources/session-4.pdf), Nicolas Sabouret, Université Paris-Saclay, M1 DKAI, couverture « September 2026 ».
- 47 pages PDF, 38 numéros de diapositives.
- SHA-256 : `6af98d9be9ac2abca7241093dca7d9cce3703dd5f74d1ae7e027d571a49fc700`.
- [Texte extrait et métadonnées](slides/texte.json), [lecture avec images](slides/texte_integral.md), [correspondance des pages](slides/README.md).

Les références Shannon (1977), Fishwick (1997), « Voltera, 1926 » et W. Ouerdane sont des attributions du support. Le PDF ne donne pas leur bibliographie complète. Les documents originaux n'ont pas été consultés et ces références ne sont pas présentées comme des vérifications indépendantes.

## Documentation officielle consultée

| Source | Usage dans la préparation |
| --- | --- |
| [Mesa sur PyPI](https://pypi.org/project/Mesa/) | Version stable affichée, préversion, Python requis et extras d'installation |
| [Vue d'ensemble Mesa](https://mesa.readthedocs.io/stable/overview.html) | Modélisation, analyse et visualisation |
| [Guide de migration](https://mesa.readthedocs.io/stable/migration_guide.html) | AgentSet, anciennes écritures d'activation et avancement du temps |
| [API Mesa](https://mesa.readthedocs.io/stable/mesa.html) | Constructeurs, aléatoire, enregistrement et retrait des agents |
| [Premier modèle](https://mesa.readthedocs.io/stable/tutorials/0_first_model.html) | Règles du tutoriel d'échange de monnaie |
| [Ajout de l'espace](https://mesa.readthedocs.io/stable/tutorials/4_adding_space.html) | Cellules, voisinages et agents spatiaux |
| [Collecte de données](https://mesa.readthedocs.io/stable/tutorials/5_collecting_data.html) | DataCollector, données individuelles et indicateurs du modèle |
| [Visualisation de base](https://mesa.readthedocs.io/stable/tutorials/6_visualization_basic.html) | SolaraViz, SpaceRenderer, portrayal, paramètres et Colab |
| [FAQ Matplotlib, threads](https://matplotlib.org/stable/users/faq.html#work-with-threads) | Limite de sûreté en concurrence et sérialisation des accès |

Les tutoriels actuellement accessibles ne constituent pas une copie du notebook du prof. Ils peuvent évoluer ou utiliser des exemples légèrement différents. Les pages affichent certains avertissements de dépréciation et des éléments issus de plusieurs étapes de l'évolution de Mesa. Vérifier l'API contre la version réellement utilisée avant de programmer.

## Référence citée par le cours, non vérifiée en ligne

[Erocr/mesa_graphics](https://github.com/Erocr/mesa_graphics) est cité à la diapo 35. Son ouverture par l'outil web a échoué. Le nom de l'auteur, la méthode d'installation et la limitation Windows rapportés dans cette préparation proviennent donc uniquement du support. Aucune disponibilité actuelle, compatibilité précise ou correction du bug Linux n'est affirmée.

## Limites de l'extraction

La couche texte du PDF peut perdre les espacements et l'indentation du code. Elle peut aussi contenir des textes non encore visibles dans une étape d'animation. Les images rendues conservent le contenu visible de chaque page. Les schémas importants ont fait l'objet d'une description séparée, sans inventer des données à partir de captures trop petites.

Les couvertures, titres, listes, formules, exemples, consignes et figures des sessions 4 et 5 sont couverts par les archives et lectures commentées. Les notes orales, les autres séances et le notebook restent absents. L'énoncé du projet est désormais fourni par la session 5 ; le canal de dépôt et les éventuelles précisions orales ne peuvent pas être reconstitués.
