import logging

from django.utils import timezone

from shw import yuno
from shw.dj.git import models as git_models
from shw.dj.yuno import models


logger = logging.getLogger(__name__)


def load(backfill_from_repos=False):
    apps = yuno.parse(yuno.load())
    broken = {}
    for app in apps:
        logger.info("Updating %s", app)
        if backfill_from_repos:
            try:
                backfill(app.id)
            except Exception as e:
                broken[app.id] = e
            continue

        previous = models.AppVersion.objects.filter(name=app.id).order_by("-updated")

        if previous.exists():
            previous = previous.first()

            previous_app = yuno.App(
                id=previous.name,
                architectures=set(
                    a
                    for a in previous.architectures.all().values_list("name", flat=True)
                ),
                version=previous.version,
                yuno_ldap=previous.yuno_ldap,
                yuno_multi_instance=previous.yuno_multi_instance,
                yuno_sso=previous.yuno_sso,
                yuno_high_quality=previous.yuno_high_quality,
                yuno_maintained=previous.yuno_maintained,
                yuno_state=previous.yuno_state,
                repo=previous.repo,
            )

            logger.debug("comparing app {app} to previous {previous_app}")

            if app == previous_app:
                logger.info("skipping {app} because it is identical to {previous_app}")
                continue

        app_version = models.AppVersion(
            name=app.id,
            version=app.version,
            yuno_ldap=app.yuno_ldap,
            yuno_multi_instance=app.yuno_multi_instance,
            yuno_sso=app.yuno_sso,
            yuno_high_quality=app.yuno_high_quality,
            yuno_maintained=app.yuno_maintained,
            yuno_state=app.yuno_state,
            repo=app.repo,
            updated=timezone.now(),
        )

        app_version.save()

        for architecture in app.architectures:
            architecture_instance, _created = models.Architecture.objects.get_or_create(
                name=architecture
            )
            app_version.architectures.add(architecture_instance)
    assert not broken, f"Broken apps {broken}"


def backfill(app):
    models.AppVersion.objects.filter(name=app).delete()
    for app, date in yuno.backfill(app):
        app_version = models.AppVersion(
            name=app.id,
            version=app.version,
            yuno_ldap=app.yuno_ldap,
            yuno_multi_instance=app.yuno_multi_instance,
            yuno_sso=app.yuno_sso,
            yuno_high_quality=app.yuno_high_quality,
            yuno_maintained=app.yuno_maintained,
            yuno_state=app.yuno_state or "unknown",
            repo=app.repo,
            updated=date,
        )

        app_version.save()


def create_git_apps():
    app_names_with_repo = set(
        models.AppVersion.objects.filter(repo__isnull=False).values_list("name")
    )

    for app in app_names_with_repo:
        app = app[0]
        latest_app = models.AppVersion.objects.filter(
            name=app, repo__isnull=False
        ).order_by("-updated")
        if len(latest_app) == 0:
            continue
        repo = latest_app[0].repo
        if len(git_models.GitApp.objects.filter(name=app, manual=True)) > 0:
            continue
        git_models.GitApp.objects.update_or_create(
            name=app, defaults={"remote_url": repo}
        )
