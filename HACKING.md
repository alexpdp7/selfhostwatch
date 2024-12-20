# Hacking

selfhostwatch collects data from services such as YunoHost and presents them as a website.

Currently, selfhostwatch is a Django application.
The data collection processes store data in a relational database by using the Djang ORM.
The website that presents the data is implemented by using Django views and templates.

Django helps implement a basic administrator interface that administrators can use to manipulate selfhostwatch data.

## Running selfhostwatch in development mode

To manage its dependencies, selfhostwatch uses [uv](https://github.com/astral-sh/uv).

The selfhostwatch Django settings detects the `DEV` environment variable to enable development mode.
When the `DEV` environment variable is present, selfhostwatch uses an SQLite database and tweaks some Django settings for an easier development experience.

To run Django `manage.py` commands, set the `DEV` environment variable and use uv to run the `shw.dj.manage` modules:

```
DEV=y uv run python -m shw.dj.manage ...
```

### Loading data from the public website

The public website runs the `manage.py` `dumpdata` command daily and publishes the result.
You can seed your development database from the public website data with the following command:

```
curl https://alexpdp7.github.io/selfhostwatch/dump.json | DEV=y uv run python -m shw.dj.manage loaddata --format json -
```

## Creating a new app

selfhostwatch has a non-standard Django project structure:

* Non-Django-specific code is in `shw.foo` modules, such as `shw.yuno` for YunoHost data extraction code.
* Django-specific code is in `shw.dj.foo` modules, such as `shw.dj.yuno` for code that uses the Django ORM to persist YunoHost data.

The `manage.py` `startapp` command requires a few tweaks to create apps properly in this structure:

```
mkdir -p shw/dj/foo
uv run python -m shw.dj.manage startapp foo shw/dj/foo
$EDITOR shw/dj/settings.py  # add to INSTALLED_APPS
$EDITOR shw/dj/foo/apps.py  # change FooConfig.name to shw.dj.foo
```

## The production deployment

Currently, selfhostwatch is exposed to the Internet as a static website on GitHub Pages.
This delegates the maintenance burden of keeping the website available to GitHub.

The data collection and static website publishing services run in a private Kubernetes cluster.

The public web site has URLs that translate well to file names.
Instead of using URLs that end in `/`, URLs end in `x.html`.
The `publish` Kubernetes cronjob uses `wget --mirror` to extract a static web site, and publishes by pushing to GitHub Pages.

### The Kubernetes deployment

The following commands describe roughly how selfhostwatch is deployed to the private Kubernetes cluster.

```
kubectl create ns shw
kubectl config set-context --current --namespace shw
kubectl create configmap shw --from-literal=ALLOWED_HOSTS=localhost --from-literal=DJANGO_SETTINGS_MODULE=shw.dj.settings
# see https://github.com/jazzband/dj-database-url
kubectl create secret generic shw --from-file=SECRET_KEY=<(openssl rand 128 | base64 -w 0) --from-literal=DATABASE_URL=... --from-literal=EXPORT_GIT_URL=...
kubectl apply -f k8s.yaml
kubectl exec -it deployments/shw shw-runserver -- uv run --with git+https://github.com/alexpdp7/selfhostwatch.git[pg] django-admin createsuperuser
```
