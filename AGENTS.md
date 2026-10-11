# Cadrage du clone YemX

Référence : https://yemxapp.com/ — inspection du DOM et de l’interface dans le navigateur intégré le 11 octobre 2026.

Ce document consigne l’entretien et le cadrage confirmé. Il ne constitue pas une implémentation du site. Les contraintes techniques confirmées sont Django, SQLite, Django admin avec Unfold et un livrable final strictement inférieur à 500 Mo, selon la définition ci-dessous.

## GOALS

### 1. Objectifs fonctionnels prioritaires

- Reproduire l’accueil public complet de YemX, avec toutes les sections cartographiées, son identité, ses textes, son logo et ses captures.
- Prioriser le parcours de compréhension de l’offre puis d’accès aux téléchargements Google Play et APK.
- Permettre la comparaison Gratuit/Pro et l’ouverture du contact WhatsApp, sans envoi automatique.
- Rendre fonctionnels la navigation par ancres, le menu mobile, la galerie avec agrandissement et navigation, les six accordéons FAQ et le changement FR/EN.
- Prioriser la fidélité visuelle mobile, assurer une adaptation desktop fidèle, corriger les icônes et compléter les traductions.
- Valider à 390, 768 et 1440 px : comparaison visuelle, absence de débordement horizontal, contrôle de chaque interaction et navigation clavier.

### 2. Contraintes techniques

- Utiliser Django pour le projet web et SQLite pour sa base de données.
- Utiliser Django admin avec Unfold pour l’interface d’administration ; les fonctions de gestion métier restent exclues.
- Maintenir le livrable final strictement inférieur à 500 Mo, assets et base livrée inclus, hors `.git`, environnement virtuel et caches.
- Conserver les destinations réelles de YemX pour Google Play, APK, WhatsApp, Facebook, exemple PDF et pages légales.
- Résoudre les liens externes relatifs vers leurs URL absolues sur le site original.

### 3. Périmètre strictement Hors-Scope

- Reconstruction de l’application Android ou iOS et de ses écrans métier interactifs.
- Gestion effective des ventes, stocks, clients, crédits, boutiques et équipes ; persistance de données métier.
- Synchronisation cloud, fonctionnement métier hors-ligne et génération de rapports PDF.
- Paiement ou gestion d’abonnements Pro ; envoi automatique de messages WhatsApp.
- Reconstruction locale des quatre pages légales, hébergement des APK et génération de l’exemple PDF.
- Nouvelle marque, nouvelle identité visuelle ou remplacement des captures par une démo métier.
- Implémentation ou publication du site dans cette étape : seule la mise à jour documentaire est prévue.

## PRD — Vitrine YemX

Ce PRD intègre le choix confirmé : contenus administrables avec Django admin et Unfold.

### 1. Vision et utilisateurs

Reproduire fidèlement l’accueil public de YemX pour permettre aux commerçants de comprendre l’offre, télécharger l’application et contacter YemX pour l’offre Pro.

Deux profils utilisent le site :

- **Visiteur** : consulte librement la vitrine, en français ou en anglais, principalement sur téléphone.
- **Administrateur** : maintient les contenus depuis une interface Django admin avec Unfold, accessible après authentification.

Le succès repose sur une vitrine complète, fidèle et utilisable, avec des destinations réelles et des contenus administrables. Aucun compte visiteur ni outil métier n’est requis.

### 2. Exigences fonctionnelles

#### Vitrine publique

