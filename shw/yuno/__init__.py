from collections import abc
import dataclasses
import logging
import subprocess
import tomllib

import httpx

from shw import git


logger = logging.getLogger(__name__)


def load():
    return httpx.get("https://apps.yunohost.org/default/v3/apps.json").json()


@dataclasses.dataclass
class App:
    id: str
    architectures: set[str]
    version: str
    yuno_ldap: str # true, false, not_relevant
    yuno_multi_instance: bool
    yuno_sso: str  # true, false, not_relevant
    yuno_high_quality: bool
    yuno_maintained: bool
    yuno_state: str
    repo: str


def app_from_json(j):
    architectures = j["manifest"]["integration"]["architectures"]

    if architectures == "all":
        architectures = set()
    else:
        architectures = set(architectures)

    return App(
        id=j["id"],
        architectures=architectures,
        version=j["manifest"]["version"],
        yuno_ldap=str(j["manifest"]["integration"]["ldap"]).lower(),
        yuno_multi_instance=j["manifest"]["integration"]["multi_instance"],
        yuno_sso=str(j["manifest"]["integration"]["sso"]).lower(),
        yuno_high_quality=j["high_quality"],
        yuno_maintained=j["maintained"],
        yuno_state=j["state"],
        repo=j["manifest"]["upstream"].get("code"),
    )


def app_from_manifest(s):
    manifest = tomllib.loads(s)
    return App(
        id=manifest["id"],
        architectures=manifest["integration"]["architectures"],
        version=manifest["version"],
        yuno_ldap=str(manifest["integration"]["ldap"]).lower(),
        yuno_multi_instance=manifest["integration"]["multi_instance"],
        yuno_sso=str(manifest["integration"]["sso"]).lower(),
        yuno_high_quality=None,
        yuno_maintained=None,
        yuno_state=None,
        repo=manifest["upstream"].get("code"),
    )


def parse(apps_json) -> abc.Iterator[App]:
    return [app_from_json(j) for j in apps_json["apps"].values()]


def backfill(app):
    versions = []
    last_app = None
    with git.clone_repo(f"https://github.com/YunoHost-Apps/{app}_ynh.git") as repo:
        while True:
            manifest_text = (repo / "manifest.toml").read_text()
            try:
                app = app_from_manifest(manifest_text)
                date = git.get_last_commit_date(repo)
                if not last_app or last_app != app:
                    yield app, date
                    last_app = app
            except tomllib.TOMLDecodeError as e:
                logger.error("malformed manifest")

            log = subprocess.run(["git", "log", "--format=%H", "HEAD^", "manifest.toml"], check=True, encoding="utf8", stdout=subprocess.PIPE, cwd=repo)
            previous_commit = log.stdout.strip()
            if not previous_commit:
                return
            previous_commit = previous_commit.splitlines()[0]
            subprocess.run(["git", "checkout", previous_commit], check=True, cwd=repo)
