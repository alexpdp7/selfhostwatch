import pathlib
import subprocess
import tempfile


def export():
    with tempfile.TemporaryDirectory() as tempdir:
        tempdir = pathlib.Path(tempdir)
        subprocess.run(["wget", "--mirror", "--convert-links", "http://localhost:8000/updates/index.html"], check=True, cwd=tempdir)
        subprocess.run(["git", "init"], check=True, cwd=tempdir / "localhost:8000" / "updates")
        subprocess.run(["git", "add", "."], check=True, cwd=tempdir / "localhost:8000" / "updates")
        subprocess.run(["git", "commit", "-m", "pages"], check=True, cwd=tempdir / "localhost:8000" / "updates")
        subprocess.run(["git", "push", "git@github.com:alexpdp7/selfhostwatch.git", "HEAD:gh-pages", "--force"], check=True, cwd=tempdir / "localhost:8000" / "updates")