- Reproduire toutes les sections cartographiées, dans leur ordre : introduction, problèmes, fonctionnalités, galerie, installation, tarifs, chiffres clés, FAQ, téléchargement, présentation de YemX et footer.
- Conserver la marque, la palette, la typographie, les textes et les captures de référence ; compléter les traductions et corriger les icônes défectueuses.
- Conserver les identifiants des ancres publiques. Les sections ciblées doivent rester visibles malgré le header fixe.
- Proposer un menu mobile ouvrable et refermable ; le choix d’une ancre ferme le menu.
- Présenter Google Play et APK comme destinations actives. Le badge App Store reste une annonce non cliquable.
- Afficher les offres Gratuit et Pro avec les prix, limites et avantages de référence. Le CTA Gratuit rejoint le téléchargement ; le CTA Pro ouvre WhatsApp avec le message prérempli existant, sans l’envoyer.
- Ouvrir chaque capture de la galerie dans une modale avec légende, précédent/suivant et indicateur de position. La navigation boucle entre les quatre captures.
- Permettre la fermeture de la modale par bouton, clic sur le fond ou Échap ; gérer le focus à l’ouverture et le restituer à la fermeture.
- Afficher six FAQ fermées initialement, ouvrables et refermables indépendamment.
- Proposer FR/EN sans modifier les destinations ni réinitialiser la section consultée. Français par défaut ; conserver le choix de langue dans le navigateur.
- Lier PDF, APK, pages légales et services externes à leurs URL absolues sur les destinations originales.

#### Administration

- Permettre aux administrateurs autorisés de modifier textes FR/EN, FAQ, tarifs, avantages, légendes et ordre de la galerie, ainsi que les liens externes.
- Conserver la structure, les ancres et le design dans les templates : l’admin ne devient pas un constructeur de pages.
- Appliquer les modifications enregistrées aux prochaines consultations de la vitrine, sans étape de publication supplémentaire.
- Fournir les contenus initiaux de référence par une commande de chargement reproductible, qui ne remplace pas les modifications existantes par défaut.
- Limiter la gestion des médias à la sélection d’assets locaux fournis avec le projet ; aucun système d’upload ou de traitement d’images n’est requis.

### 3. User Stories et acceptation

| ID | User Story | Critères d’acceptation |
| --- | --- | --- |
| US01 | Comme visiteur, je veux comprendre ce que propose YemX. | Toutes les sections et contenus de référence sont présents et lisibles dans l’ordre prévu. |
| US02 | Comme visiteur Android, je veux installer YemX. | Google Play ouvre la fiche réelle ; les CTA APK utilisent l’URL réelle ; le CTA Gratuit rejoint `#download`. |
| US03 | Comme commerçant, je veux comparer les offres. | Prix, limites et avantages correspondent à la référence ; le CTA Pro ouvre le contact et le message prérempli, sans envoi automatique. |
| US04 | Comme visiteur mobile, je veux atteindre rapidement une section. | Menu et barre fixe fonctionnent ; les ancres ciblent les bonnes sections sans masquer leurs titres. |
| US05 | Comme visiteur, je veux examiner les captures. | Les quatre images s’agrandissent ; précédent/suivant, position et toutes les fermetures fonctionnent ; le focus est géré. |
| US06 | Comme visiteur, je veux obtenir des réponses aux questions courantes. | Six questions disponibles ; chaque réponse s’ouvre et se ferme ; l’état accessible correspond à l’état visible. |
| US07 | Comme visiteur francophone ou anglophone, je veux consulter ma langue. | Tous les textes publics et libellés accessibles sont traduits ; le choix persiste ; les liens restent corrects. |
| US08 | Comme visiteur au clavier, je veux accéder à tous les contrôles. | Ordre de tabulation cohérent, focus visible, activation clavier et absence de piège involontaire. |
| US09 | Comme administrateur, je veux maintenir la vitrine. | Les contenus autorisés sont éditables dans Unfold et leurs modifications apparaissent sur la page publique. |
| US10 | Comme administrateur, je veux protéger l’édition des contenus. | Un visiteur anonyme ne peut pas modifier les données ; les accès administratifs exigent authentification et permissions appropriées. |

Toutes ces stories sont nécessaires en V1. L’ordre de réalisation privilégie téléchargement, tarifs/contact Pro, puis exploration et administration.

### 4. Modélisation logique des données

