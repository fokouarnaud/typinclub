# Vérification backend YemX

Travail du 11 octobre 2026, à partir du PRD de `AGENTS.md`. Les instructions documentaires antérieures sont conservées ; la demande actuelle autorise la réalisation autonome du backend.

## Résultat

La dernière suite exécutée, `.venv/Scripts/pytest.exe -q --tb=short`, donne **47 tests réussis**, sans avertissement. Django 5.2.18, SQLite et Unfold 0.108.0 sont installés dans le venv. Les migrations, `seed_content`, `manage.py check` et la recherche de migrations manquantes ont été exécutés avec succès.

Le serveur local a répondu en HTTP 200 pour l’accueil français, l’accueil anglais, une nouvelle consultation conservant le choix anglais, la connexion admin et les assets. Les résultats sont consignés dans `http-smoke.txt`. Aucun téléchargement APK, paiement, envoi WhatsApp ou déploiement n’a été effectué.

## Cycles TDD observés

Chaque paire de fichiers `*-red.txt` / `*-green.txt` contient la sortie réelle de pytest. La suite complète a été relancée après chaque lot de modifications de tests ou d’implémentation.

| Cycle | Échec observé avant implémentation | Résultat du cycle |
| --- | --- | --- |
| 01 | Modèle éditorial absent | Modèle et validation FR/EN présents, 1 test réussi |
| 02 | Entités relationnelles absentes | Relations, contraintes de prix/ordre, URL HTTPS et assets locaux, 10 réussis |
| 03 | Commande de chargement absente | Chargement reproductible préservant les éditions, 11 réussis |
| 04 | Accueil absent : 404 | Rendu éditorial échappé, sections et refus POST, 13 réussis |
| 05 | Liens de téléchargement absents | Destinations Google Play/APK/PDF/légales, 14 réussis |
| 06 | Aucune offre rendue | Prix, limites et CTA Gratuit/Pro, 15 réussis |
| 07 | Aucune capture ni FAQ rendue | Galerie ordonnée et six FAQ, 17 réussis |
| 08 | Sélection EN ignorée | Langue rendue et persistée en cookie, 19 réussis |
| 09 | Modèles non enregistrés dans l’admin, routes absentes | Édition Unfold, accès refusés et protection contre suppression, 35 réussis |
| 10 | Avantage modifié dupliqué par le second chargement | Identifiant stable préservant texte et ordre, 36 réussis |
| 11 | Navigation sémantique absente | Ancres, navigation et accès au contenu, 37 réussis |
| 13 | Libellé de lien modifié non rendu | Libellés des liens lus dans les données, 46 réussis |
| 14 | Utilisateur/groupe avec formulaires Django non Unfold | Formulaires Unfold, 47 réussis |

Les tests du lot 12 complètent la couverture de comportements déjà présents : édition via POST admin de chaque famille, visibilité publique FR/EN, permission limitée à un seul modèle, validation administrative et protection CSRF. Ce lot a réussi immédiatement ; il constitue une vérification complémentaire, pas un cycle rouge/vert.

Les premiers échecs d’existence de modèles, de commande et de routes établissent leurs prérequis. Les tests verts vérifient ensuite leurs validations et comportements. Aucun échec de syntaxe ou de dépendance n’est présenté comme une preuve de comportement métier. Les avertissements transitoires Django sur les formulaires URL ont été corrigés en configurant explicitement le schéma HTTPS des champs concernés.

## Couverture du PRD et limites

| Story | Partie backend vérifiée | Partie non vérifiée ou reportée |
| --- | --- | --- |
| US01 | Rendu des textes, ordre des sections, échappement | Fidélité visuelle intégrale et comparaison des captures |
| US02 | Liens publics absolus, badge App Store non cliquable | Ouverture effective des stores et téléchargement des APK |
| US03 | Offres, prix, avantages, ancre et lien WhatsApp prérempli | Disponibilité du service WhatsApp |
| US04 | Ancres et navigation sémantique servies | Menu mobile, fermeture et barre mobile fixe |
| US05 | Quatre captures locales, ordre, textes alternatifs et légendes | Modale, boucle, fermeture et gestion du focus |
| US06 | Six questions/réponses, fermées initialement via HTML natif | Remplacement par les accordéons visuels de référence et contrôle navigateur |
| US07 | FR/EN, cookie, langue invalide, liens conservés | Conservation de la section lors du changement de langue et audit de tous les libellés accessibles |
| US08 | Liens sémantiques, accès direct au contenu et CSS de focus | Parcours clavier réel et focus de la future modale |
| US09 | Édition de toutes les familles, affichage immédiat FR/EN, seed non destructif, sélection d’assets locaux | Vérification manuelle dans le navigateur de chaque formulaire |
| US10 | Authentification, permissions limitées, refus des mutations et suppressions, CSRF | Configuration et exploitation en production |

La compétence design-taste-frontend a guidé la préservation de la marque, la palette verte, la police Lexend auto-hébergée et les assets réels. Le template demeure un aperçu backend, pas la vitrine fidèle achevée. Aucun critère de comparaison à 390, 768 ou 1440 px, de Lighthouse ou de navigation clavier réelle n’est déclaré réussi.

## Taille et reproductibilité

La commande `.venv/Scripts/python.exe scripts/measure_delivery.py` mesure tous les fichiers, base SQLite et preuves compris, hors `.git`, environnements virtuels et caches. La mesure avant ce compte rendu était **1 080 979 octets**, strictement sous 500 000 000 octets ; la dernière mesure est conservée dans `delivery-size.txt`.

Les dépendances sont figées dans `requirements.txt`. La base locale ne contient aucun utilisateur précréé. Une installation neuve se reconstruit depuis les migrations et données livrées. Les paramètres locaux utilisent une clé éphémère en absence de variable privée ; la procédure de configuration est dans `README.md`.
