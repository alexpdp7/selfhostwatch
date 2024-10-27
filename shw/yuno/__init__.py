import dataclasses

import httpx


def load():
    return httpx.get("https://apps.yunohost.org/default/v3/apps.json").json()


def parse(apps_json):
    return [app_from_json(j) for j in apps_json["apps"].values()]


@dataclasses.dataclass
class App:
    id: str
    architectures: list[str]
    version: str
    yuno_ldap: bool
    yuno_multi_instance: bool
    yuno_sso: bool
    yuno_high_quality: bool
    yuno_maintained: bool
    yuno_state: str


def app_from_json(j):
    return App(
        id=j["id"],
        architectures=j["manifest"]["integration"]["architectures"],
        version=j["manifest"]["version"],
        yuno_ldap=j["manifest"]["integration"]["ldap"],
        yuno_multi_instance=j["manifest"]["integration"]["multi_instance"],
        yuno_sso=j["manifest"]["integration"]["sso"],
        yuno_high_quality=j["high_quality"],
        yuno_maintained=j["maintained"],
        yuno_state=j["state"],
    )
