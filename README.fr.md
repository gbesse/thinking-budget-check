# Thinking Budget Check

**Mesurez si le raisonnement améliore assez vos décisions sur tickets pour justifier l’attente.**

[English](README.md) · Français · [Español](README.es.md)

## Voir le problème en une commande

```sh
python3 compare.py demo --lang fr
```

Les réponses et latences de la fixture à deux tickets sont fictives ; elle ne mesure pas Jeeves.

## Projets voisins

- [PostHog/jeeves](https://github.com/PostHog/jeeves) — Son option `options.think` et son API locale compatible Jev sont l’intégration directe.
- [fstandhartinger/jevbench](https://github.com/fstandhartinger/jevbench) — Compare déjà des modèles en précision, vitesse et coût ; cet outil compare seulement les modes de raisonnement d’un modèle sur vos cas. Aucune affiliation.

## Utiliser vos données

```sh
python3 compare.py run --cases fixtures/cases.json --endpoint http://127.0.0.1:8009 --lang fr
```

Démarrez Jeeves et indiquez son URL locale. Chaque cas `choice` étiqueté est envoyé deux fois à `/v1/systemone`, avec `options.think` désactivé puis activé. Le contrôle donne la précision et la latence médiane de chaque mode ; il ne choisit pas une politique à votre place.

## Périmètre et limites

Un serveur Jeeves réel exige des poids et du matériel compatibles. Deux requêtes successives ne suppriment pas la variance liée au chargement ou à la charge ; répétez les essais avant toute décision. `--token-env NAME` est facultatif.

## Tests

```sh
python3 -m unittest discover -s tests -v
```

Python 3.11+. Licence MIT. La démo ne demande ni compte ni clé API.
