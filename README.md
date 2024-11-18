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
kubectl exec -it deployments/shw shw-runserver -- uv run --with git+https://github.com/alexpdp7/selfhostwatch.git@k8s[pg] django-admin createsuperuser --settings shw.dj.settings
```
