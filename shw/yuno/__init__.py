from collections import abc
import dataclasses

import httpx


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
    )


def parse(apps_json) -> abc.Iterator[App]:
    return [app_from_json(j) for j in apps_json["apps"].values()]
