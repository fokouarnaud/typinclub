# Publication PythonAnywhere — 11 octobre 2026

L’utilisateur a autorisé les commits sur develop, la fusion vers main, leur publication GitHub et le déploiement. Le compte cible a été confirmé : **typinclub**. La session préexistante ventisax n’a pas été utilisée pour modifier ses fichiers ou son application.

## Résultat observé

- Accueil public : https://typinclub.pythonanywhere.com/ ; administration : https://typinclub.pythonanywhere.com/admin/.
- Code applicatif publié depuis la fusion `b6a9e3b`, avec les commits `c8aba61` et `4e80f6c` sur develop.
- Clone dans `/home/typinclub/typinclub`, Python 3.13.1 et virtualenv `/home/typinclub/.virtualenvs/yemx`.
- WSGI PythonAnywhere configuré avec `config.production` ; source, dossier de travail, virtualenv et mapping `/static/` enregistrés dans Web ; Force HTTPS activé ; rechargement effectué.
- `.env` généré sur le serveur avec une clé Django aléatoire privée et le SMTP demandé. Permissions observées : `600`. Les secrets ont été saisis dans des invites masquées, sans commande Bash contenant leur valeur. Aucun secret ni fichier SQLite n’est versionné.
- Migrations appliquées et chargement initial effectué : **121 textes, 6 FAQ, 2 offres, 4 captures**. Les données initiales ont aussi été vérifiées dans SQLite localement.
- Compte `fokou` créé avec l’adresse de réception demandée. Le mot de passe fourni par l’utilisateur reste uniquement sous forme hachée dans SQLite.
- Après le mot de passe, l’administration a demandé un OTP. Gmail a accepté l’envoi, l’utilisateur a confirmé la réception en fournissant le code, et sa saisie a ouvert l’administration Unfold. Aucun code OTP n’est enregistré dans ces preuves.
- Accueil FR/EN : HTTP 200, en-têtes de langue corrects, dix sections dans leur ordre ; les neuf ressources image/script/feuille CSS vérifiées dans chaque langue répondent en HTTP 200. HTTP redirige vers HTTPS. Voir `http-checks.json`.
- HSTS d’un an, CSP stricte sur l’accueil, anti-iframe et anti-sniffing observés dans les réponses HTTPS.
- Galerie réelle : ouverture, passage de 1/4 à 4/4 par précédent, retour par suivant, fermeture Échap et restitution du focus au déclencheur. FAQ : ouverture et traduction FR/EN observées avec conservation de son état.

## Vérification locale

La suite existante et les six tests OTP ont donné **85 tests réussis**. Les trois tests de configuration PythonAnywhere ajoutés ensuite ont donné **3 tests réussis**, soit **88 tests exécutés et réussis** au total. Les nouveaux tests couvrent notamment refus de lecture/écriture admin sans OTP, usage unique, session distincte, expiration, limitation des essais et des renvois, CSRF, absence d’adresse et panne SMTP. Les tests de configuration vérifient le proxy PythonAnywhere et le refus du debug ou de la désactivation OTP dans `config.production`.

`manage.py check` : aucun problème. `makemigrations --check --dry-run` : aucune modification manquante. Sur le serveur, `manage.py check --deploy` ne signale que **security.W005 et security.W021**, conservés et documentés.

Mesure serveur avant ajout de ces preuves : **6 883 061 octets**, sous 500 000 000, selon `scripts/measure_delivery.py`. Occupation réelle observée avec `du` : projet **9,9 Mio**, virtualenv **88 Mio**, sous le quota gratuit de 512 Mio. Le contrôle de taille inclut SQLite et assets et exclut Git, environnements virtuels et caches.

## Preuves et limites

`home.png`, `admin-otp.png` et `admin-verified.png` montrent les écrans publiés. `http-checks.json` conserve les réponses et ressources contrôlées. Les captures évitent les secrets et le code OTP.

La date d’expiration affichée dans Web est le **11 novembre 2026** : utiliser « Run until 1 month from today » pour renouveler l’application gratuite. Aucun achat ni abonnement payant n’a été effectué.

Cette réception de déploiement ne constitue pas un nouvel audit complet de tous les critères responsive/accessibilité ou un test d’intrusion du serveur public. La limitation du premier facteur par le proxy, les sauvegardes et le suivi des dépendances restent à organiser. Les téléchargements, paiements et messages WhatsApp n’ont pas été déclenchés.

La procédure complète d’installation et de mise à jour figure à la fin du README. Sources d’hébergement : [déploiement Django](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/), [Force HTTPS](https://help.pythonanywhere.com/pages/ForcingHTTPS/), [compte gratuit](https://help.pythonanywhere.com/pages/FreeAccountsFeatures/).
