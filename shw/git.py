import datetime
import pathlib
import subprocess
import tempfile


def get_tags_to_commits(remote_url):
    result = {}
    git = subprocess.run(["git", "ls-remote", "--tags", "--refs", remote_url], check=True, stdout=subprocess.PIPE, encoding="utf8")
    lines = git.stdout.splitlines()
    for l in lines:
        commit, tag = l.split()
        assert tag.startswith("refs/tags/"), f"{tag} does not start with refs/tags/"
        tag = tag[len("refs/tags/"):]
        result[tag] = commit
    return result


def get_commits_to_dates(remote_url, commits):
    result = {}
    with tempfile.TemporaryDirectory() as tempdir:
        tempdir = pathlib.Path(tempdir)
        subprocess.run(["git", "clone", "--filter=blob:none", remote_url, "."], check=True, cwd=tempdir)
        for commit in commits:
            log = subprocess.run(["git", "log", "-1", "--format=format:%ci", commit], check=True, cwd=tempdir, stdout=subprocess.PIPE, encoding="utf8")
            result[commit] = datetime.datetime.fromisoformat(log.stdout)
    return result


def get_remote_tags_to_dates(remote_url):
    result = {}
    tags_to_commits = get_tags_to_commits(remote_url)
    commits_to_dates = get_commits_to_dates(remote_url, tags_to_commits.values())
    for tags, commit in tags_to_commits.items():
        result[tags] = commits_to_dates[commit]
    return result
