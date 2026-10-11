# Revue de sécurité — 11 octobre 2026

Périmètre : code Django/SQLite de la vitrine, templates, JavaScript, modèles, formulaires et administration Unfold. La demande actuelle autorise les tests et correctifs, au-delà de l’étape documentaire historique. Aucun déploiement ni test d’intrusion contre yemxapp.com ou ses services externes. Les attaques automatisées utilisent la base temporaire de pytest-django ; aucun compte administratif réel n’a été créé ou modifié.

## Constats et correctifs

| Constat | Impact et traitement |
| --- | --- |
| Debug activé par défaut | Risque d’exposition de détails internes si le projet est publié sans configuration. Debug désactivé par défaut ; développement HTTP avec `DJANGO_DEBUG=1` explicite. |
| Production sans HTTPS obligatoire et cookies `Secure` | Un transport HTTP pourrait exposer identifiants et session. Redirection HTTPS, cookies session/CSRF `Secure`, session `HttpOnly`, `SameSite=Lax`, durée de huit heures et HSTS d’un an sur le domaine. Tests sur requêtes Django simulant HTTPS ; aucun certificat réel éprouvé. |
| Clé aléatoire au démarrage, même sans debug | Instabilité des sessions entre processus, pas une preuve de vol de session. Production refusée sans clé privée stable d’au moins 50 caractères et cinq caractères distincts ; refus des clés préfixées `django-insecure-`. Ces seuils ne prouvent pas l’entropie d’une clé humaine. |
| Hôtes de production non exigés explicitement, joker possible | Risque de mauvaise configuration de la validation Host. Hôtes explicites obligatoires, joker refusé ; Host étranger testé à 400. En-têtes de proxy non fiables par défaut. |
| CSP absente de la vitrine | Absence de défense supplémentaire, sans XSS exploitable observée. Ajout d’une CSP : ressources locales, scripts inline/eval, objets, base et intégration en iframe interdits. Aucun assouplissement `unsafe-inline`/`unsafe-eval`. |
| Formulaire URL normalisant `//evil.example/` en HTTPS | Écart à l’exigence de destination absolue explicite ; pas une exécution JavaScript constatée. Validation avant normalisation, imposant `https://`, sur les liens et la provenance des assets. |
| Redirection sûre après connexion vers `/accounts/profile/` inexistant | Défaut de parcours, pas une redirection ouverte. `LOGIN_REDIRECT_URL=/admin/` ; cible externe refusée lors de la connexion. |

Pas de SQL brut ou de construction SQL à partir de requêtes dans le code applicatif inspecté : ORM Django utilisé. Textes rendus avec échappement Django, traductions transférées via `json_script`, mises à jour DOM via `textContent`/attributs textuels ; pas de `innerHTML`, `eval`, `mark_safe` ou `csrf_exempt` observés dans l’application. La validation HTTPS, les chemins limités aux assets fournis, les permissions et la protection CSRF étaient déjà présentes ; elles ont été éprouvées, sans les réimplémenter.

## Tests d’intrusion reproductibles

`tests/test_security.py` exerce les réponses HTTP, les formulaires, la base et les sessions effectives du client Django. Les tests de configuration démarrent un processus séparé avec des variables contrôlées. Les secrets de test sont synthétiques ; aucune clé de production n’est enregistrée.

| Attaque | Entrée et résultat attendu |
| --- | --- |
| Injection SQL | `' OR 1=1 --` et `'; DROP TABLE showcase_localizedtext; --` via `lang`, cookie et recherche admin : réponse valide, aucune ligne trouvée par contournement, nombre de textes inchangé. Connexion avec nom injecté : aucune authentification. |
| XSS stockée | Fermeture `</script>`, script, image avec `onerror`, rupture de guillemets et `onmouseover` dans tous les textes FR/EN : aucune balise/attribut actif injecté, texte conservé, JSON valide et attribut description intact. Même contrôle dans liste et formulaire Unfold. |
| XSS réfléchie | `<svg onload=alert(1)>` dans langue et recherche : langue française de secours et aucun résultat injecté. |
| URL active ou relative | `javascript:`, `data:`, `//host`, identifiants dans URL et rupture d’attribut : formulaire admin invalide, destination enregistrée inchangée. |
| Traversée de chemin | `../../config/settings.py`, chemin Windows et sortie des assets : `ValidationError` à l’enregistrement. |
| CSRF | POST admin sans jeton, POST avec jeton valide mais origine étrangère et connexion sans jeton : 403, contenu inchangé. |
| Session | Identifiant connu avant connexion : rotation et refus du rejeu ; ancien identifiant après déconnexion : refus ; session expirée et identifiant forgé : accès admin refusé. |
| Transport et Host | HTTP redirigé vers HTTPS même avec `X-Forwarded-Proto` forgé ; connexion HTTPS avec jeton/origine valides, cookies sécurisés, HSTS ; Host étranger rejeté. |
| Configuration dangereuse | Clé absente/faible, hôtes absents/avec joker, debug invalide et environnement sans sélection explicite du debug : démarrage refusé avec `ImproperlyConfigured`. |

