# Documentation pour comprendre TaxiShare et préparer le rapport

Ce dossier rassemble les notes du dossier parent, les consignes du professeur,
les choix de conception, l’historique et les résultats disponibles. Import du
30 octobre 2026 : les originaux du parent sont conservés, les liens sont adaptés
au dépôt et les images ainsi que les PDF sources sont copiés à l’identique.
Ce travail organise les matériaux de rédaction ; il ne constitue pas le rapport.

## Par où commencer pour le rapport

1. Lire [l’énoncé commenté de la session 5](08_projet_session5.md) et les
   [consignes du professeur](02_consignes_prof.md) : objectifs, livrables,
   barème et distinction entre exigences et exemples.
2. Utiliser les [décisions techniques actuelles](technical-decisions.md) et
   la [couverture des règles](rules-coverage.md) pour décrire le programme.
   La [synthèse de conception](04_canevas_conception.md) conserve les motivations
   et distingue la cible consolidée de l’ancienne démonstration.
3. Consulter les [vérifications et résultats](validation.md), puis les
   [tableaux comparatifs versionnables](results/capacity-comparison/README.md).
   Les tests valident le fonctionnement ; les simulations fournissent les
   observations à analyser. Les anciennes valeurs sans demi-tour restent
   historiques et ne doivent pas être mélangées aux résultats actuels.
4. Revenir au [cours sur la simulation](01_cours_complet.md), à
   [l’analyse des figures](06_analyse_visuelle.md) et aux [sources](07_sources.md)
   pour expliquer la méthode et citer les supports.
5. Utiliser le [registre des décisions](10_decisions_et_reprise_llm.md) pour
   retrouver la provenance et les changements de choix. La
   [checklist](05_checklist.md) aide à relire la remise ; ses cases historiques
   ne sont pas des résultats de validation actuels.

## Références actuelles et contenu historique

Pour le fonctionnement réellement implémenté, le code et les trois documents
`technical-decisions.md`, `rules-coverage.md` et `validation.md` font référence.
Les documents importés conservent leurs dates et leurs anciens statuts : une
phrase « non implémenté » ou « comparaison reportée » peut décrire une étape
passée. Les propositions du professeur, de l’utilisateur et de l’assistant
restent distinguées dans le registre ; elles ne deviennent pas toutes des
exigences du sujet.

| Document | Contenu et statut |
| --- | --- |
| [technical-decisions.md](technical-decisions.md) | Architecture et conventions du moteur actuel |
| [rules-coverage.md](rules-coverage.md) | Correspondance entre règles, code et vérifications |
| [validation.md](validation.md) | Vérifications exécutées et résultats datés, avec historique |
| [results/capacity-comparison](results/capacity-comparison/README.md) | Étude actuelle : cinq paires capacité 1 / 3, tableaux et provenance |
| [01_cours_complet.md](01_cours_complet.md) | Lecture commentée de la session 4 |
| [02_consignes_prof.md](02_consignes_prof.md) | Exigences et recommandations du professeur |
| [03_guide_mesa.md](03_guide_mesa.md) | Guide historique : versions et commandes anciennes, à ne pas appliquer au code actuel |
| [04_canevas_conception.md](04_canevas_conception.md) | Conception consolidée, puis descriptions historiques clairement séparées |
| [05_checklist.md](05_checklist.md) | Points de relecture du projet et de la remise |
| [06_analyse_visuelle.md](06_analyse_visuelle.md) | Description des figures du cours et du sujet |
| [07_sources.md](07_sources.md) | Provenance, empreintes des supports et consultations datées |
| [08_projet_session5.md](08_projet_session5.md) | Énoncé commenté du projet et barème |
| [09_modele_implemente.md](09_modele_implemente.md) | Ancienne démonstration, conservée comme historique |
| [10_decisions_et_reprise_llm.md](10_decisions_et_reprise_llm.md) | Registre de provenance et de décisions ; contient les choix remplacés |
| [11_priorites_et_experiences.md](11_priorites_et_experiences.md) | Anciennes propositions de progression et d’expériences |
| [archives/](archives/) | Premiers guides et canevas, historiques |

## Supports du professeur

Les supports sont conservés pour consulter les consignes et citer les pages,
sans changer leurs contenus ni leurs auteurs.

- [Session 4, PDF original](sources/session-4.pdf),
  [index des pages](slides/README.md), [texte avec images](slides/texte_integral.md)
  et [extraction JSON](slides/texte.json).
- [Session 5, PDF original](sources/session-5.pdf),
  [index des pages](slides-session-5/README.md),
  [texte avec images](slides-session-5/texte_integral.md) et
  [extraction JSON](slides-session-5/texte.json).
- [Provenance des copies PDF](sources/README.md).

Les textes extraits peuvent perdre l’indentation et les espacements. Pour une
figure ou une formulation exacte, consulter le PDF ou l’image de la page.
Les consultations techniques historiques ne sont pas de nouvelles vérifications
sur la version actuelle de Mesa.

## Périmètre actuel à garder en tête

Le modèle utilise Mesa 3.3.1, une ville générée 21 × 21 par défaut, un pas de
0,2 s et des portions de 100 m. Les demi-tours sont autorisés aux frontières de
cellules, sans interrompre une action engagée. La congestion reste séparée par
sens. Les comparaisons utilisent les mêmes entrées entre capacités, les budgets
individuels et les engagements restent protégés. Les correspondances entre taxis
et le calcul d’émissions restent hors périmètre. Le [README du projet](../README.md)
contient les commandes actuelles d’installation et d’exécution.