SQLite stocke uniquement les contenus éditoriaux et les données d’administration. Les médias restent des fichiers statiques locaux.

| Entité | Champs logiques essentiels | Relations et règles |
| --- | --- | --- |
| **Utilisateur administratif** | Utilisateur Django standard, état actif, accès staff, groupes et permissions. | Utiliser l’authentification Django existante ; aucun modèle de compte visiteur. |
| **Texte localisé** | Clé unique et stable, texte FR, texte EN. | Référentiel commun pour titres, paragraphes, boutons, légendes et libellés accessibles ; deux langues requises. |
| **Asset** | Clé unique, chemin statique local, référence du texte alternatif, URL de provenance. | Référence un fichier fourni ; les textes alternatifs sont localisés. |
| **Aperçu** | Clé stable, asset, référence de légende, ordre. | Quatre entrées initiales ; ordre explicite et unique. |
| **FAQ** | Clé stable, références de question et réponse, ordre. | Six entrées initiales ; ordre explicite et unique. |
| **Offre** | Code stable, référence de nom, prix en FCFA, référence de périodicité, mise en avant, ordre, cible CTA. | Deux entrées initiales : Gratuit et Pro ; prix non négatif ; CTA vers téléchargement ou lien externe. |
| **Avantage d’offre** | Offre, référence de texte, ordre. | Plusieurs avantages appartiennent à une offre ; ordre unique dans chaque offre. |
| **Lien externe** | Clé stable, URL HTTPS, référence de libellé. | Centraliser Google Play, APK, WhatsApp, PDF, Facebook et les quatre pages légales. |

Les titres et textes des autres sections utilisent les clés du référentiel de textes localisés. Leurs regroupements et leur placement restent définis dans les templates.

Préserver les références utilisées par la page : les enregistrements structurels et assets requis ne sont pas supprimables depuis l’admin. Valider les URL, prix, traductions et chemins d’assets lors de l’enregistrement. Les contenus sont rendus comme texte échappé ; aucun HTML arbitraire saisi dans l’admin.

Aucune entité Vente, Stock, Client, Crédit, Boutique, Paiement ou Abonnement n’est créée.

### 5. Contraintes et interfaces

- Django, SQLite et Django admin avec Unfold sont obligatoires.
- Utiliser les templates Django, CSS et JavaScript nécessaires aux interactions ; aucune API publique ni application frontend séparée n’est requise.
- Exposer l’accueil sur `/`, l’administration sur `/admin/`, et conserver les ancres de référence.
- Fournir migrations, assets et données initiales nécessaires à une installation reproductible.
- Maintenir le livrable sous **500 000 000 octets**, assets et base livrée compris, hors `.git`, environnement virtuel et caches.
- Ne livrer aucun secret, mot de passe administratif ou identifiant de production.

Les fonctions métier, applications mobiles, paiements, synchronisation cloud, génération PDF, hébergement APK, pages légales locales et changement d’identité restent hors scope. Aucun déploiement n’est inclus dans cette étape documentaire.

### 6. Definition of Done

La future implémentation est terminée uniquement lorsque tous les critères suivants sont démontrés :

