# Vitrine YemX

Django 5.2, SQLite et Django admin avec Unfold. La demande actuelle autorise l’implémentation backend après l’étape documentaire décrite dans `AGENTS.md`, qui est conservé.

Depuis ce dossier, avec Python 3.12 ou plus récent, sous PowerShell :

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:DJANGO_DEBUG = '1' # Développement HTTP local uniquement
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py seed_content
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver
```

Accueil : http://127.0.0.1:8000/ ; administration : http://127.0.0.1:8000/admin/.
Le venv et la base locale sont exclus de Git. Les migrations et données éditoriales sont livrées ; `seed_content` conserve les modifications existantes, sans option de remplacement. Aucun administrateur ou mot de passe n’est précréé.

La langue française est utilisée par défaut. `/?lang=en` et `/?lang=fr` enregistrent un cookie de préférence valable un an. Les textes, offres, avantages, FAQ, captures, assets et liens sont administrables, protégés contre la suppression et soumis aux permissions Django. Les clés structurelles sont en lecture seule après création. Les assets se sélectionnent parmi les fichiers fournis ; aucun upload n’est proposé. Pour inverser deux positions uniques, affecter d’abord une position temporaire libre.

Les templates reprennent les sections et les classes de la référence. Les images YemX, Lexend, les icônes SVG, CSS et JavaScript sont servis localement par les fichiers statiques Django. Le menu mobile, la galerie avec navigation et restitution du focus, les six FAQ indépendantes et le changement FR/EN sans perdre la section sont fonctionnels. Le choix de langue persiste dans le navigateur et dans un cookie ; les contenus administrables restent échappés.

Le navigateur intégré a servi aux comparaisons à 390, 768 et 1440 px et aux contrôles des interactions. Les corrections responsive et les limites observées sont documentées dans `evidence/FRONTEND_REPORT.md`. Les captures sont dans `evidence/visual/`.

Vérification :

```powershell
.\.venv\Scripts\pytest.exe -q
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe scripts\measure_delivery.py
```

Les tests créent leur propre base temporaire et ne modifient pas `db.sqlite3`. Voir `evidence/REPORT.md` pour les cycles TDD backend et `evidence/FRONTEND_REPORT.md` pour la validation du frontend.

Le mode debug exige désormais `DJANGO_DEBUG=1` explicitement. Pour conserver les sessions entre redémarrages locaux, définir une clé privée stable dans `DJANGO_SECRET_KEY` ; en développement seulement, une clé éphémère est générée si elle manque. Pytest sélectionne `config.test_settings` et utilise une base temporaire.

En production, `DJANGO_DEBUG=0` (valeur par défaut) exige `DJANGO_SECRET_KEY` privée, stable et aléatoire (au moins 50 caractères et cinq caractères distincts), et `DJANGO_ALLOWED_HOSTS` explicites séparés par des virgules, sans joker. Générer la clé avec `django.core.management.utils.get_random_secret_key` puis la stocker dans l’environnement privé du serveur ; ne pas la copier dans le dépôt. Une clé absente/faible ou des hôtes absents/avec joker empêchent le démarrage. Ces validations ne mesurent pas l’entropie réelle d’une clé choisie manuellement.

Ce mode impose la redirection HTTPS, HSTS d’un an sur le domaine, les cookies session/CSRF `Secure` et `SameSite=Lax`, une session `HttpOnly` valable huit heures, et le refus de l’intégration en iframe. La CSP stricte de l’accueil autorise uniquement les ressources locales et interdit les scripts inline ; elle ne s’applique pas à Unfold, qui utilise des scripts inline. Le cookie de langue reste accessible au JavaScript et ne donne aucun droit.

Avant tout déploiement, fournir TLS et un serveur WSGI/ASGI adapté, servir les fichiers statiques et limiter les essais de connexion à l’admin au niveau du reverse proxy. Les en-têtes de proxy ne sont pas considérés fiables par défaut : `config.production` est réservé au proxy géré par PythonAnywhere et reconnaît son en-tête HTTPS. HSTS ne couvre pas les sous-domaines et n’est pas préchargé ; les avertissements `security.W005` et `security.W021` sont des choix documentés à réévaluer selon l’hébergement.

Contrôles de sécurité reproductibles : `pytest tests/test_security.py -q`, puis `manage.py check --deploy` dans l’environnement de production. Voir [evidence/SECURITY_REPORT.md](evidence/SECURITY_REPORT.md) pour les attaques testées, les correctifs et les limites.

Références : https://yemxapp.com/ (HTML, traductions et captures conservés dans les données et preuves), https://unfoldadmin.com/docs/installation/quickstart/ et https://docs.djangoproject.com/en/5.2/. Lexend est livré avec sa licence OFL dans le dossier des polices. Les assets YemX conservent leur identité et leurs URL de provenance.

Collecte des fichiers statiques pour un serveur configuré à cet effet :

```powershell
.\.venv\Scripts\python.exe manage.py collectstatic --noinput
```

`runserver` sert directement les assets en développement. La collecte donne priorité aux fichiers Unfold pour les trois scripts admin de même nom que Django.

## Connexion administrateur avec OTP email

En production, le mot de passe doit être suivi d’un code à six chiffres envoyé à l’adresse email du compte Django. Le code expire après cinq minutes, est lié à la session qui l’a demandé et n’est utilisable qu’une fois. Cinq codes incorrects bloquent les vérifications et les renvois pendant dix minutes, y compris dans une nouvelle session. Un renvoi est possible après une minute. La base conserve uniquement des empreintes HMAC du code et de la session. Une panne SMTP ne donne jamais accès à l’administration. Déconnexion, changement du mot de passe ou nouvelle session imposent une nouvelle vérification.

`DJANGO_ADMIN_OTP_REQUIRED=1` active également cette protection en développement, avec un SMTP configuré. `config.production` refuse le debug et la désactivation de l’OTP. Chaque administrateur doit posséder une adresse email valide ; l’adresse de l’expéditeur Gmail est distincte de celle du destinataire. Les secrets SMTP et la clé Django restent dans `.env`, exclu de Git et chargé sans écraser les variables du processus. Le mot de passe d’application Gmail doit être saisi sans les espaces de présentation.

## Publication sur PythonAnywhere gratuit

Procédure pour le compte **typinclub**, le site `https://typinclub.pythonanywhere.com` et le dépôt public [fokouarnaud/typinclub](https://github.com/fokouarnaud/typinclub). Se connecter à [PythonAnywhere](https://www.pythonanywhere.com/user/typinclub/) avec ce compte. Le dossier est `/home/typinclub/typinclub` ; ne pas utiliser les chemins du compte `ventisax`.

