import contextlib
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
    with clone_repo(remote_url, filter_blobs=True) as clone:
        for commit in commits:
            result[commit] = get_last_commit_date(clone, commit)
    return result


def get_remote_tags_to_dates(remote_url):
    result = {}
    tags_to_commits = get_tags_to_commits(remote_url)
    commits_to_dates = get_commits_to_dates(remote_url, tags_to_commits.values())
    for tags, commit in tags_to_commits.items():
        result[tags] = commits_to_dates[commit]
    return result


@contextlib.contextmanager
def clone_repo(remote_url, filter_blobs=True):
    with tempfile.TemporaryDirectory() as tempdir:
        tempdir = pathlib.Path(tempdir)
        filter_blobs = ["--filter=blob:none"] if filter_blobs else []
        subprocess.run(["git", "clone", "--filter=blob:none", remote_url, tempdir], check=True, env={"GIT_TERMINAL_PROMPT": "0"})
        yield tempdir


def get_last_commit_date(clone, commit=None):
    commit = [commit] if commit else []
    log = subprocess.run(["git", "log", "-1", "--format=format:%ci"] + commit, check=True, cwd=clone, stdout=subprocess.PIPE, encoding="utf8")
    return datetime.datetime.fromisoformat(log.stdout)