- **Installation** : installation depuis les instructions fournies, migrations, chargement initial et démarrage réussis ; contrôles Django sans erreur.
- **Contenu** : toutes les sections, quatre captures, six FAQ, deux offres et traductions FR/EN présents ; aucune image cassée ni nom d’icône affiché à la place d’une icône.
- **Parcours** : chaque User Story validée ; destinations vérifiées sans installer d’APK, effectuer de paiement ou envoyer de message.
- **Responsive** : captures comparatives à 390, 768 et 1440 px, même hauteur de viewport pour le clone et la référence ; aucun débordement horizontal, texte tronqué ou contrôle masqué.
- **Fidélité visuelle** : ordre, proportions, couleurs, typographie, espacements et images comparés à la référence ; écarts documentés et corrigés, hors corrections explicitement prévues.
- **Accessibilité** : contrôles utilisables au clavier, focus visible, modale avec focus contenu et restitué, menu et FAQ avec états accessibles cohérents.
- **Administration** : édition et affichage public vérifiés pour chaque famille de contenus, dans les deux langues ; accès anonyme et édition sans permission refusés.
- **Robustesse** : validation des données invalides vérifiée ; aucun échec serveur ou erreur JavaScript sur les parcours testés ; aucun appel local vers des pages légales ou APK inexistants.
- **Tests** : tests ciblés couvrant rendu initial, contenus localisés, permissions administratives et validations ; vérification navigateur des interactions réelles.
- **Sécurité applicative** : tests d’intrusion locaux reproductibles sur base isolée couvrant charges SQL dans langue, recherche admin et connexion, XSS stockée dans textes/attributs/JSON FR/EN et Unfold, URL actives et chemins traversants, refus CSRF et origine étrangère, fixation et falsification de session, expiration, déconnexion et rejet des redirections externes. Aucun contournement ne doit apparaître dans ces cas ; les protections ORM, échappement et `json_script` doivent être conservées.
- **Configuration de sécurité** : debug désactivé par défaut, démarrage de production refusé sans clé privée forte et hôtes explicites sans joker ; HTTPS obligatoire, HSTS sur le domaine, cookies de session/CSRF `Secure` et `SameSite=Lax`, session `HttpOnly` de huit heures, en-têtes anti-iframe et anti-sniffing, CSP stricte sur l’accueil. Le développement HTTP exige `DJANGO_DEBUG=1` explicite.
- **Réception sécurité du 11 octobre 2026** : conformité du code aux scénarios vérifiés consignée dans `evidence/SECURITY_REPORT.md` et `tests/test_security.py`, avec preuves avant/après. Cette réception ne certifie pas l’absence de toute vulnérabilité ni la conformité d’un déploiement : TLS réel, limitation des essais de connexion, configuration du proxy et suivi des dépendances restent à vérifier avant exposition publique. La CSP de l’admin Unfold n’est pas durcie dans cette passe. Les avertissements de déploiement `security.W005` et `security.W021` (sous-domaines/préchargement HSTS) restent explicitement documentés, non masqués.
- **Livrable** : taille mesurée sous la limite, procédure de mesure documentée, aucun secret embarqué et instructions de lancement disponibles.
- **Preuves** : compte rendu indiquant contrôles effectués, résultats, captures et éventuelles limites ; aucun critère non vérifié présenté comme réussi.

### 7. Vérification de l’insertion documentaire

Vérifier que le PRD suit immédiatement `GOALS`, que les dix User Stories, huit entités et critères de réception sont présents, et que la cartographie ainsi que les neuf questions/réponses sont conservées.

Cette étape modifie uniquement `AGENTS.md`. Les critères de la Definition of Done décrivent la future implémentation ; ils ne sont pas déclarés réussis par l’ajout du PRD.

## Cartographie observée

La page publique est une vitrine de l’application Android. Les écrans de ventes, stocks et crédits sont des captures ; aucun outil métier utilisable n’a été observé sur cette page.