### 1. Console Bash, clone et environnement virtuel

Ouvrir **Consoles → Bash**, puis :

```bash
cd /home/typinclub
git clone --branch main https://github.com/fokouarnaud/typinclub.git
cd /home/typinclub/typinclub
python3.13 -m venv /home/typinclub/.virtualenvs/yemx
source /home/typinclub/.virtualenvs/yemx/bin/activate
python -m pip install --no-cache-dir -r requirements.txt
```

Choisir la même version de Python dans la console et dans l’application Web. Les exemples utilisent Python 3.13.

### 2. Configuration privée `.env`

```bash
cp .env.example .env
chmod 600 .env
```

Éditer `.env` depuis **Files**, sans copier les secrets dans le dépôt, dans une commande historisée ou dans les preuves. Renseigner :

```dotenv
DJANGO_SETTINGS_MODULE=config.production
DJANGO_DEBUG=0
DJANGO_SECRET_KEY=<clé privée aléatoire générée sur le serveur>
DJANGO_ALLOWED_HOSTS=typinclub.pythonanywhere.com
DJANGO_ADMIN_OTP_REQUIRED=1
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=<adresse Gmail expéditrice>
EMAIL_HOST_PASSWORD=<mot de passe d’application Gmail sans espaces>
DEFAULT_FROM_EMAIL=<adresse Gmail expéditrice>
```

Pour générer et enregistrer la clé directement dans le fichier, sans l’afficher :

