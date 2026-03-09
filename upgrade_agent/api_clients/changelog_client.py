import requests


def fetch_changelog(repo_url):
    """
    Attempt to fetch CHANGELOG.md from a GitHub repository.
    """

    repo_url = repo_url.replace(".git", "").rstrip("/")

    parts = repo_url.split("/")

    owner = parts[-2]
    repo = parts[-1]

    possible_paths = [
        "CHANGELOG.md",
        "CHANGELOG",
        "changelog.md",
        "docs/CHANGELOG.md",
    ]

    for path in possible_paths:

        url = f"https://raw.githubusercontent.com/{owner}/{repo}/HEAD/{path}"

        try:

            response = requests.get(url, timeout=10)

            if response.status_code == 200 and response.text:

                print(f"Found changelog at: {path}")

                return response.text

        except Exception:
            pass

    return None