| Zone, dans l’ordre du DOM | Structure et contenu observés |
| --- | --- |
| `header#navbar` | Logo lié à l’accueil, boutons FR/EN, navigation, bouton d’ouverture du menu mobile. |
| `#mobile-menu` | Logo, fermeture et ancres Fonctionnalités, Comment ça marche, Tarifs, FAQ. |
| `main` : introduction | H1 YemX, promesse commerciale, Google Play, App Store bientôt disponible, ancre APK, badge Afrique et capture du tableau de bord. |
| Section des problèmes | H2 « Tu connais ça ? », trois cartes : Cahier raturé, Calculatrice infinie, Dette perdue. |
| `section#features` | Ventes rapides, Stock temps réel, Gestion crédits, Offline-first, Multi-boutiques, Rapports PDF Professionnels ; captures et lien vers un exemple PDF. |
| `section#app-preview` | Quatre boutons d’agrandissement : Tableau de bord, Gestion du stock, Rapport PDF, Journal d’activité. |
| `section#how-it-works` | Trois étapes : Installer YemX, Créer votre boutique, Vendre ! |
| `section#pricing` | Cartes Gratuit (0 FCFA à vie) et Pro (2 500 FCFA/mois), listes de capacités, ancre de téléchargement et lien WhatsApp. |
| Bandeau de chiffres | 100 % offline, boutique créée en 2 min, vente en 3 sec, démarrage à 0 FCFA. |
| `section#faq` | Six boutons d’accordéon et leurs réponses : gratuité, hors-ligne, Google Play/APK, définition APK, iPhone, mises à jour. |
| `section#download` | Google Play, App Store bientôt disponible, téléchargement APK, option Android ancien (32 bits), version affichée « — » et explication APK. |
| `section#about` | Logo, présentation de la startup camerounaise et de sa mission. |
| `footer` | Marque, liens internes, support, Facebook, quatre liens légaux et copyright 2026. |
| Navigation mobile fixe | Fonctions → `#features`, Installer → `#download`, Tarifs → `#pricing`. |

### Interactions et apparence observées

- Menu mobile : ouverture vérifiée, liens internes et bouton de fermeture présents.
- FR/EN : changement de langue observé ; certains textes et libellés accessibles restent en français en anglais.
- Galerie : ouverture de `#preview-modal` vérifiée visuellement ; capture agrandie, légende, fond assombri, fermeture, boutons précédent/suivant et indicateurs présents. Le parcours complet précédent/suivant n’a pas été vérifié.
- FAQ : six contrôles d’accordéon présents. Un clic a été effectué, mais le relevé immédiat indiquait encore `aria-expanded="false"` ; l’expansion effective n’a pas été confirmée.
- Ancres internes et liens externes relevés ; les téléchargements et services externes n’ont pas été exécutés.
- Vue initiale : fond clair, palette verte, titres noirs épais, captures de téléphone, barre mobile fixe. Plusieurs noms d’icônes apparaissaient comme du texte dans la vue initiale.
- Les largeurs de validation définies ci-dessous n’ont pas fait l’objet d’une comparaison visuelle complète lors de cet entretien.

### Destinations publiques relevées

- Google Play : https://play.google.com/store/apps/details?id=com.yemxapp.app
- APK principal et option 32 bits : https://yemxapp.com/apk/yemx-latest.apk
- Exemple PDF : https://yemxapp.com/docs/exemple-rapport.pdf
- Offre Pro : https://wa.me/237694208641?text=Bonjour%2C%20je%20suis%20int%C3%A9ress%C3%A9(e)%20par%20l%27offre%20Pro%20de%20YemX.
- Facebook : https://www.facebook.com/people/YemX/61572368152527/
- Mentions légales : https://yemxapp.com/mentions-legales.html
- Confidentialité : https://yemxapp.com/politique-confidentialite.html
- Termes et Conditions : https://yemxapp.com/cgu.html
- CGV : https://yemxapp.com/cgv.html

## Entretien : questions exactes et réponses

### Q1 — Périmètre

« Cloner YemX » est trop flou pour construire quoi que ce soit : acceptes-tu de limiter la V1 à la vitrine publique complète, avec ses interactions, sans reconstruire l’application de gestion montrée dans les captures ?

**Réponse :** Vitrine complète (Recommended)

### Q2 — Réussite

Périmètre verrouillé : vitrine complète. Maintenant tranche : si je dois arbitrer, acceptes-tu que la fidélité visuelle mobile passe avant le desktop, puisque la page vend une application utilisée sur téléphone ?

**Réponse :** Mobile fidèle (Recommended)

### Q3 — Conversion

