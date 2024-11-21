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

## Create a new app

```
mkdir -p shw/dj/foo
uv run python -m shw.dj.manage startapp foo shw/dj/foo
$EDITOR shw/dj/settings.py  # add to INSTALLED_APPS
$EDITOR shw/dj/foo/apps.py  # change FooConfig.name to shw.dj.foo
```

## Kubernetes

```
kubectl create ns shw
kubectl config set-context --current --namespace shw
kubectl create configmap shw --from-literal=allowed_hosts=localhost
# see https://github.com/jazzband/dj-database-url
kubectl create secret generic shw --from-file=secret_key=<(openssl rand 128 | base64 -w 0) --from-literal=database_url=...
kubectl apply -f k8s.yaml
kubectl exec -it deployments/shw shw-runserver -- uv run --with git+https://github.com/alexpdp7/selfhostwatch.git[pg] django-admin createsuperuser --settings shw.dj.settings
```
