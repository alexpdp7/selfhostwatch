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
    yuno_ldap: str  # true, false, not_relevant
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

    _check_manifest(j["manifest"])

    return App(
        id=j["id"],
        architectures=architectures,
        version=j["manifest"]["version"],
        yuno_ldap=str(j["manifest"]["integration"]["ldap"]).lower(),
        yuno_multi_instance=str(j["manifest"]["integration"]["multi_instance"]),
        yuno_sso=str(j["manifest"]["integration"]["sso"]).lower(),
        yuno_high_quality=j["high_quality"],
        yuno_maintained=j["maintained"],
        yuno_state=j["state"],
        repo=j["manifest"]["upstream"].get("code"),
    )


def app_from_manifest(s):
    manifest = tomllib.loads(s)

    _check_manifest(manifest)

    return App(
        id=manifest["id"],
        architectures=manifest["integration"]["architectures"],
        version=manifest["version"],
        yuno_ldap=str(manifest["integration"]["ldap"]).lower(),
        yuno_multi_instance=str(manifest["integration"]["multi_instance"]),
        yuno_sso=str(manifest["integration"]["sso"]).lower(),
        yuno_high_quality=None,
        yuno_maintained=None,
        yuno_state=None,
        repo=manifest["upstream"].get("code"),
    )


def _check_manifest(m):
    required_keys = set(["id", "integration", "version", "upstream"])
    missing_keys = required_keys - m.keys()
    if missing_keys:
        raise InvalidManifest(f"missing keys {missing_keys} in {m}")

    required_keys = set(["ldap", "multi_instance", "sso"])
    missing_keys = required_keys - m["integration"].keys()
    if missing_keys:
        raise InvalidManifest(f"missing integration keys {missing_keys} in {m}")

    if "https://github.com/search?" in m["upstream"].get("code", ""):
        raise InvalidManifest(f"{m} has a bad upstream.code")


class InvalidManifest(Exception):
    pass


def parse(apps_json) -> abc.Iterator[App]:
    return [app_from_json(j) for j in apps_json["apps"].values()]


def backfill(app):
    last_app = None
    with git.clone_repo(f"https://github.com/YunoHost-Apps/{app}_ynh.git") as repo:
        while True:
            try:
                manifest_text = (repo / "manifest.toml").read_text()
                app = app_from_manifest(manifest_text)
                date = git.get_last_commit_date(repo)
                if not last_app or last_app != app:
                    yield app, date
                    last_app = app
            except FileNotFoundError:
                # this just happens for scovie and my_webdav; we seem to be only discarding v1 history or very early history
                logger.error("manifest not found")
                return
            except (tomllib.TOMLDecodeError, InvalidManifest) as e:
                logger.error("malformed manifest %s", e)

            logs = subprocess.run(
                ["git", "log", "--format=%H", "manifest.toml"],
                check=True,
                encoding="utf8",
                stdout=subprocess.PIPE,
                cwd=repo,
            )
            if len(logs.stdout.strip().splitlines()) == 1:
                return

            log = subprocess.run(
                ["git", "log", "--format=%H", "HEAD^", "manifest.toml"],
                check=True,
                encoding="utf8",
                stdout=subprocess.PIPE,
                cwd=repo,
            )
            previous_commit = log.stdout.strip()
            if not previous_commit:
                return
            previous_commit = previous_commit.splitlines()[0]
            subprocess.run(["git", "checkout", previous_commit], check=True, cwd=repo)