Un clone avec des boutons décoratifs échoue sur son parcours principal. Acceptes-tu que les CTA Google Play, APK et WhatsApp conduisent aux destinations réelles de YemX, plutôt que de simuler un téléchargement ou une prise de contact ?

**Réponse :** Liens réels (Recommended)

### Q4 — Fidélité

Le passage en anglais laisse certains textes français, et plusieurs icônes apparaissent comme des mots dans la vue observée. Acceptes-tu de reproduire le design voulu en corrigeant ces défauts, plutôt que de copier les anomalies du site ?

**Réponse :** Corriger les défauts (Recommended)

### Q5 — Pages

« Vitrine complète » peut multiplier le travail : acceptes-tu que les quatre liens légaux ouvrent les pages originales, et que seule la page d’accueil soit reconstruite localement ?

**Réponse :** Accueil seul (Recommended)

### Q6 — Identité

La fidélité ne survivra pas à des captures génériques. Acceptes-tu de conserver le nom YemX, ses textes, son logo et ses captures publiques comme références et assets du clone, sans nouvelle identité visuelle ?

**Réponse :** Conserver YemX (Recommended)

### Q7 — Parcours

Qu’est-ce qui doit être irréprochable le jour de la livraison ? Acceptes-tu cet ordre : 1) comprendre l’offre et atteindre Google Play/APK, 2) comparer Gratuit/Pro et ouvrir WhatsApp, 3) parcourir captures, FAQ et FR/EN — avec tous les parcours fonctionnels dès la V1 ?

**Réponse :** Cet ordre (Recommended)

### Q8 — Validation

« Ça ressemble » ne suffit pas. Acceptes-tu une validation visuelle à 390 px, 768 px et 1440 px, sans débordement horizontal, puis un contrôle de chaque CTA, menu, galerie, accordéon et traduction, avec navigation clavier sur les contrôles ?

**Réponse :** Oui, ces critères (Recommended)

### Q9 — Accord

Dernier verrou : confirmes-tu le cadrage — accueil YemX complet, priorité mobile, assets d’origine, défauts corrigés, liens externes réels, aucune application métier ni page légale locale, validation aux trois largeurs — et un AGENTS.md contenant la carte DOM, les neuf questions et tes réponses ?

**Réponse :** Oui, cadrage confirmé (Recommended)

## Exigences confirmées pour le futur clone

1. Reproduire uniquement l’accueil public complet, toutes ses sections et interactions. Exclure l’application de gestion et les données métier persistantes.
2. Prioriser la fidélité mobile ; assurer ensuite une adaptation desktop fidèle et responsive.
3. Conserver les destinations réelles Google Play, APK et WhatsApp. Ouvrir le contact Pro sans envoyer automatiquement de message.
4. Afficher de vraies icônes et compléter la traduction anglaise, en conservant le design et le sens des contenus.
5. Lier les quatre pages légales et l’exemple PDF au site original ; ne pas les reconstruire localement. Résoudre leurs liens relatifs vers les URL absolues de la référence.
6. Conserver YemX, ses textes, son logo, ses captures publiques, sa palette et sa typographie comme références et assets de réplication.
7. Prioriser les parcours : comprendre l’offre et télécharger → comparer Gratuit/Pro et ouvrir WhatsApp → explorer galerie, FAQ et FR/EN. Tous restent fonctionnels dès la V1.
8. Comparer visuellement à la référence à 390, 768 et 1440 px ; vérifier l’absence de débordement horizontal, chaque CTA, menu, galerie, accordéon, traduction et l’utilisation des contrôles au clavier.
9. Le cadrage et le contenu prévu de ce document ont été explicitement confirmés lors de Q9.

Ces critères sont des exigences de réception du futur clone, pas des tests déjà réussis. La présente étape se limite à mettre à jour et vérifier ce document ; elle consigne les contraintes techniques confirmées dans GOALS, n’implémente pas le site et ne le publie pas. Après cette mise à jour, arrêter le travail et attendre la validation de l’utilisateur avant toute suite.