Cycle initial : **10 échecs / 16 réussites** dans `security-red.txt`. Les échecs comprennent le durcissement manquant, la normalisation URL et le défaut de destination de retour. Lors de la mise au point du harnais, la connexion HTTPS a reçu son en-tête Origin légitime et la recherche Unfold a été filtrée sur la ligne attaquée, initialement hors de la première page paginée. Les assertions de refus et d’inertie n’ont pas été supprimées ou assouplies.

Résultat final observé : **79 tests réussis en 59,30 s**, dont **29 cas de sécurité**, zéro échec. Preuves : `security-full-tests.txt`, `security-results.xml` et `security-green.txt` (extrait des résultats JUnit). `manage.py check` : aucun problème ; `makemigrations --check --dry-run` : aucune modification détectée (`security-local-check.txt`). Livrable environ **6,85 Mo**, inférieur à 500 000 000 octets, selon les exclusions prévues (`security-delivery-size.txt`).

Rejouer depuis la racine :

```powershell
.\.venv\Scripts\pytest.exe tests/test_security.py -q
.\.venv\Scripts\pytest.exe -q
$env:DJANGO_DEBUG = '1'
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe scripts\measure_delivery.py
```

Pour `manage.py check --deploy`, utiliser `DJANGO_DEBUG=0`, une clé privée forte et `DJANGO_ALLOWED_HOSTS` explicites. La commande exécutée avec une clé éphémère privée de vérification n’a signalé que `security.W005` et `security.W021` : inclusion des sous-domaines et préchargement HSTS désactivés intentionnellement tant que l’hébergement n’est pas défini. Aucun avertissement n’est masqué. Résultat dans `security-deploy-check.txt`.

## Vérification navigateur et limites

Accueil servi en HTTP local sur `127.0.0.1:8001`, avec la même CSP qu’en production. Changement FR → EN, ouverture/fermeture du menu mobile, galerie Dashboard → Inventory management (1/4 → 2/4), fermeture par Échap et ouverture de la première FAQ avec `aria-expanded=true` observés dans le navigateur intégré. Aucun message error/warn capturé dans la console sur ce parcours. Les assets restent locaux ; aucune destination de téléchargement/contact n’a été activée.

Une requête HTTP réelle avec la charge SQL dans `lang` a également reçu 200, langue `fr`, CSP, `X-Frame-Options: DENY` et `X-Content-Type-Options: nosniff` (`security-http-smoke.json`).

Les charges XSS sont contrôlées par parsing des réponses et validation du JSON ; elles n’ont pas été exécutées comme scénario d’attaque dans un navigateur. Le contrôle navigateur porte sur la compatibilité des interactions avec la CSP. Ce n’est pas un audit exhaustif ou une certification de sécurité.

Avant exposition publique : vérifier TLS réel, serveur WSGI/ASGI et fichiers statiques, reverse proxy et validation de ses en-têtes, restriction ou limitation des essais de connexion à l’admin, sauvegardes et permissions SQLite, rotation des secrets et suivi des avis de sécurité des dépendances. Aucun mécanisme anti-bruteforce applicatif/MFA n’est ajouté. Unfold conserve ses scripts inline et ne reçoit pas la CSP stricte de l’accueil. Aucun scan complet des dépendances, test de charge/DoS ou test d’infrastructure n’a été effectué.

Références consultées : [sécurité Django 5.2](https://docs.djangoproject.com/en/5.2/topics/security/) et [checklist de déploiement](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/). Ces recommandations motivent la séparation HTTP local/HTTPS production et la vérification des protections natives ; elles ne constituent pas une preuve propre à ce projet.
