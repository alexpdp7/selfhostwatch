import os
import pathlib
import subprocess
import tempfile

from django.core.management.commands import dumpdata


def export():
    http_host_port = os.environ["EXPORT_HTTP_HOST_PORT"]
    with tempfile.TemporaryDirectory() as tempdir:
        tempdir = pathlib.Path(tempdir)
        mirrordir = tempdir / http_host_port / "updates"
        mirrordir.mkdir(parents=True, exist_ok=True)

        subprocess.run(
            [
                "wget",
                "--mirror",
                "--convert-links",
                f"http://{http_host_port}/updates/index.html",
            ],
            check=True,
            cwd=tempdir,
        )

        dumpdata.Command().handle("git", "yuno",
                                  format="json",
                                  output=mirrordir / "dump.json",
                                  verbosity=0, exclude=[],
                                  indent=None, database=None, traceback=None, use_natural_foreign_keys=None, use_natural_primary_keys=None, use_base_manager=None, primary_keys=None)

        subprocess.run(["git", "init"], check=True, cwd=mirrordir)
        subprocess.run(["git", "add", "."], check=True, cwd=mirrordir)
        subprocess.run(
            ["git", "commit", "-m", "pages"],
            check=True,
            cwd=mirrordir,
            env={
                "EMAIL": "shw@example.com",
            },
        )
        subprocess.run(
            [
                "git",
                "push",
                os.environ["EXPORT_GIT_URL"],
                "HEAD:gh-pages",
                "--force",
            ],
            check=True,
            cwd=mirrordir,
        )