## Revue visuelle autorisée — 11 octobre 2026

La demande ultérieure de l’utilisateur autorise explicitement l’exécution du projet existant, son ouverture dans le Browser Plugin intégré et les retouches graphiques. Le cadrage documentaire ci-dessus reste conservé comme historique. Cette passe ne publie pas le site.

### Modifications de style

Les ajustements sont limités à `showcase/static/showcase/site.css`, entre 768 et 1000 px. La palette, Lexend, les assets, les textes et les destinations sont conservés.

- **Introduction :** les colonnes peuvent désormais se réduire (`min-width: 0`) ; leur intervalle passe de 48 à 32 px. Avant correction, la colonne du téléphone atteignait x = 756 px pour une largeur utile de 753 px à 768 px : le recadrage horizontal masquait le défaut. Après correction, les deux colonnes occupent 336,5 px chacune, entre les marges de 24 px. Le téléphone réserve 28 px pour ses boutons latéraux et conserve son ratio 320/660.
- **Typographie tablette :** la promesse du H1 passe de 48 à 40 px pour éviter le mot « des » isolé sur une ligne. Le nom YemX conserve sa taille. Les tailles mobile (30 px) et desktop (60 px) de la promesse restent inchangées.
- **Badges et liens de l’introduction :** retour à la ligne selon l’espace disponible, sans réduire les badges ni leurs libellés, en FR comme en EN.
- **Téléchargement :** marge intérieure du contenu ramenée de 56 à 32 px sur tablette ; colonne visuelle stable avec 24 px de marge intérieure. Les badges peuvent revenir à la ligne. Le téléphone s’adapte proportionnellement (ratio 200/412), au lieu de réduire uniquement sa largeur. À 768 px, les colonnes mesurent 470 et 235 px ; aucune ne dépasse sa largeur allouée.

### Contrôles observés

Serveur Django démarré sur `http://127.0.0.1:8000/` et page affichée dans le navigateur intégré. Comparaison des accueils avec `https://yemxapp.com/` à 390, 768 et 1440 px, hauteur 844 px. La référence présente elle-même un débordement sur tablette ; les retouches privilégient l’absence de recadrage exigée par le PRD. Galerie tablette, fonctionnalités mobiles, tarifs mobiles, FAQ et téléchargement tablette inspectés visuellement.

Mesures après correction, dans les deux langues : largeur utile / largeur du document de 375/375, 753/753 et 1425/1425 px respectivement. Aucune image cassée détectée. Données dans `evidence/visual/review-metrics.json` ; captures `review-390-intro.jpg`, `review-768-intro.jpg`, `review-768-download.jpg`, `review-1440-intro.jpg` et `review-reference-1440-intro.jpg` dans le même dossier.

Interactions recontrôlées : ouverture du menu mobile, choix Tarifs avec fermeture et focus sur la section ; passage de la première à la quatrième capture par précédent, retour par suivant, fermeture avec Échap et restitution du focus au déclencheur ; ouverture simultanée des six FAQ avec six états `aria-expanded="true"` ; changement FR/EN aux trois largeurs. Aucun avertissement ou erreur capturé dans la console de la vue desktop.

Validation automatisée après les retouches : `.venv/Scripts/pytest.exe -q` donne **50 tests réussis** ; `manage.py check` ne signale aucun problème. Mesure du livrable par `scripts/measure_delivery.py` : environ **6,81 Mo**, sous 500 000 000 octets, selon les exclusions prévues. Le serveur reste actif pour la consultation locale.

Limites : comparaison visuelle manuelle, sans certification pixel à pixel de toutes les sections ni audit complet de la Definition of Done. Les téléchargements et messages externes n’ont pas été déclenchés. Les vérifications historiques plus étendues restent dans `evidence/FRONTEND_REPORT.md`.
