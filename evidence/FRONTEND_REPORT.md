# Validation des templates et assets — 11 octobre 2026

## Réalisation

Le template Django reprend l'ordre et les classes de la page YemX observée : introduction, problèmes, fonctionnalités, galerie, installation, tarifs, chiffres, FAQ, téléchargement, présentation et footer. Les enregistrements Django fournissent les textes, traductions, offres, avantages, captures, FAQ et destinations. Les données JSON de traduction sont échappées avec `json_script` ; le JavaScript utilise `textContent`.

Les captures et le logo WebP, Lexend avec licence OFL, le sprite SVG Tabler avec licence MIT, les utilitaires CSS de référence et les adaptations locales sont servis sous `/static/showcase/`. Aucun CDN de police ou d'icônes n'est requis. Le script ne télécharge pas d'APK ni ne contacte WhatsApp automatiquement.

La compétence Taste est appliquée en préservation de la référence. Le générateur `scripts/build_reference_template.py` conserve une source reproductible du template ; les adaptations CSS sont dans `showcase/static/showcase/site.css`.

## Tests et installation

- Les premiers tests de structure, assets et traduction accessible ont échoué avant implémentation : `15-templates-red.txt` et `16-about-localization-red.txt`.
- La suite complète finale : **50 tests réussis** (`17-frontend-final-tests.txt`). Les tests ciblés des templates ont également été relancés après les dernières corrections CSS : **3 réussis**.
- `manage.py check` : aucun problème ; `makemigrations --check --dry-run` : aucun changement.
- `collectstatic --noinput` : collecte réussie de 172 fichiers. Trois noms de scripts admin sont communs à Unfold et Django ; l'ordre des applications donne la priorité à Unfold.
- Serveur Django local exécuté sur `http://127.0.0.1:8000/`.

## Observations dans le Browser Plugin

Comparaisons visuelles effectuées dans le navigateur intégré, hauteur de viewport 844 px : accueil aux trois largeurs 390, 768 et 1440 px ; fonctionnalités et tarifs sur desktop ; téléchargement sur tablette ; galerie sur desktop/tablette ; tarifs, FAQ, modale, présentation et footer sur mobile. Les captures sont dans `visual/`. Les captures de référence prises pendant l'animation ou avant stabilisation des images ne constituent pas des mesures pixel à pixel.

| Viewport | Largeur disponible | Largeur du document | Images cassées |
| --- | --- | --- | --- |
| 390 × 844 | 375 | 375 | 0 |
| 768 × 844 | 753 | 753 | 0 |
| 1440 × 844 | 1425 | 1425 | 0 |

La différence de 15 px correspond à la barre de défilement du navigateur. Mesures enregistrées dans `visual/browser-metrics.json`. Aucun débordement horizontal du document observé aux trois largeurs.

Corrections issues de l'inspection visuelle : centrage des barres fixes, réduction du menu desktop sur tablette, redimensionnement proportionnel des quatre téléphones à 768 px, hauteur de la modale, taille des icônes et interlignes, suppression des halos absents du rendu de référence, décalage de 96 px des ancres, fond du header et lisibilité du contact dans le footer mobile.

Parcours réellement exercés :

- Menu mobile : ouverture, fermeture sur choix de Tarifs, état `aria-expanded`, focus sur la section.
- Galerie : quatre images, boucle suivant et précédent, légende et position, fermeture par bouton, Échap et fond ; restitution du focus au déclencheur. Un défaut de bouclage du focus a été constaté, corrigé, puis recontrôlé avec Tab.
- FAQ : ouverture simultanée des six réponses, fermeture indépendante et états accessibles synchronisés ; initialement fermées après rechargement.
- FR/EN : conservation de `#faq`, traduction des libellés et de la présentation, persistance après rechargement et retour à la racine ; retour au français vérifié.
- Lecture des logs navigateur sur le rendu final : aucun avertissement ou erreur capturé.

## Écarts et limites

La navigation desktop ajoute FAQ, conformément aux vues déjà validées. Le prix Pro est affiché `2500 FCFA`, sans espace de groupement, conformément au contrat backend testé. Le paragraphe de mission provient du contenu éditorial déjà livré ; il est traduit et administrable, mais diffère du deuxième paragraphe original. Les icônes SVG corrigent les mots d'icônes visibles sur certains chargements de la référence. La mise en page tablette est ajustée pour éviter le débordement constaté sur le site original.

Les comparaisons sont manuelles, pas une certification pixel à pixel de chaque section dans chaque langue. Aucun audit Lighthouse, lecteur d'écran, autre navigateur ou formulaire admin complet n'a été exécuté dans cette étape. Les destinations sont couvertes par les tests de rendu ; aucun téléchargement, paiement ou envoi de message n'a été déclenché. Le rapport backend `REPORT.md` est conservé comme compte rendu historique ; ses points frontend reportés sont complétés ici. La Definition of Done globale du PRD n'est pas déclarée entièrement validée.

Pour reproduire les contrôles automatisés : suivre `README.md`, exécuter `.venv/Scripts/pytest.exe -q`, puis ouvrir le serveur local. La taille finale, base, preuves et assets collectés inclus, est enregistrée dans `delivery-size.txt` avec la procédure `scripts/measure_delivery.py`.
