Django `manage.py`:

```
uv run python -m shw.dj.manage ...
```

## Create a new app

```
mkdir -p shw/dj/foo
uv run python -m shw.dj.manage startapp foo shw/dj/foo
$EDITOR shw/dj/settings.py  # add to INSTALLED_APPS
$EDITOR shw/dj/foo/apps.py  # change FooConfig.name to shw.dj.foo
```
