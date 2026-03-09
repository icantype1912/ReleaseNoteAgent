import os
import requests
from upgrade_agent.utils.version_utils import normalize_tag

print("DEBUG TOKEN:", os.getenv("GITHUB_TOKEN"))

def parse_github_repo(repo_url):

    repo_url = repo_url.replace(".git", "")
    repo_url = repo_url.rstrip("/")

    parts = repo_url.split("/")

    owner = parts[-2]
    repo = parts[-1]

    return owner, repo


def fetch_github_releases(repo_url):

    owner, repo = parse_github_repo(repo_url)

    url = f"https://api.github.com/repos/{owner}/{repo}/releases"

    token = os.getenv("GITHUB_TOKEN")

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "dependency-upgrade-agent"
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.get(url, headers=headers, timeout=10)

    print("DEBUG STATUS:", response.status_code)

    if response.status_code != 200:
        print("DEBUG RESPONSE:", response.text)
        return []

    releases = response.json()

    results = []

    for release in releases:

        results.append(
            {
                "version": normalize_tag(release.get("tag_name", "")),
                "notes": release.get("body", ""),
                "published_at": release.get("published_at"),
                "url": release.get("html_url"),
            }
        )

    return results