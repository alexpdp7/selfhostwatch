from shw import git
from shw.dj.git import models


def load():
    broken = {}
    for git_app in models.GitApp.objects.all():
        try:
            load_app(git_app)
        except Exception as e:
            broken[git_app.name] = e
    assert not broken, f"Broken repos {broken}"


def load_app(git_app):
    tags_to_commits = git.get_remote_tags_to_dates(git_app.remote_url)

    for tag, date in tags_to_commits.items():
        models.Version.objects.update_or_create(
            git_app=git_app,
            version=tag,
            defaults={"date": date}
        )
