# selfhostwatch

I believe people should self-host more (and people self-hosted more in the past).
I have found many projects, such as [YunoHost](https://yunohost.org/), that I consider great for introducing people to self-hosting.

However, I think finding a hosting project to trust with dilligent updates and long-term future is a huge obstacle.

selfhostwatch scrapes self-hosting systems (currently, only YunoHost) and displays a timeline of upstream and downstream updates.

You can view the current timelines at <https://alexpdp7.github.io/selfhostwatch/>.

## Hacking

Django `manage.py`:

```
DEV=y uv run python -m shw.dj.manage ...
```

### Create a new app

```
mkdir -p shw/dj/foo
uv run python -m shw.dj.manage startapp foo shw/dj/foo
$EDITOR shw/dj/settings.py  # add to INSTALLED_APPS
$EDITOR shw/dj/foo/apps.py  # change FooConfig.name to shw.dj.foo
```

### Loading data from the public website

```
curl https://alexpdp7.github.io/selfhostwatch/dump.json | DEV=y uv run python -m shw.dj.manage loaddata --format json -
```

## Kubernetes

```
kubectl create ns shw
kubectl config set-context --current --namespace shw
kubectl create configmap shw --from-literal=ALLOWED_HOSTS=localhost --from-literal=DJANGO_SETTINGS_MODULE=shw.dj.settings
# see https://github.com/jazzband/dj-database-url
kubectl create secret generic shw --from-file=SECRET_KEY=<(openssl rand 128 | base64 -w 0) --from-literal=DATABASE_URL=... --from-literal=EXPORT_GIT_URL=...
kubectl apply -f k8s.yaml
kubectl exec -it deployments/shw shw-runserver -- uv run --with git+https://github.com/alexpdp7/selfhostwatch.git[pg] django-admin createsuperuser
```

## How it works

I run the k8s deployment in my own cluster.
This deployment is *not* accessible outside the cluster yet.
I can use `kubectl port-forward` to access the Django website.

The public web site has URLs that translate well to file names.
Instead of using URLs that end in `/`, URLs end in `x.html`.
The `publish` cronjob uses `wget --mirror` to extract a static web site, and publishes by pushing to GitHub Pages.

In this way, I can run the scraping processes in Kubernetes, with a database, etc. and just publish a static website.
(But still, I can use Django `runserver` for interactive development.)
