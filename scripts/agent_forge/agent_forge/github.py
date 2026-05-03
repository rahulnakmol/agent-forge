"""Minimal GitHub API client — resolves SHAs and fetches tarballs without full clone."""

import io
import tarfile

import httpx


def raw_url(repo: str, ref: str, path: str) -> str:
    return f"https://raw.githubusercontent.com/{repo}/{ref}/{path}"


def resolve_plugin_sha(repo: str, ref: str, path: str) -> str:
    """Latest commit SHA touching `path` at `ref`."""
    response = httpx.get(
        f"https://api.github.com/repos/{repo}/commits",
        params={"path": path, "sha": ref, "per_page": 1},
        timeout=30.0,
    )
    response.raise_for_status()
    commits = response.json()
    if not commits:
        raise ValueError(f"No commits found for {path} at {ref}")
    return commits[0]["sha"]


def fetch_plugin_tarball(repo: str, sha: str, dest: str) -> None:
    """Download repo tarball at sha, extract to dest."""
    response = httpx.get(
        f"https://api.github.com/repos/{repo}/tarball/{sha}",
        follow_redirects=True,
        timeout=120.0,
    )
    response.raise_for_status()
    with tarfile.open(fileobj=io.BytesIO(response.content), mode="r:gz") as tf:
        tf.extractall(dest, filter="data")