```bash
python - <<'PY'
from pathlib import Path
from django.core.management.utils import get_random_secret_key
path = Path('.env')
content = path.read_text()
if 'DJANGO_SECRET_KEY=\n' not in content:
    raise SystemExit('Clé déjà renseignée : conserver la clé existante.')
path.write_text(content.replace('DJANGO_SECRET_KEY=\n', 'DJANGO_SECRET_KEY=' + get_random_secret_key() + '\n'))
path.chmod(0o600)
PY
export DJANGO_SETTINGS_MODULE=config.production
```

Ne pas changer cette clé lors des mises à jour. Le chargement de `.env` est automatique dans les settings. L’export sélectionne ces settings pour les commandes de gestion ; le fichier WSGI les sélectionne indépendamment pour le serveur.

### 3. SQLite, contenus initiaux et administrateur

```bash
python manage.py migrate
python manage.py seed_content
python manage.py createsuperuser --username fokou --email <email destinataire des OTP>
python manage.py collectstatic --noinput
python manage.py check --deploy
```

Saisir le mot de passe administrateur dans l’invite masquée. Aucun mot de passe n’est fourni dans Git. `seed_content` initialise notamment quatre captures, six FAQ, deux offres et les textes FR/EN ; une deuxième exécution conserve les éditions existantes. `db.sqlite3` reste sur le serveur et est exclu de Git. Les avertissements HSTS `security.W005` et `security.W021` restent documentés. Ne pas utiliser `runserver` pour la publication.

### 4. Application Web et WSGI

Dans **Web → Add a new web app**, choisir le sous-domaine gratuit, **Manual configuration**, puis **Python 3.13**. Indiquer :

| Réglage | Valeur |
| --- | --- |
| Source code | `/home/typinclub/typinclub` |
| Working directory | `/home/typinclub/typinclub` |
| Virtualenv | `/home/typinclub/.virtualenvs/yemx` |
| Static URL | `/static/` |
| Static directory | `/home/typinclub/typinclub/staticfiles` |

Dans le fichier WSGI accessible depuis **Web**, enregistrer :

```python
import os
import sys

project = '/home/typinclub/typinclub'
if project not in sys.path:
    sys.path.insert(0, project)
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.production'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Activer **Force HTTPS** dans **Web**, puis cliquer **Reload**. Le domaine gratuit dispose de HTTPS géré par l’hébergeur. La configuration de confiance du proxy est spécifique à PythonAnywhere ; ne pas réutiliser `config.production` sur un proxy non vérifié.

### 5. Réception et mises à jour

Consulter l’accueil en FR/EN, les images et `/admin/`. Se connecter avec le compte créé, vérifier l’arrivée réelle de l’OTP dans la boîte destinataire et saisir le code. Vérifier que l’administration reste inaccessible avant le code. Examiner **Web → Error log** si un problème apparaît. Gmail peut refuser la connexion SMTP ; garder l’OTP actif et corriger les identifiants ou l’accès SMTP. L’arrivée du message dans la boîte doit être confirmée par son destinataire.

Pour mettre à jour : sauvegarder SQLite et `.env` dans un emplacement privé hors dépôt, puis :

```bash
cd /home/typinclub/typinclub
source /home/typinclub/.virtualenvs/yemx/bin/activate
export DJANGO_SETTINGS_MODULE=config.production
git pull --ff-only origin main
python -m pip install --no-cache-dir -r requirements.txt
python manage.py migrate
python manage.py seed_content
python manage.py collectstatic --noinput
python manage.py check --deploy
```

Cliquer ensuite **Reload**. Le compte gratuit impose un quota de stockage, un budget CPU et une expiration mensuelle de l’application Web : renouveler depuis **Web** avant la date indiquée. La limitation des essais du premier facteur, le suivi des dépendances et les sauvegardes restent à organiser avant une utilisation durable.

Sources de la procédure : [déploiement Django](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/), [HTTPS](https://help.pythonanywhere.com/pages/ForcingHTTPS/), [limites du compte gratuit](https://help.pythonanywhere.com/pages/FreeAccountsFeatures/).
